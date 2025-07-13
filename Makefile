PYTHON = python3
SOURCE_DIRS = src tests
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
	$(PYTHON) -m isort $(SOURCE_DIRS) --settings $(SETTINGS_FILE)
	$(PYTHON) -m autoflake $(SOURCE_DIRS) --config $(SETTINGS_FILE)
	$(PYTHON) -m black $(SOURCE_DIRS) --config $(SETTINGS_FILE)
	$(PYTHON) -m autopep8 $(SOURCE_DIRS) --global-config $(SETTINGS_FILE)

lint:
	flake8 --config=.flake8.cfg
	$(PYTHON) -m black $(SOURCE_DIRS) --check --diff --config $(SETTINGS_FILE)
	$(PYTHON) -m isort $(SOURCE_DIRS) --check --diff --settings $(SETTINGS_FILE)

secure:
	$(PYTHON) -m bandit -r $(SOURCE_DIRS) --config ${SETTINGS_FILE}

type-check:
	$(PYTHON) -m mypy $(SOURCE_DIRS) --config ${SETTINGS_FILE} --explicit-package-bases

enable-pre-commit-hooks:
	${PYTHON} -m pre_commit install

install:
	pip install -r requirements.txt

test:
	${PYTHON} -m pytest

test-unit:
	${PYTHON} -m pytest -svvv -m "unit" tests

test-integration:
	${PYTHON} -m pytest -svvv -m "integration" tests