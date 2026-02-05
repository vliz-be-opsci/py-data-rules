TEST_PATH = ./tests/
FLAKE8_EXCLUDE = venv,.venv,.eggs,.tox,.git,__pycache__,*.pyc
PROJECT = py_data_rules
AUTHOR = Vlaams Instituut voor de Zee (VLIZ)
PYTHON = python
PIP = $(PYTHON) -m pip
POETRY = $(PYTHON) -m poetry

.DEFAULT_GOAL := run

.PHONY: build docs clean install docker-build

clean:
	@find . -name '*.pyc' -exec rm --force {} +
	@find . -name '*.pyo' -exec rm --force {} +
	@find . -name '*~' -exec rm --force {} +
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -f *.sqlite
	@rm -rf .cache

startup:
	$(PIP) install --upgrade pip
	$(POETRY) --version >/dev/null || $(PIP) install poetry

init: startup
	$(POETRY) install --extras 'tests' --extras 'dev' --extras 'docs'

init-base: startup
	$(POETRY) install

init-docs: startup
	$(POETRY) install --extras 'docs'

docs:
	if ! [ -d "./docs" ]; then $(POETRY) run sphinx-quickstart -q --ext-autodoc --sep --project $(PROJECT) --author $(AUTHOR) docs; fi
	$(POETRY) run sphinx-apidoc -f -o ./docs/source ./$(PROJECT)
	$(POETRY) run sphinx-build -E -a -b html ./docs/source ./docs/build/html

test:
	$(POETRY) run pytest ${TEST_PATH}

test-coverage:
	$(POETRY) run pytest --cov=$(PROJECT) ${TEST_PATH} --cov-report term-missing

check:
	$(POETRY) run black --check --diff .
	$(POETRY) run isort --check --diff .
	$(POETRY) run flake8 . --exclude ${FLAKE8_EXCLUDE}
	$(POETRY) run pyrefly check

lint-fix:
	$(POETRY) run black .
	$(POETRY) run isort .

docker-build:
	docker build . -t py_data_rules

update:
	$(POETRY) update

build: update check test docs
	$(POETRY) build

release: build
	$(POETRY) release
