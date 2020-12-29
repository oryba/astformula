test:
	PYTHONPATH=${CURDIR} pytest tests/

check_flake8:
	flake8 --exclude=venv

check_pylint:
	pylint --rcfile=pylint.rc astformula

coverage:
	PYTHONPATH=${CURDIR} pytest tests/ --cov=astformula
