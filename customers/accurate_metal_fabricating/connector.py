import sys
print("sys.path at runtime:", sys.path)

from baseintegration.utils import run_integration

if __name__ == '__main__':
    run_integration()
