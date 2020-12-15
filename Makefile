test:
	PYTHONPATH=astformula pytest tests/

check_flake8:
	flake8

check_pylint:
	pylint --rcfile=pylint.rc astformula

coverage:
	PYTHONPATH=astformula pytest tests/ --cov=astformula
