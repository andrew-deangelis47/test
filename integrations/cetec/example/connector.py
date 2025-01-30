import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "integrations"))
sys.path.append(os.path.join(os.path.dirname(__file__), "integrations/cetec"))
sys.path.append(os.path.join(os.path.dirname(__file__), "integrations/baseintegration"))
from baseintegration.utils import run_integration

if __name__ == '__main__':
    run_integration()
