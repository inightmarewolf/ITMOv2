.PHONY: install test run step6

PYTHON ?= python

install:
	@$(PYTHON) -c "import sys; assert sys.version_info >= (3, 10), 'Python 3.10+ required'; import sqlite3; print('Standard library only: ready')"

test: install
	$(PYTHON) -m unittest -v

step6: test

run:
	$(PYTHON) service.py
