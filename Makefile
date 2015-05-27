PYTHON ::= python3
LINT_ARGS ::= --rcfile=pylint.ini
SOURCES ::= war3/mdx.py war3/model.py

.PHONY: lint

lint: $(SOURCES)
	$(PYTHON) -m pylint $(LINT_ARGS) $^
