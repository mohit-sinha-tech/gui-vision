import base64
import numpy as np
import cv2
from selenium.webdriver.remote.webdriver import WebDriver

def webdriver_screenshot_rgb(driver: WebDriver):
    b64 = driver.get_screenshot_as_base64()
    png = base64.b64decode(b64)
    img = cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
