.PHONY: test

MODULES ?= frage tests

RUNNER ?= poetry run

all: black-format check-all

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

PYTESTARGS ?= -vv --tb=native --cov=frage

test:
	$(RUNNER) pytest $(PYTESTARGS)

publish:
	poetry publish --build
