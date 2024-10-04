##
## Hand-e project, 2024
## hostasphere python profiler api
## File description:
## Makefile
##

TOKEN_FILE = token.secret

all: clean build upload

build:
	python setup.py sdist bdist_wheel

upload:
	@echo "Uploading to PyPI..."
	@TOKEN=$$(cat $(TOKEN_FILE)) && \
	twine upload -r pypi -u __token__ -p $$TOKEN dist/*

clean:
	rm -rf dist build *.egg-info

fclean: clean
	rm -rf .tox .pytest_cache .coverage

.PHONY: all build upload clean generate_grpc
