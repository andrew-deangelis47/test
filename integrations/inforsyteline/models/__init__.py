from inforsyteline.utils import get_version_number
print(get_version_number())
if get_version_number() == "default":
    from .default_models import *  # noqa: F401, F403
else:
    from .syteline_10_models import *  # noqa: F401, F403
