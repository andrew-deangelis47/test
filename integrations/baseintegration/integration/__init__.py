import yaml
import os
import logging
import sys
from configparser import RawConfigParser
from logging.handlers import TimedRotatingFileHandler
from paperless.client import PaperlessClient
from paperless.objects.integration_actions import ManagedIntegration
import sentry_sdk
from distutils.util import strtobool

# Set up a basic logger just in case something tries to use the logger before configure_logging() is run
logger = logging.getLogger('paperless')
logger.setLevel(logging.DEBUG)
logging_configured = False


class Integration:
    """This is an orchestration class that uses the APScheduler library to
    schedule imports and exports and read from config.yaml """
    INTEGRATION_VERSION = '1.0*'

    def __init__(self):
        self.integration_enabled = True
        self._client = None
        self._logging_configured = False
        self.test_mode: bool = any("test" in string for string in sys.argv) or os.environ.get('TEST')
        self.config_yaml = None
        self.paperless_config = None
        self.secrets = None
        self.api_client = None
        self.get_config_yaml()
        self.ph = None
        self.fh = None
        self.managed_integration_uuid = None
        self.default_formatter = None
        self._setup()
        self._setup_sentry()
        from baseintegration.integration.integration_scheduler import IntegrationScheduler  # noqa: E402
        self.integration_scheduler = IntegrationScheduler(self)

    def run(self) -> None:
        self.integration_scheduler.run()

    def _setup(self) -> None:
        self.secrets = self._get_secrets()
        if "Paperless" not in self.secrets:
            raise ValueError("Paperless section not found in secrets.ini. Are you sure the secrets file is present?")
        self.config = {**self.config_yaml["Paperless"], **self.secrets["Paperless"]}
        self._setup_paperless_config(self.config)
        self._configure_logging(self.paperless_config.logpath)
        logger.info("Setting up Paperless client")

        self._client = PaperlessClient(
            access_token=self.paperless_config.token,
            group_slug=self.paperless_config.slug,
            base_url=self.paperless_config.base_url
        )
        try:
            # we make the assumption right now that only one managed integration is registered - this may change over time
            self.managed_integration_uuid = self.config["managed_integration_uuid"]
        except:
            raise ValueError("Managed integration UUID not present in secrets.ini file, please add it")
        try:
            ManagedIntegration.get(self.managed_integration_uuid)
        except:
            raise ValueError("Managed integration not found for user group, please double check API token and managed integration UUID")

    def _setup_sentry(self) -> None:
        if self.paperless_config and self.paperless_config.sentry_dsn:
            logger.info("Configuring Sentry")
            sentry_sdk.init(self.paperless_config.sentry_dsn, server_name=self.paperless_config.slug)

    def _configure_logging(self, log_file_path: str) -> None:
        """ Only run configure_logging if logging has not already been configured. Otherwise, we end up adding duplicate
            handlers which results in duplicate log statements. """
        if logger.handlers:
            logger.handlers = []
        if not self._logging_configured:
            self.default_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.ph = logging.StreamHandler(sys.stdout)
            self.ph.setFormatter(self.default_formatter)
            logger.addHandler(self.ph)

            self.fh = TimedRotatingFileHandler(
                os.path.join(os.path.dirname(__file__), f"../../../logs/{log_file_path}"),
                backupCount=30,
                when='midnight',
                interval=1
            )
            self.fh.suffix = '%Y-%m-%d'
            self.fh.setFormatter(self.default_formatter)
            self.fh.setLevel(logging.INFO)
            logger.addHandler(self.fh)

            self._logging_configured = True

    def get_config_yaml(self) -> None:
        try:
            with open(os.path.join(os.path.dirname(__file__), "../../../config.yaml")) as file:
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                self.config_yaml = yaml.load(file, Loader=yaml.FullLoader)
        except Exception:
            self.config_yaml = None
        # Paperless key is set here to allow tests to pass
        if not self.config_yaml:
            self.config_yaml = {"Paperless": {}}

    def _setup_paperless_config(self, config: dict) -> None:
        if self.paperless_config is None:
            class PaperlessConfig:
                def __init__(self, **kwargs):
                    self.v2_integration = kwargs.get('v2_integration', False)
                    self.token = kwargs.get('token')
                    self.slug = kwargs.get('slug')
                    self.customer_slug = kwargs.get('customer_slug')
                    self.release_image_active = kwargs.get('release_image_active')
                    self.should_write_to_paperless_parts = kwargs.get('should_write_to_paperless_parts')
                    self.logpath = kwargs.get('logpath')
                    self.base_url = kwargs.get('base_url')
                    self.aws_access_key = kwargs.get('aws_access_key')
                    self.aws_secret_key = kwargs.get('aws_secret_key')
                    self.managed_integration_uuid = kwargs.get('managed_integration_uuid')
                    self.ecr_repository = kwargs.get('ecr_repository')
                    self.new_customer_emails = kwargs.get('new_customer_emails')
                    self.source_email = kwargs.get('source_email')
                    self.sentry_dsn = kwargs.get('sentry_dsn')

            # if you would like to test using the integrations group, just set "testing_token" in your secrets file
            # and comment it out as needed w/ a semicolon
            # ;testing_token=123456789
            if config.get('testing_token'):
                token = config['testing_token']
                base_url = "https://release.paperlessparts.com/api"
            else:
                token = config['token']
                base_url = config.get('base_url', 'https://api.paperlessparts.com')

            self.paperless_config = PaperlessConfig(
                token=token,
                v2_integration=config.get('v2_integration', 'False'),
                slug=config['slug'],
                logpath=config['logpath'],
                customer_slug=config.get('customer_slug'),
                release_image_active=strtobool(config.get('release_image_active', 'False')),
                # Make should_write_to_paperless_parts default to True for backwards compatibility
                should_write_to_paperless_parts=strtobool(config.get('should_write_to_paperless_parts', 'True')),
                base_url=base_url,
                aws_access_key=config['aws_access_key'] if not self.test_mode else 'aws_access_key',
                aws_secret_key=config['aws_secret_key'] if not self.test_mode else 'aws_secret_key',
                managed_integration_uuid=config.get('managed_integration_uuid'),
                ecr_repository=config.get('ecr_repository'),
                new_customer_emails=config.get('new_customer_emails'),
                source_email=config.get('source_email'),
                sentry_dsn=config.get('sentry_dsn')
            )

            # modify the slug for v2 if needed
            if self.paperless_config.v2_integration:
                self.paperless_config.slug = f'integrations/customers/{self.paperless_config.slug}'

    def _get_secrets(self) -> dict:
        print('Reading secrets configuration file')
        with open(os.path.join(os.path.dirname(__file__), "../../../secrets.ini")) as fp:
            parser = RawConfigParser()
            parser.read_file(fp)
            return parser._sections
