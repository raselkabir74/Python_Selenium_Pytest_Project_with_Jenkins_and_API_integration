#!/bin/bash
# shellcheck shell=bash

pylint --generate-rcfile > .pylintrc
pylint --rcfile=.pylintrc $(find . -iname "*.py" -print) -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint-report.txt || exit 0