#!/usr/bin/env bash

readonly ENV_FILE=".envrc"

[ ! -s "${ENV_FILE}" ] && echo "Please cd to base directory containing '${ENV_FILE}'" && exit 1
source ${ENV_FILE}

[[ $(aws s3 ls s3://${S3_BUCKET} 2>&1 >/dev/null) -ne 0 ]] && aws s3 mb s3://${S3_BUCKET}

