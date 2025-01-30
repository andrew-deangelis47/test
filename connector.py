import os
import sys

def resource_path(relative_path):
    """
    Use sys._MEIPASS if present (PyInstaller),
    else fallback to normal.
    """
    try:
        base_path = sys._MEIPASS  # Set by PyInstaller
    except AttributeError:
        base_path = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(base_path, relative_path))


sys.path.append(resource_path("integrations"))
sys.path.append(resource_path("integrations/epicor"))
sys.path.append(resource_path("integrations/baseintegration"))


from baseintegration.utils import run_integration

if __name__ == '__main__':
    run_integration()
