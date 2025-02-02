# Makefile for CyberGenie

# Variables
PYTHON = python3
PIP = pip3
FLASK = flask
VENV_DIR = venv
REQUIREMENTS_FILE = requirements.txt

# Targets
.PHONY: all setup run test lint clean

all: setup run

setup:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/$(PIP) install -r $(REQUIREMENTS_FILE)

run:
	$(VENV_DIR)/bin/$(FLASK) run

test:
	$(VENV_DIR)/bin/$(PYTHON) -m pytest

lint:
	$(VENV_DIR)/bin/flake8 .

clean:
	rm -rf $(VENV_DIR)
