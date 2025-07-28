test:
	pytest

coverage:
	pytest --cov=python_practice --cov-report term-missing

lint:
	flake8 python_practice

check: lint test