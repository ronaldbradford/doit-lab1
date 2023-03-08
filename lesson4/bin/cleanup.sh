#!/usr/bin/env bash

readonly ENV_FILE=".envrc"

[ ! -s "${ENV_FILE}" ] && echo "Please cd to base directory containing '${ENV_FILE}'" && exit 1
source ${ENV_FILE}

# Remove Lambda stack deployed with `sam`
sam delete --stack-name ${STACK_NAME} --no-prompts --region ${AWS_DEFAULT_REGION}
rm -rf .aws-sam

# Delete bucket
aws s3 rm s3://${S3_BUCKET}
