from typing import Type

import boto3
from contextlib import contextmanager

from ...baseintegration.datamigration import BaseDataMigration, logger
from ...baseintegration.exporter.processor import BaseProcessor
from ...baseintegration.exporter.exceptions import ProcessorNotRegisteredError, IntegrationNotImplementedError

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from paperless.main import PaperlessSDK


class BaseExporter(BaseDataMigration):
    """
    This is the base class to run an export between an Paperless and an ERP.
    The core of the class is run(), which will call the paperless listener and process updates.
    Run() should be overriden by OrderExporter() / QuoteExporter() / etc
    """

    paperless_config = None

    def __init__(self, integration):
        super().__init__(integration)
        # TODO: support looping
        self.my_sdk = PaperlessSDK(loop=False)

    def run(self):
        """
        calling this method is what runs the export.
        """
        raise IntegrationNotImplementedError(f"run() is not implemented for {self.__class__.__name__}")

    def register_processor(self, cls, processor_cls: Type[BaseProcessor]):
        """
        Register which Processor subclass will handle the creation and updating of the cls passed in. Can be used to
        override an existing processor.
        :param cls: The ERP wrapper class whose object will be output
        :param processor_cls: The processor who will produce an instance of the cls. Should be inherited class from baseintegration.exporter.processor.BaseProcessor
        :return:
        """
        self._registered_processors[cls.__name__] = processor_cls

    def get_processor_instance(self, cls):
        """
        Get a registered processor by its key. It can be helpful to access an instance of a processor outside the
        standard process_resource flow in situations where the processor has helper methods that can be useful in
        other processors.
        :param cls: The class the processor is registered for
        :return: The registered processor
        """
        processor_cls = self._registered_processors.get(cls.__name__, None)
        if processor_cls is None:
            return None
        processor_instance = processor_cls(self)
        return processor_instance

    def remove_processor(self, cls):
        """
        Register which Processor subclass will handle the creation and updating of the cls passed in.
        :param cls: The ERP wrapper class whose processor should be removed
        :return:
        """
        self._registered_processors.pop(cls.__name__, None)

    @contextmanager
    def process_resource(self, cls, *args, **kwargs):
        """
        This will process the provided inputs and output a resource by calling the registered processor of a class
        :return:
        """
        # TODO: Should we throw an error if no processor is registered for class? Seems like silently failing here
        # Could make more bugs later.
        processor_cls = self._registered_processors.get(cls.__name__, None)
        if processor_cls:
            # TODO: consider storing the list of processor() objects produced to ensure a many/many rollback at runtime.
            logger.info(f'processing_resource {cls.__name__}')
            val = None
            res_processor = None
            try:
                res_processor = processor_cls(self)
                val = res_processor.run(*args, **kwargs)
            except Exception as e:
                if res_processor.do_rollback:
                    logger.exception(f"Error in processor {cls.__name__}, calling .rollback()!")
                    res_processor.rollback(val, *args, **kwargs)
                else:
                    logger.exception(f'Error in processor {cls.__name__}! Skipping .rollback()!')
                raise e
            # Once we have the value, we will yield it out
            try:
                yield val
            except StopIteration as e:
                logger.info(e)

        else:
            # TODO: add sentry logger.error, maybe replace raising the error...
            raise ProcessorNotRegisteredError(f"No processor was registered for provided resource: {str(cls)}")

    def send_email(self, subject: str, body: str, filepath=None, additional_recipients=[]):
        emails_str = self._integration.paperless_config.new_customer_emails
        if not emails_str:
            logger.info("No destination emails found. Not sending email")
            return
        if not self._integration.paperless_config.source_email:
            logger.info("Source email not found. Cannot send the email")
            return
        if not self._integration.paperless_config.release_image_active:
            logger.info("Not sending email as release image active is not set - this is dev")
            return
        to_list = emails_str.split(',')
        to_list.extend(additional_recipients)
        if len(to_list) < 1:
            return
        client = boto3.client(
            'ses',
            region_name='us-west-2',
            aws_access_key_id=self._integration.paperless_config.aws_access_key,
            aws_secret_access_key=self._integration.paperless_config.aws_secret_key,
        )
        if filepath:
            for to in to_list:
                msg = MIMEMultipart()
                msg["Subject"] = subject
                msg["From"] = self._integration.paperless_config.source_email
                msg["To"] = to

                # Set message body
                body = MIMEText(body, "plain")
                msg.attach(body)

                with open(filepath, "rb") as attachment:
                    part = MIMEApplication(attachment.read())
                    part.add_header("Content-Disposition",
                                    "attachment",
                                    filename=filepath)
                msg.attach(part)
                response = client.send_raw_email(
                    Source=self._integration.paperless_config.source_email,
                    Destinations=to_list,
                    RawMessage={"Data": msg.as_string()}
                )
        else:
            if self._integration.paperless_config.source_email:
                response = client.send_email(
                    Destination={
                        'ToAddresses': to_list},
                    Message={
                        'Body': {
                            'Text': {
                                'Charset': "UTF-8",
                                'Data': body,
                            },
                        },
                        'Subject': {
                            'Charset': "UTF-8",
                            'Data': subject,
                        },
                    },
                    Source=self._integration.paperless_config.source_email,
                )
            else:
                response = "Failed to send email as source email is not set in config"
        logger.info(response)
