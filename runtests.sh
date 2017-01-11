export PYTHONPATH="./teptools:$PYTHONPATH" &&
	flake8 teptools tests &&
	coverage run -m py.test tests &&
	coverage report
