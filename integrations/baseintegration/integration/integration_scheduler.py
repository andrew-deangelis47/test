import time

import botocore.exceptions
from apscheduler.schedulers.background import BackgroundScheduler
from ...baseintegration.integration import logger
import boto3
from ...baseintegration.utils import get_data_migrator, should_time_out_integration_action_from_event, set_custom_formatter, reset_custom_formatter, mark_action_as_failed, mark_action_as_completed, mark_action_as_cancelled
from paperless.objects.integration_actions import IntegrationAction, ManagedIntegration
from paperless.objects.integration_heartbeats import IntegrationHeartbeat
from distutils.util import strtobool


class IntegrationScheduler:

    def __init__(self, integration):
        self.integration_should_run = True
        self.integration = integration
        self.release_image_id = self._get_release_image_id()
        self.scheduler = BackgroundScheduler()

    def run(self) -> None:
        self.schedule_tasks()
        self.scheduler.start()
        try:
            while True:
                if self.integration_should_run:
                    time.sleep(0.5)
                else:
                    raise Exception(f"Integration is being killed for {self.integration.paperless_config.slug} to get new image")
        except (KeyboardInterrupt, SystemExit, TimeoutError):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            self.scheduler.shutdown()

    def post_integration_heartbeat(self):
        logger.info("Posting integration heartbeat")
        x = IntegrationHeartbeat(600)
        x.create(self.integration.managed_integration_uuid)
        logger.info("Posted integration heartbeat")

    def check_for_integration_active_status(self):
        logger.info("Running integration active status listener")
        new_integration_active_status_events = ManagedIntegration.event_list(uuid=self.integration.managed_integration_uuid, params={"event_type_in": "integration.turned_on,integration.turned_off"})
        new_integration_active_status_events = sorted(
            new_integration_active_status_events,
            key=lambda x: x.created_dt
        )
        if len(new_integration_active_status_events) > 0:
            logger.info("New integration active status events detected, checking the most recent one")
            status = self.integration.integration_enabled
            if status and new_integration_active_status_events[-1].type == "integration.turned_off":
                status = False
                logger.info("Turning integration off")
            elif not status and new_integration_active_status_events[-1].type == "integration.turned_on":
                status = True
                logger.info("Turning integration on")
            self.integration.integration_enabled = status

    def check_for_new_integration_action_requests(self):
        logger.info("Running integration action request listener")
        new_ia_request_events = ManagedIntegration.event_list(uuid=self.integration.managed_integration_uuid, params={"event_type_in": "integration_action.requested"})
        new_ia_request_events = sorted(
            new_ia_request_events,
            key=lambda x: x.created_dt
        )
        logger.info(f"{str(len(new_ia_request_events))} new integration action requests found to process")
        for event in new_ia_request_events:
            action = IntegrationAction.get(event.data["uuid"])
            logger.info(f"Running integration action {action.uuid}")
            if not self.integration.integration_enabled:
                logger.info("Integration currently disabled - skipping this run")
                mark_action_as_cancelled(action, "Integration is currently off, skipping this order")
                continue
            if not self.integration.test_mode and should_time_out_integration_action_from_event(event):
                message = f"NOTICE: Integration action export_order with order {action.entity_id} and action UUID {action.uuid} is older than 3 days, it will be timed out and not processed."
                action.status = "timed_out"
                action.status_message = message
                action.update()
                continue
            action.status = "in_progress"
            action.current_record_count = 1
            action.update()

            # get a non bulk data migrator and set entity id to first
            if "bulk_" in event.data["type"]:
                non_bulk_event_type = event.data["type"].replace("bulk_", "")
                data_migrator = get_data_migrator(action_type=non_bulk_event_type, integration=self.integration)
                entity_id = "first"
            else:
                data_migrator = get_data_migrator(action_type=event.data["type"], integration=self.integration)
                entity_id = event.data["entity_id"]
            try:
                set_custom_formatter(self.integration, event.data["type"], str(entity_id))
                data_migrator.run(entity_id)
                mark_action_as_completed(action, data_migrator.success_message)
            except Exception as e:
                mark_action_as_failed(action, e, entity_id)
            reset_custom_formatter(self.integration)

    def schedule_tasks(self) -> None:  # noqa: C901
        logger.info("Scheduling tasks")
        logger.info("Scheduling task to check for new release image")
        self.scheduler.add_job(self.check_for_integration_active_status, "interval", minutes=1)
        self.scheduler.add_job(self.check_for_new_release_image, "interval", minutes=1)
        self.scheduler.add_job(self.check_for_new_integration_action_requests, "interval", minutes=1)
        self.post_integration_heartbeat()
        self.scheduler.add_job(self.post_integration_heartbeat, "interval", minutes=3)
        try:
            interval = self.integration.config_yaml["autoquote"]["interval"]
            logger.info("Found autoquote in the configuration!")
            x = get_data_migrator("auto_quote", self.integration)
            self.scheduler.add_job(x.run, "interval", minutes=interval)
        except KeyError:
            logger.info("Did not start the auto quoter")
        except Exception as e:
            logger.info("Autoquote failed to start -- logging exception")
            logger.info(e)
        try:
            interval = self.integration.config_yaml["Exporters"]["quotes"]["interval"]
            logger.info("Found quote exports in the configuration!")
            x = get_data_migrator("export_quote", self.integration)
            self.scheduler.add_job(x.run, "interval", minutes=interval)
        except KeyError:
            logger.info("Did not start the quote exporter")
        except Exception as e:
            logger.info("Quote exporter failed to start -- logging exception")
            logger.info(e)
        try:
            interval = self.integration.config_yaml["Exporters"]["orders"]["interval"]
            logger.info("Found order exports in the configuration!")
            x = get_data_migrator("export_order", self.integration)
            self.scheduler.add_job(x.run, "interval", minutes=interval)
        except KeyError:
            logger.info("Did not start the order exporter")
        except Exception as e:
            logger.info("Order exporter failed to start -- logging exception")
            logger.info(e)
        try:
            interval = self.integration.config_yaml["Importers"]["materials"]["interval"]
            logger.info("Found material imports in the configuration!")
            x = get_data_migrator("import_material", self.integration)
            self.scheduler.add_job(x.run, "interval", minutes=interval)
        except KeyError:
            logger.info("Did not start the material importer")
        except Exception as e:
            logger.info("Material importer failed to start -- logging exception")
            logger.info(e)
        try:
            interval = self.integration.config_yaml["Importers"]["quotes"]["interval"]
            logger.info("Found material pricing importer in the configuration!")
            x = get_data_migrator("import_material_pricing", self.integration)
            self.scheduler.add_job(x.run, "interval", minutes=interval)
        except KeyError:
            logger.info("Did not start the material pricing importer")
        except Exception as e:
            logger.info("Material pricing importer failed to start -- logging exception")
            logger.info(e)

        try:
            interval = self.integration.config_yaml["Importers"]["purchased_components"]["interval"]
            logger.info("Found purchased component imports in the configuration!")
            x = get_data_migrator("import_purchased_component", self.integration)
            self.scheduler.add_job(x.run, "interval", minutes=interval)
        except KeyError:
            logger.info("Did not start the purchased component importer")
        except Exception as e:
            logger.info("Purchased component importer failed to start -- logging exception")
            logger.info(e)
        try:
            interval = self.integration.config_yaml["Importers"]["accounts"]["interval"]
            logger.info("Found account imports in the configuration!")
            x = get_data_migrator("import_account", self.integration)
            self.scheduler.add_job(x.run, "interval", minutes=interval)
        except KeyError:
            logger.info("Did not start the account importer")
        except Exception as e:
            logger.info("Account importer failed to start -- logging exception")
            logger.info(e)
        try:
            interval = self.integration.config_yaml["Importers"]["work_centers"]["interval"]
            logger.info("Found work center imports in the configuration!")
            x = get_data_migrator("import_work_center", self.integration)
            self.scheduler.add_job(x.run, "interval", minutes=interval)
        except KeyError:
            logger.info("Did not start the work center importer")
        except Exception as e:
            logger.info("Work center importer failed to start -- logging exception")
            logger.info(e)
        try:
            interval = self.integration.config_yaml["Importers"]["outside_services"]["interval"]
            logger.info("Found outside service imports in the configuration!")
            x = get_data_migrator("import_service", self.integration)
            self.scheduler.add_job(x.run, "interval", minutes=interval)
        except KeyError:
            logger.info("Did not start the outside service importer")
        except Exception as e:
            logger.info("Outside service importer failed to start -- logging exception")
            logger.info(e)
        try:
            interval = self.integration.config_yaml["Importers"]["vendors"]["interval"]
            logger.info("Found vendor imports in the configuration!")
            x = get_data_migrator("import_vendor", self.integration)
            self.scheduler.add_job(x.run, "interval", minutes=interval)
        except KeyError:
            logger.info("Did not start the vendor importer")
        except Exception as e:
            logger.info("Vendor importer failed to start -- logging exception")
            logger.info(e)
        try:
            interval = self.integration.config_yaml["Importers"]["custom_table"]["interval"]
            logger.info("Found custom table record imports in the configuration!")
            x = get_data_migrator("import_custom_table_record", self.integration)
            self.scheduler.add_job(x.run, "interval", minutes=interval)
        except KeyError:
            logger.info("Did not start the custom table record importer")
        except Exception as e:
            logger.info("Custom table record importer failed to start -- logging exception")
            logger.info(e)
        try:
            interval = self.integration.config_yaml["Importers"]["repeat_part"]["interval"]
            logger.info("Found repeat part record imports in the configuration!")
            x = get_data_migrator("import_repeat_part", self.integration)
            self.scheduler.add_job(x.run, "interval", minutes=interval)
        except KeyError:
            logger.info("Did not start the repeat part importer")
        except Exception as e:
            logger.info("repeat part importer failed to start -- logging exception")
            logger.info(e)

    def check_for_new_release_image(self) -> None:
        if self.is_new_release_image():
            logger.info("Attempting to shutdown the scheduler")
            # removes all jobs from scheduler so nothing more will be scheduled
            self.scheduler.remove_all_jobs()
            try:
                # waits for scheduler to not have jobs
                self.scheduler.shutdown()
            except RuntimeError:
                pass
            # this is set so we can break out of the while True loop above
            self.integration_should_run = False

    def is_new_release_image(self) -> bool:
        # if current release image active is false and new secrets.ini is true, get release image id and then change release image active in memory
        if not self.integration.paperless_config.release_image_active and strtobool(self.integration._get_secrets().get("Paperless", {}).get("release_image_active", "False")):
            self.integration.paperless_config.release_image_active = True
            self.release_image_id = self._get_release_image_id()
        if (not self.release_image_id) or (self._get_release_image_id() == self.release_image_id):
            logger.info("New image is not detected, not killing")
            return False
        else:
            logger.info("New image is detected, killing")
            return True

    def _get_release_image_id(self) -> str:
        logger.info("Getting release image id")
        if self.integration.paperless_config.release_image_active and self.integration.paperless_config.slug and \
                self.integration.paperless_config.aws_access_key and self.integration.paperless_config.aws_secret_key:
            client = boto3.client('ecr',
                                  region_name='us-west-2' if not self.integration.paperless_config.v2_integration else 'us-east-1',
                                  aws_access_key_id=self.integration.paperless_config.aws_access_key,
                                  aws_secret_access_key=self.integration.paperless_config.aws_secret_key)
            try:
                images = client.describe_images(repositoryName=self.integration.paperless_config.slug).get("imageDetails")
            except botocore.exceptions.ClientError as e:
                if self.integration.paperless_config.customer_slug or self.integration.paperless_config.ecr_repository:
                    logger.warning(
                        f'Got the following exception checking ECR with this slug {self.integration.paperless_config.slug}: {e}')
                    if self.integration.paperless_config.ecr_repository:
                        try:
                            logger.info(f'trying ecr_repository for fallback repo name {self.integration.paperless_config.ecr_repository}')
                            images = client.describe_images(repositoryName=self.integration.paperless_config.ecr_repository).get("imageDetails")
                        except botocore.exceptions.ClientError as e:
                            if self.integration.paperless_config.customer_slug:
                                logger.warning(
                                    f'Got the following exception checking ECR with {self.integration.paperless_config.ecr_repository} as fallback: {e}')
                            else:
                                raise e
                    if self.integration.paperless_config.customer_slug:
                        logger.info(f'trying customer_slug fallback repo name {self.integration.paperless_config.customer_slug}')
                        images = client.describe_images(repositoryName=self.integration.paperless_config.customer_slug).get("imageDetails")
                else:
                    raise e
            release_image = {"imageDigest": None}
            for image in images:
                if "imageTags" in image and "release" in image["imageTags"]:
                    if not release_image:
                        release_image = image
                    else:
                        if (not release_image.get("imagePushedAt")) or (image["imagePushedAt"] > release_image["imagePushedAt"]):
                            release_image = image
            logger.info(f"release image ID is {release_image['imageDigest']}")
            return release_image['imageDigest']
        else:
            logger.info("Not getting release image info since one of the required parameters (release_image_active=True, slug, aws_access_key, aws_secret_key) is not populated")
