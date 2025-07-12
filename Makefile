PYTHON = python3
PROJECT_DIR = src
SETTINGS_FILE = pyproject.toml

.PHONY: format lint secure type-check enable-pre-commit-hooks install help

help:
	@echo "Available commands:"
	@echo "  make format  - Format the code with black and isort"
	@echo "  make lint    - Lint the code with flake8"
	@echo "  make secure    - Check security issues via bandit"
	@echo "  make type-check    - Check type issues via mypy"
	@echo "  make enable-pre-commit-hooks    - Enable pre commit hook"er"
	@echo "  make help    - Show this help message"

format:
	$(PYTHON) -m isort $(PROJECT_DIR) --settings $(SETTINGS_FILE)
	$(PYTHON) -m autoflake $(PROJECT_DIR) --config $(SETTINGS_FILE)
	$(PYTHON) -m black $(PROJECT_DIR) --config $(SETTINGS_FILE)
	$(PYTHON) -m autopep8 $(PROJECT_DIR) --global-config $(SETTINGS_FILE)

lint:
	flake8 --config=.flake8.cfg
	$(PYTHON) -m black $(PROJECT_DIR) --check --diff --config $(SETTINGS_FILE)
	$(PYTHON) -m isort $(PROJECT_DIR) --check --diff --settings $(SETTINGS_FILE)

secure:
	$(PYTHON) -m bandit -r $(PROJECT_DIR) --config ${SETTINGS_FILE}

type-check:
	$(PYTHON) -m mypy $(PROJECT_DIR) --config ${SETTINGS_FILE} --explicit-package-bases

enable-pre-commit-hooks:
	${PYTHON} -m pre_commit install

install:
	pip install -r requirements.txt