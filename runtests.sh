#! /bin/bash

rm -rf .coverage
coverage run ./manage.py test --settings=dominion.settings_tests "$@" -v 2 --noinput --buffer &&
coverage report --show-missing --skip-covered &&
echo "Success"
