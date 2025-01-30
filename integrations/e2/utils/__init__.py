import os
import yaml


# this has to be in __init__.py because it needs to be defined before the e2 model import
def get_version_number() -> str:
    if os.environ.get('ERP_VERSION'):
        if "shop_system" in os.environ.get('ERP_VERSION'):
            return "shop_system"
        else:
            return "default"
    else:
        try:
            with open(os.path.join(os.path.dirname(__file__), "../../../config.yaml")) as file:
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                config_yaml = yaml.load(file, Loader=yaml.FullLoader)
                if config_yaml.get("Paperless") and config_yaml["Paperless"].get("erp_version") and "shop_system" in \
                        config_yaml["Paperless"]["erp_version"]:
                    return "shop_system"
        except Exception:
            pass
    return "default"
