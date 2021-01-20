"""
Allows for quick and simple debugging of tests.
Note:
    `pytest-cov` / `coverage.py` must be disabled for this to debug properly.
    Easiest way is to ensure that pytest gets passed the `- -no - cov` flag.
"""

import sys
import pytest

if __name__ == "__main__":
    # Checking if the setup.cfg contains lines that will mess with debugging.
    with open('setup.cfg', 'r') as setup_config:
        for line in setup_config.readlines():
            if not line.strip().startswith('#') and '--cov' in line:
                print('Cannot debug with coverage on. Switch it off in the `setup.cfg`.')
                sys.exit(0)
    pytest.main()
