#!/bin/sh
coverage run --source='dominion/' manage.py test $@ --verbosity=2 && coverage report --show-missing --fail-under=100 --omit="*test*.py" && find dominion -name '*.py' | grep -v migration | xargs flake8 && echo '\nSuccess'
