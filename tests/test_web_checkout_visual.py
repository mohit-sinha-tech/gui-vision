import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.web.selenium_utils import webdriver_screenshot_rgb
from src.vision.asserts import assert_present, assert_absent, assert_above

@pytest.fixture
def driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,900")
    drv = webdriver.Chrome(options=opts)
    yield drv
    drv.quit()

def test_checkout_summary_visual(driver, detector):
    # Replace with your real URL
    driver.get("https://example.com/")
    time.sleep(1.0)

    img = webdriver_screenshot_rgb(driver)
    dets = detector.predict(img)
    # Example assertions – set real expectations after training your model
    assert_present(dets, "Price", at_least=0)
    assert_present(dets, "PrimaryButton", at_least=0)
    assert_absent(dets, "Spinner")
    # If both detected, ensure visual order
    if any(d['cls']=='Price' for d in dets) and any(d['cls']=='PrimaryButton' for d in dets):
        assert_above(dets, "Price", "PrimaryButton", min_gap=8)
