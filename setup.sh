#!/usr/bin/env bash
set -e

WITH_OCR=0
for arg in "$@"; do
  case $arg in
    --with-ocr) WITH_OCR=1 ;;
  esac
done

echo "==> Python: $(python3 --version || true)"
echo "==> Creating virtualenv at .venv"
python3 -m venv .venv
. .venv/bin/activate

echo "==> Upgrading pip and installing requirements"
pip install --upgrade pip wheel
pip install -r requirements.txt

if [ "$WITH_OCR" -eq 1 ]; then
  echo "==> OCR requested. Please ensure Tesseract is installed system-wide."
  echo "    macOS: brew install tesseract"
  echo "    Ubuntu: sudo apt-get update && sudo apt-get install -y tesseract-ocr"
fi

cat <<'TIP'

✅ Setup complete.

Next steps:
1) Place your dataset under data/images and data/labels (train/val/test).
2) Train a model:
   make train
3) Validate:
   make val
4) Run the visual smoke tests:
   make test
   # or: GUI_MODEL=runs/gui/weights/best.pt make test

Selenium (optional):
- Install Chrome + Chromedriver, ensure 'chromedriver' is on PATH.
- Update tests/test_web_checkout_visual.py with your real URL and expectations.

Appium (optional):
- Install Node.js and Appium server, set up Android/iOS SDKs.
- Use src/mobile/appium_utils.py to capture screenshots and add tests similarly.

TIP
