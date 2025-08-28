PYTHON := python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
ULTRA := $(VENV)/bin/yolo

DATA := yolo/data.yaml
PARAMS := yolo/params.yaml
MODEL := yolov8n.pt

.PHONY: help venv train val export detect test lint clean

help:
	@echo "Targets:"
	@echo "  make venv            - create venv and install deps"
	@echo "  make train           - train YOLO model"
	@echo "  make val             - validate trained model"
	@echo "  make export          - export model to ONNX"
	@echo "  make detect IMG=...  - run inference on a single image"
	@echo "  make test            - run pytest visual suite"
	@echo "  make clean           - remove runs"

venv:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

train: venv
	$(ULTRA) detect train data=$(DATA) model=$(MODEL) project=runs name=gui epochs=50 imgsz=960 \
		$(if $(wildcard $(PARAMS)),cfg=$(PARAMS),)

val: venv
	$(ULTRA) detect val data=$(DATA) project=runs name=gui_val

export: venv
	$(ULTRA) export model=runs/gui/weights/best.pt format=onnx opset=13 dynamic=true

detect: venv
	@if [ -z "$(IMG)" ]; then echo "Usage: make detect IMG=path/to/image.png"; exit 1; fi
	$(ULTRA) detect predict model=runs/gui/weights/best.pt source=$(IMG) conf=0.5 save=True

test: venv
	$(PY) -m pytest -q

clean:
	rm -rf runs
