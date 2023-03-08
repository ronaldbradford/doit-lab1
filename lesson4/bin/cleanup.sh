#!/usr/bin/env bash

. .envrc

# Remove Lambda stack deployed with `sam`
sam delete --stack-name ${STACK_NAME} --no-prompts --region ${AWS_DEFAULT_REGION}
rm -rf .aws-sam

# Delete bucket
aws s3 rm s3://${S3_BUCKET}
