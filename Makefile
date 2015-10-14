PY_FILES =$(shell git diff --name-only | grep \.py)
unit_test:
	python -m unittest discover test
acceptance:
	python -m unittest acceptance_test
format:
	@echo $(PY_FILES)
	autopep8 --in-place --recursive --verbose $(PY_FILES)
coverage:
	coverage run --branch -m  unittest discover
	coverage report -m --skip-covered
all: format unit_test coverage
