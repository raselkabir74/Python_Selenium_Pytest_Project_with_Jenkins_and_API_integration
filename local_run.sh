#!/bin/bash
# shellcheck shell=bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Set variables
PATH_TO_TEST="tests/CREATIVE/test_creatives.py"
TEST_CASE_NAME="test_dashboard_creative_copy_creative_to_another_user_banner"

# Kill any running Chrome instances
pkill chrome

# Remove previous screenshot reports
rm -rf reports_screenshot

# Run tests with pytest
if [ "$TEST_CASE_NAME" = "" ] && [ "$PATH_TO_TEST" != "" ]; then
  python -m pytest "$PATH_TO_TEST" -s --verbose --dist=loadfile --durations=0 -vv -n 4 --reruns 1 --reruns-delay 5 --timeout=1500
elif [ "$TEST_CASE_NAME" = "" ] && [ "$PATH_TO_TEST" = "" ]; then
  python -m pytest -s --verbose --dist=loadfile --durations=0 -vv -n 4 --reruns 1 --reruns-delay 5 --timeout=1500
else
  python -m pytest "$PATH_TO_TEST"::"$TEST_CASE_NAME" -s --verbose
fi