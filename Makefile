.PHONY: test

MODULES ?= frage

RUNNER ?= poetry run

check-all: black-check linters test

linters: mypy

black-format:
	$(RUNNER) black $(MODULES)

black-check:
	$(RUNNER) black --check $(MODULES)

flake8:
	$(RUNNER) flake8 $(MODULES)

mypy:
	$(RUNNER) mypy --ignore-missing-imports --strict-optional $(MODULES)

PYTESTARGS ?= -vv --tb=native tests

test:
	$(RUNNER) pytest $(PYTESTARGS)
