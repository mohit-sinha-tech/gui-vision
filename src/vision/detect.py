from typing import Dict
import numpy as np
from ultralytics import YOLO

DEFAULT_THRESH = 0.5
DEFAULT_IOU = 0.45

class GuiDetector:
    def __init__(self, weights_path: str, conf_overrides: Dict[str, float] | None = None):
        self.model = YOLO(weights_path)
        self.conf_overrides = conf_overrides or {}

    def predict(self, rgb_image: np.ndarray, conf: float = DEFAULT_THRESH, iou: float = DEFAULT_IOU):
        res = self.model.predict(rgb_image, conf=conf, iou=iou, verbose=False)[0]
        dets = []
        for b in res.boxes:
            cls_id = int(b.cls.item())
            cls_name = self.model.names[cls_id]
            conf_box = float(b.conf.item())
            # apply per-class overrides
            if conf_box < self.conf_overrides.get(cls_name, conf):
                continue
            x1, y1, x2, y2 = map(float, b.xyxy[0].tolist())
            dets.append({"cls": cls_name, "conf": conf_box, "xyxy": (x1, y1, x2, y2)})
        return dets
