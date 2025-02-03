from plex_v2.configuration import PlexConfig
from plex_v2.utils.export import ExportUtils
from plex_v2.utils.import_utils import ImportUtils
from typing import Union


class BaseFactory:

    config: PlexConfig
    utils: ExportUtils

    def __init__(self, config: PlexConfig, utils: Union[ExportUtils, ImportUtils]):
        self.config = config
        self.utils = utils
