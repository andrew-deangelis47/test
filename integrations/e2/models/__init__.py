from e2.utils import get_version_number

if get_version_number() == "default":
    from .default_models import *  # noqa: F401, F403
else:
    from .e2_shop_system_models import *  # noqa: F401, F403
