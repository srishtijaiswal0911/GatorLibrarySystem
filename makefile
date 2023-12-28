PYTHON = python
SCRIPT = gatorLibrary.py
TEST_CASE = 'testcase1.txt'

run:
	$(PYTHON) $(SCRIPT) $(TEST_CASE)

.PHONY: run