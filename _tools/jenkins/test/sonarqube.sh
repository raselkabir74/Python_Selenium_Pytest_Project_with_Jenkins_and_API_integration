#!/bin/bash
# shellcheck shell=bash

# Report to sonarqube
if [[ "${BRANCH_NAME}" == "master" ]]; then
  sh "${SONAR_SCANNER_HOME}/bin/sonar-scanner"
else
  sh "${SONAR_SCANNER_HOME}/bin/sonar-scanner" \
    -Dsonar.pullrequest.branch=${BRANCH_NAME} \
    -Dsonar.pullrequest.key=${CHANGE_ID} \
    -Dsonar.pullrequest.bitbucketserver.headSha=${GIT_COMMIT}
fi