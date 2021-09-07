.PHONY: test

MODULES ?= frage

RUNNER ?= poetry run

all: black-format check-all

check-all: black-check linters test

linters: mypy

black-format:
	$(RUNNER) black $(MODULES) tests

black-check:
	$(RUNNER) black --check $(MODULES) tests

flake8:
	$(RUNNER) flake8 $(MODULES) tests

mypy:
	$(RUNNER) mypy --ignore-missing-imports --strict-optional $(MODULES) tests

PYTESTARGS ?= -vv --tb=native --cov=$(MODULES) tests

test:
	$(RUNNER) pytest $(PYTESTARGS)
