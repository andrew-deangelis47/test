from m2m.utils import get_version_number

if get_version_number() == "default":
    from .default_models import *  # noqa: F401, F403
else:
    from .m2m_shop_system import *  # noqa: F401, F403
