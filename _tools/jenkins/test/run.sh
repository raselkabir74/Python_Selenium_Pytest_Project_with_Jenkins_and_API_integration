#!/bin/bash
# shellcheck shell=bash

# private staging area to run the tests on
SUFFIX="$1"
UI_TEST_RUN="$2"
MODULES_TO_TEST="$3"

if [[ -z "$SUFFIX" ]] ; then
  SUFFIX="-qa-testing"
fi

CFG_OVERRIDE_FILE="local_generated.ini"
echo "[credential]" > "$CFG_OVERRIDE_FILE"
echo "url = https://dsp$SUFFIX.eskimi.com" >> "$CFG_OVERRIDE_FILE"

#rm -R downloads
#mkdir -m 777 -p downloads
pkill chrome
pkill chromium-browser
pkill chromium

rm -R reports_screenshot
rm -R report-screenshot-zip

#CON_NAME=$(docker ps --format "{{.Names}}, {{.Ports}}" | grep "4444")
#CONTAINER_NAME=$(echo "$CON_NAME" | cut -d ',' -f 1)
#echo "$CONTAINER_NAME"
#docker stop "$CONTAINER_NAME"
#docker rm "$CONTAINER_NAME"
#docker pull selenium/standalone-chrome
#docker run -d -p 4444:4444 --name selenium-new -v "$(pwd)/downloads:/home/seluser/downloads" selenium/standalone-chrome:latest
#CHROME_DRIVER=$(docker exec selenium-new chromedriver --version)
CHROME_DRIVER=$(chromedriver --version)
echo "Chrome driver version: $CHROME_DRIVER"
echo "Suffix: $SUFFIX"

if [ "$UI_TEST_RUN" = true ]; then
  echo "Modules to test: $MODULES_TO_TEST"
else
  echo "Modules to test: ALL_MODULES"
fi

TEST_DIRS_FORMATTED=$(echo "$MODULES_TO_TEST" | tr ',' ' ' | xargs)
pytest_command="python -m pytest"
for dir in $TEST_DIRS_FORMATTED; do
  if [ "$dir" != "ALL_MODULES" ]; then
    pytest_command+=" tests/$dir"
  fi
done

pytest_command+=" -s --verbose --dist=loadfile --durations=0 -vv -n 4 --reruns 2 --reruns-delay 5 --timeout=1500 --color=yes --junitxml=test_results.xml"

echo "$pytest_command"

if [ "$UI_TEST_RUN" = true ]; then
  python -m pytest tests/REGRESSION/test_prerequisite_test_case.py::test_regression_prerequisite_and_delete_io -s --verbose --durations=0 -vv -n 1 --reruns 1 --reruns-delay 5 --timeout=1500

  if [[ "$MODULES_TO_TEST" == *"ALL_MODULES"* ]] && [[ "$SUFFIX" != "-qa-testing" ]]; then
    python -m pytest -s --verbose --dist=loadfile --durations=0 -vv -n 4 --reruns 2 --reruns-delay 5 --timeout=1500 --color=yes --junitxml=test_results.xml
  elif [[ "$MODULES_TO_TEST" == *"ALL_MODULES"* ]] && [[ "$SUFFIX" == "-qa-testing" ]]; then
    python -m pytest tests/REGRESSION -s --verbose --dist=loadfile --durations=0 -vv -n 4 --reruns 1 --reruns-delay 5 --timeout=1500 --color=yes --junitxml=test_results.xml
  else
    eval "$pytest_command"
  fi
else
  python -m pytest tests/REGRESSION/test_prerequisite_test_case.py::test_regression_prerequisite_and_delete_io -s --verbose --durations=0 -vv -n 1 --reruns 1 --reruns-delay 5 --timeout=1500
  if [[ "$SUFFIX" == "-qa-testing" ]]; then
    python -m pytest tests/REGRESSION -s --verbose --dist=loadfile --durations=0 -vv -n 4 --reruns 1 --reruns-delay 5 --timeout=1500 --color=yes --junitxml=test_results.xml
  else
    python -m pytest -s --verbose --dist=loadfile --durations=0 -vv -n 4 --reruns 2 --reruns-delay 5 --timeout=1500 --color=yes --junitxml=test_results.xml
  fi
fi

python _tools/jenkins/test/upload.py

rm -f "$CFG_OVERRIDE_FILE"
rm -R report-screenshot-zip
rm -R reports_screenshot
if [ -d "downloads" ]; then
    rm -R downloads
fi
