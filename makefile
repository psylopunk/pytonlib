VENV ?= .venv
PYTHON_VERSION ?= 3.10

init:
	python$(PYTHON_VERSION) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install

publish:
	$(VENV)/bin/poetry config pypi-token.pypi $(PYPI_TOKEN)
	$(VENV)/bin/poetry publish --build
