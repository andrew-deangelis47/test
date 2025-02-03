import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "integrations"))
sys.path.append(
    os.path.join(os.path.dirname(__file__), "integrations/globalshop"))
sys.path.append(
    os.path.join(os.path.dirname(__file__), "integrations/baseintegration"))

from baseintegration.integration import logger
from baseintegration.utils import run_integration

logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    run_integration()
