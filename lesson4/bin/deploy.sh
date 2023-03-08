#!/usr/bin/env bash

. .envrc

sam build  # required to get requirements.txt packages
sam deploy --stack-name "${STACK_NAME}" --s3-bucket ${S3_BUCKET} --capabilities CAPABILITY_IAM | tee deploy.log
URL=$(grep ^Value deploy.log | awk '{print $2}')
echo ${URL}
export URL
