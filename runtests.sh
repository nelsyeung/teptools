export PYTHONPATH="./teptools:$PYTHONPATH" &&
	coverage run -m py.test tests &&
	coverage report
