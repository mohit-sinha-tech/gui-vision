import numpy as np
import cv2
from mss import mss

def grab_screen(region: dict | None = None):
    """Return an RGB numpy image of the full screen or a region.
    region example: {"top":0, "left":0, "width":1280, "height":800}
    """
    with mss() as sct:
        mon = sct.monitors[1]
        bbox = {"top": mon["top"], "left": mon["left"], "width": mon["width"], "height": mon["height"]}
        if region:
            bbox = region
        img = np.array(sct.grab(bbox))[:, :, :3]  # BGRA->BGR
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
