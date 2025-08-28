# GUI Visual Validation (YOLO) – Starter Package

A production-ready starter to add **visual validation** to your automation framework using **YOLO (Ultralytics)**.
It works with plain desktop screenshots, **Selenium** (web), and **Appium** (mobile). Includes dataset config, a
detector wrapper, visual assertions, pytest integration, Makefile, and setup scripts.

---

## 🚀 What you get
- YOLO **dataset config** (`yolo/data.yaml`) for GUI element classes
- **Detector wrapper** and **assertion utilities**
- **Selenium/Appium** screenshot helpers
- **Pytest** runner with sample tests
- **Makefile** (train/val/export/detect/test)
- **setup.sh** to bootstrap a virtualenv and dependencies
- Clean **project structure**

```
gui-vision/
├─ data/
│  ├─ images/{train,val,test}/        # your screenshots
│  └─ labels/{train,val,test}/        # YOLO txt labels
├─ models/
│  └─ yolov8n.pt                      # base weights (auto-downloaded on first run)
├─ yolo/
│  ├─ data.yaml                       # dataset config (edit class names if needed)
│  └─ params.yaml                     # optional training params
├─ src/
│  ├─ vision/
│  │  ├─ detect.py                    # GuiDetector wrapper (Ultralytics)
│  │  ├─ asserts.py                   # presence/overlap/layout checks
│  │  └─ screenshot.py                # desktop screen capture
│  ├─ web/selenium_utils.py           # Selenium → RGB numpy image
│  └─ mobile/appium_utils.py          # Appium → RGB numpy image
├─ tests/
│  ├─ test_visual_smoke.py            # desktop example
│  └─ test_web_checkout_visual.py     # Selenium example
├─ conftest.py                        # pytest fixture for detector
├─ pytest.ini
├─ requirements.txt
├─ Makefile
├─ setup.sh
└─ .gitignore
```

---

## 🔧 Prerequisites

### Mandatory
- **Python 3.10+** and **pip**
- macOS or Linux (Windows works with WSL or adjust `setup.sh`)
- For **training/inference**: CPU works; GPU optional (CUDA supported by Ultralytics if available)

### Optional (for features you enable)
- **OCR**: Tesseract (`brew install tesseract` on macOS, `sudo apt-get install tesseract-ocr` on Ubuntu)
- **Selenium (Web)**: Google Chrome + Chromedriver (or another browser/driver)
- **Appium (Mobile)**: Node.js + Appium server and platform SDKs (Android/iOS). This starter only includes Python client helpers.

---

## 🧱 Install

```bash
cd gui-vision
chmod +x setup.sh
./setup.sh
# or: ./setup.sh --with-ocr
```

What it does:
- Creates a **venv** in `.venv/`
- Installs Python dependencies from `requirements.txt`
- Prints helpful post-setup tips

> If you plan to use Selenium tests headlessly, ensure `chromedriver` is installed and on PATH.

---

## 📁 Dataset

Put your images and labels like this:

```
data/
├─ images/train/   img1.png, img2.jpg, ...
├─ images/val/
└─ images/test/
data/labels/train/ img1.txt, img2.txt, ...
data/labels/val/
data/labels/test/
```

Each label file is YOLO format per line: `class_id cx cy w h` normalized to [0,1].
Edit class names in `yolo/data.yaml` if needed.

Default classes included:
```
PrimaryButton, SecondaryButton, SearchIcon, Spinner, Toast,
Modal, Tooltip, ErrorBanner, Checkbox, Radio, Switch,
Avatar, TabActive, TabInactive, Badge, Price, CartIcon
```

---

## 🏃 Quick Start

### 1) Train (after placing your images/labels)
```bash
make train
```

### 2) Validate
```bash
make val
```

### 3) Quick detect on an image
```bash
make detect IMG=./data/images/val/sample.png
```

### 4) Run tests (desktop visual smoke)
```bash
make test
```

Set a specific model for tests:
```bash
GUI_MODEL=runs/gui/weights/best.pt make test
```

---

## 🧪 Sample tests explained

- `tests/test_visual_smoke.py`: grabs a full-screen screenshot, runs detection, asserts:
  - a `PrimaryButton` exists,
  - no `Spinner` remains,
  - no overlap among selected classes.

- `tests/test_web_checkout_visual.py`: navigates with Selenium, screenshots the page, asserts:
  - `Price` and `PrimaryButton` detected,
  - `Spinner` absent,
  - `Price` appears above `PrimaryButton` by at least 8 px.

---

## 🧩 Integrating with your framework

- **Selenium/Appium**: Import helpers from `src/web/selenium_utils.py` and `src/mobile/appium_utils.py` to convert screenshots to NumPy RGB images.
- **Threshold tuning**: In `conftest.py` you can override class-specific confidences (e.g., stricter for tiny icons).
- **CI**: Use the **PR smoke pack** (a handful of critical screens). Run the full pack nightly.

---

## 🛠 Troubleshooting

- **Ultralytics import fails**: Re-run `./setup.sh`; ensure Python ≥ 3.10.
- **No detections**: Lower conf threshold or validate your labels/images alignment.
- **Flaky detections**: Wait for animations to finish or increase class-specific conf; try `min_gap` ≥ 8 px for layout.
- **Selenium driver errors**: Install matching Chrome/Chromedriver; set `PATH` properly.

---

## 📜 License
MIT – free to use and adapt. Please keep the notice when sharing.
