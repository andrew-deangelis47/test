import os
import yaml

VERSION_2020 = "2020"
VERSION_2022 = "2022"
VERSION_2019 = "2019"
VERSION_DEFAULT = "default"


# this has to be in __init__.py because it needs to be defined before the mietrak pro model import
def get_version_number() -> str:
    try:
        with open(os.path.join(os.path.dirname(__file__), "../../../config.yaml")) as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            config_yaml = yaml.load(file, Loader=yaml.FullLoader)
            if config_yaml.get("Paperless") and str(config_yaml["Paperless"].get("erp_version")) == VERSION_2020:
                return VERSION_2020
            if config_yaml.get("Paperless") and str(config_yaml["Paperless"].get("erp_version")) == VERSION_2019:
                return VERSION_2019
            if config_yaml.get("Paperless") and str(config_yaml["Paperless"].get("erp_version")) == VERSION_2022:
                return VERSION_2022
    except Exception:
        pass
    return VERSION_DEFAULT
