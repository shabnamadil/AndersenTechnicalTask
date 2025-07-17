PYTHON = python3
SOURCE_DIRS = src tests
DEVELOPMENT_DIR = _development
PROJECT_DIR = src
SETTINGS_FILE = pyproject.toml

.PHONY: format lint secure type-check enable-pre-commit-hooks test test-unit test-integration dev-install dev-build dev-setup dev-run help

help:
	@echo "Available commands:"
	@echo "  make format  - Format the code with black and isort"
	@echo "  make lint    - Lint the code with flake8"
	@echo "  make secure    - Check security issues via bandit"
	@echo "  make type-check    - Check type issues via mypy"
	@echo "  make enable-pre-commit-hooks    - Enable pre commit hook"er"
	@echo "  make test    - Run all tests"
	@echo "  make test-unit  - Run only unit tests"
	@echo "  make test-integration  - Run only integration tests"
	@echo "  make dev-install  - Install development stage dependencies"
	@echo "  make dev-run  - Run development server"
	@echo "  make dev-setup  - Make ready development server"
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

test:
	${PYTHON} -m pytest

test-unit:
	${PYTHON} -m pytest -svvv -m "unit" tests

test-integration:
	${PYTHON} -m pytest -svvv -m "integration" tests

dev-install:
	cd ${DEVELOPMENT_DIR} && pip install -r requirements_dev.txt

dev-build:
	cd ${DEVELOPMENT_DIR} && docker compose -f docker-compose.dev.yml up --build -d

dev-run:
	cd ${PROJECT_DIR} && ${PYTHON} manage.py runserver

dev-setup: dev-install dev-build

migrate-all:
	cd ${PROJECT_DIR} && $(PYTHON) manage.py makemigrations users tasks --noinput && python3 manage.py migrate --noinput