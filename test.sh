#!/bin/bash

set -eo pipefail

yapf -i --recursive --style='{based_on_style: chromium}' app
pylint --rcfile=".pylint.rc" app
pytest
