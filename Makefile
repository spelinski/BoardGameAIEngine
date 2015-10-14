PY_FILES =$(shell git diff --name-only | grep \.py)
unit_test:
	python -m unittest discover test -t .
acceptance_test:
	python -m unittest discover acceptance
format:
	@echo $(PY_FILES)
	autopep8 --in-place --recursive --verbose $(PY_FILES)
coverage:
	coverage run --branch -m  unittest discover test -t .
	coverage run -a --branch -m unittest discover acceptance
	coverage report -m --skip-covered
test: unit_test acceptance_test
all: format test coverage
