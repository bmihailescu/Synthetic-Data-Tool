import sys
from pathlib import Path

AUTOMATION_TESTING_DIR = Path(__file__).resolve().parent.parent
if str(AUTOMATION_TESTING_DIR) not in sys.path:
    sys.path.insert(0, str(AUTOMATION_TESTING_DIR))

from StepDefinitions import HomeStepDefinitions  # noqa: F401
