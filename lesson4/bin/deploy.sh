#!/usr/bin/env bash

readonly ENV_FILE=".envrc"

[ ! -s "${ENV_FILE}" ] && echo "Please cd to base directory containing '${ENV_FILE}'" && exit 1
source ${ENV_FILE}

sam build  # required to get requirements.txt packages

# See yet another different config file samconfig.toml
# No idea how to get dynamic parameter overrides into file
# CloudFormation Parameters cannot support '_'

sam deploy --parameter-overrides ParameterKey=SGID,ParameterValue=${SG_ID} ParameterKey=SUBNETIDS,ParameterValue="${SUBNET_IDS}" ParameterKey=INSTANCEENDPOINT,ParameterValue="${INSTANCE_ENDPOINT}" $* | tee deploy.log

URL=$(grep ^Value deploy.log | awk '{print $2}')
echo ${URL}

# Incase the URL entry was removed, make the following re-runable
[ $(grep -c "^URL" .envrc) -eq 0 ] && echo "URL=" >> .envrc

#Update URL in .envrc
sed -i -e 's@^URL=.*$@URL='"${URL}"'@' .envrc
