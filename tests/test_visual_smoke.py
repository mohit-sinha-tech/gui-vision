import time
from src.vision.screenshot import grab_screen
from src.vision.asserts import assert_present, assert_absent, assert_no_overlap

def test_desktop_visual_smoke(detector):
    time.sleep(0.5)  # allow UI to settle if you're navigating elsewhere
    img = grab_screen()
    dets = detector.predict(img)
    # Example assertions – adjust to your UI reality
    assert_present(dets, "PrimaryButton", at_least=0)  # set 1 when your model is trained
    assert_absent(dets, "Spinner")
    assert_no_overlap(dets, ["PrimaryButton", "SearchIcon", "Toast"], max_iou=0.01)
