import os
import pytest
from src.vision.detect import GuiDetector

@pytest.fixture(scope="session")
def detector():
    weights = os.getenv("GUI_MODEL", "runs/gui/weights/best.pt")
    return GuiDetector(weights_path=weights, conf_overrides={
        "Spinner": 0.60,
        "SearchIcon": 0.55,
    })
