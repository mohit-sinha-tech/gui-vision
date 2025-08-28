from typing import List, Tuple

BBox = Tuple[float, float, float, float]

def iou(a: BBox, b: BBox) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    inter_x1, inter_y1 = max(ax1, bx1), max(ay1, by1)
    inter_x2, inter_y2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0, inter_x2 - inter_x1), max(0, inter_y2 - inter_y1)
    inter = iw * ih
    ua = (ax2 - ax1) * (ay2 - ay1)
    ub = (bx2 - bx1) * (by2 - by1)
    return inter / (ua + ub - inter + 1e-6)

def assert_present(dets, cls: str, at_least: int = 1):
    count = sum(1 for d in dets if d["cls"] == cls)
    assert count >= at_least, f"Expected ≥{at_least} '{cls}', found {count}"

def assert_absent(dets, cls: str):
    count = sum(1 for d in dets if d["cls"] == cls)
    assert count == 0, f"Expected no '{cls}', found {count}"

def assert_no_overlap(dets, classes: List[str], max_iou: float = 0.01):
    boxes = [(d["cls"], d["xyxy"]) for d in dets if d["cls"] in classes]
    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            ci, bi = boxes[i]
            cj, bj = boxes[j]
            ov = iou(bi, bj)
            assert ov <= max_iou, f"Overlap {ci}-{cj} = {ov:.3f} > {max_iou}"

def assert_above(dets, top_cls: str, bottom_cls: str, min_gap: int = 4):
    tops = [d for d in dets if d["cls"] == top_cls]
    bots = [d for d in dets if d["cls"] == bottom_cls]
    assert tops and bots, f"Need both {top_cls} and {bottom_cls}"
    for t in tops:
        tx1, ty1, tx2, ty2 = t["xyxy"]
        for b in bots:
            bx1, by1, bx2, by2 = b["xyxy"]
            gap = by1 - ty2
            assert gap >= min_gap, f"{top_cls} not above {bottom_cls}; gap {gap}px < {min_gap}px"
