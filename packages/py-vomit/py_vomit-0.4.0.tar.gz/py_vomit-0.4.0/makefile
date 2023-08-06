.PHONY = build publish mypy tox
DEFAULT_TARGET: build

mypy:
	mypy src
	mypy tests
	mypy tools

build:
	rm -rf build dist
	python -m build --sdist --wheel --outdir dist/

publish:
	twine upload --verbose dist/*
