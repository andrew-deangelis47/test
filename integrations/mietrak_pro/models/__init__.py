from mietrak_pro.utils import get_version_number, VERSION_2020, VERSION_2019, VERSION_2022

if get_version_number() == VERSION_2020:
    from .v2020_models import *  # noqa: F401, F403
elif get_version_number() == VERSION_2019:
    from .v2019_models import *  # noqa: F401, F403
elif get_version_number() == VERSION_2022:
    from .v2022_models import *  # noqa: F401, F403
else:
    from .default_models import *  # noqa: F401, F403
