#!/bin/bash

set -eo pipefail

echo 'Yapf ...'
yapf -i --recursive --style='{based_on_style: chromium}' app
yapf -i --recursive --style='{based_on_style: chromium}' tests

echo 'Pylint ...'
pylint --rcfile=".pylint.rc" app
pylint --rcfile=".pylint.rc" ./main.py

