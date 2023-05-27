#! /bin/bash

rm -rf .coverage.* .coverage
coverage run ./manage.py test --settings=dominion.settings_tests "$@" -v 2 --noinput --buffer --parallel=8 &&
coverage combine &&
coverage report --show-missing --skip-covered &&
echo "Success"
