# Lesson 2

## Setup a Python Virtual Environment

For this lesson we install different Python packages so we will use a dedicated virtual environment.

```
python -m venv .venv
source .venv/bin/activate
```

## Install needed Python Packages

```
cd src
pip install -r requirements.txt
```

## Install AWS Serverless Application Model

We will require the `sam` command to complete this lesson.  See https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

### MacOS
```
TMP_DIR=${TMP_DIR:-/tmp}
cd ${TMP_DIR}
wget https://github.com/aws/aws-sam-cli/releases/download/v1.73.0/aws-sam-cli-macos-arm64.pkg
sudo installer -pkg ${TMP_DIR}/aws-sam-cli-macos-arm64.pkg -target /
sam --version
```
### Linux
```
MP_DIR=${TMP_DIR:-/tmp}
cd ${TMP_DIR}
wget https://github.com/aws/aws-sam-cli/releases/download/v1.73.0/aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install
sam --version
```
SAM CLI, version 1.73.0
```

## Show code differences

To run our locally developed FastAPI code in Lambda we require the Python [Magnum](https://mangum.io/) library, an [ASGI](https://asgi.readthedocs.io/en/latest/) wrapper.

This show the change in lesson code.
```
diff -y app/__init__.py ../../lesson1/src/app/__init__.py
```

```
from fastapi import FastAPI	                          from fastapi import FastAPI
from mangum import Mangum	                        <
from pydantic import BaseModel, constr, confloat         from pydantic import BaseModel, constr, confloat
from datetime import datetime					              	from datetime import datetime

class Telemetry(BaseModel):						                class Telemetry(BaseModel):
    timestamp: datetime    	    			                      timestamp: datetime
    device_id: constr(min_length=1, max_length=100)			  device_id: constr(min_length=1, max_length=100)
    memory_usage: confloat(ge=0.0, le=1.0)				        memory_usage: confloat(ge=0.0, le=1.0)
    cpu_usage: confloat(ge=0.0, le=1.0)					          cpu_usage: confloat(ge=0.0, le=1.0)

app = FastAPI()							                        	app = FastAPI()

@app.post("/telemetry")						                   	@app.post("/telemetry")
async def post_telemetry_data(telemetry: Telemetry):			async def post_telemetry_data(telemetry: Telemetry):
    return telemetry							                        return telemetry
                                                  <
handler = Mangum(app, lifespan="off")             <
```

## Test our Lambda based webapp container

You can build and test locally before deploying to AWS lambda


```
sam build
```

```
Building codeuri: /Users/ronald/git/doit-lab1/lesson2/src runtime: python3.9 metadata: {} architecture: x86_64 functions: Function
Running PythonPipBuilder:ResolveDependencies
Running PythonPipBuilder:CopySource

Build Succeeded

Built Artifacts  : .aws-sam/build
Built Template   : .aws-sam/build/template.yaml

Commands you can use next
=========================
[*] Validate SAM template: sam validate
[*] Invoke Function: sam local invoke
[*] Test Function in the Cloud: sam sync --stack-name {{stack-name}} --watch
[*] Deploy: sam deploy --guided

SAM CLI update available (1.75.0); (1.73.0 installed)
To download: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html
```

```
sam local start-api
```

NOTE: If you do not have a local docker setup or have it running you will need it for this step.


```
Error: Running AWS SAM projects locally requires Docker. Have you got it installed and running?
```

```
$ docker --version
Docker version 20.10.21, build baeda1f
```

```
sam local start-api

Mounting Function at http://127.0.0.1:3000$default [X-AMAZON-APIGATEWAY-ANY-METHOD]
You can now browse to the above endpoints to invoke your functions. You do not need to restart/reload SAM CLI while working on your functions, changes will be reflected instantly/automatically. If you used sam build before running local commands, you will need to re-run sam build for the changes to be picked up. You only need to restart SAM CLI if you update your AWS SAM template
2023-03-02 09:52:37  * Running on http://127.0.0.1:3000/ (Press CTRL+C to quit)
```

## Testing the Serverless container locally

You can now repeat the steps in Lesson 1, however using port 3000 instead of 8000.

NOTE: Perform the following in a different session

```
URL="http://127.0.0.1:3000"
curl -s "${URL}" | jq .
ENDPOINT="${URL}/telemetry"
curl -s ${ENDPOINT} | jq .
curl -s -X POST ${ENDPOINT} | jq .
PAYLOAD='{"timestamp": "2023-01-31T12:34:56.789Z", "device_id": "abc123","memory_usage": 0.45, "cpu_usage": 0.23}'
jq . <<< ${PAYLOAD}
curl -s -X POST -H "Content-Type: application/json" -d "${PAYLOAD}" ${ENDPOINT} | jq .
PAYLOAD='{"timestamp": "2023-01-31T12:34:56.789Z", "device_id": "abc123","memory_usage": 0.45, "cpu_usage": 1.23}'
curl -s -X POST -H "Content-Type: application/json" -d "${PAYLOAD}" ${ENDPOINT} | jq .
```

NOTE: It's dead slow

This confirms the packaged container for our Lambda is validated.

## Deploy the Lambda Stack onto S3

To deploy this as a Lambda we require a top-level S3 bucket.

```
S3_BUCKET=${USER}-doit-lab1 # Must be top level bucket
[[ $(aws s3 ls s3://${S3_BUCKET} 2>/dev/null) -ne 0 ]] && aws s3 mb s3://${S3_BUCKET}
```

Deploy this to AWS.
```
STACK_NAME="DoitLab1onLambda"
sam deploy --stack-name "${STACK_NAME}" --s3-bucket ${S3_BUCKET} --capabilities CAPABILITY_IAM | tee deploy.log
URL=$(grep ^Value deploy.log | awk '{print $2}')
echo ${URL}
```

The full output of this is not shown here.
```
...
-------------------------------------------------------------------------------------------------
CloudFormation outputs from deployed stack
-------------------------------------------------------------------------------------------------
Outputs
-------------------------------------------------------------------------------------------------
Key                 ApiUrl
Description         URL of your API
Value               https://pke97y1ur1.execute-api.us-east-2.amazonaws.com/
-------------------------------------------------------------------------------------------------

Successfully created/updated stack - DoitLab1onLambda in us-east-2
```

## Testing on Lambda

We repeat the same steps we have done previously, with the adjusted HTTP url.

```
ENDPOINT="${URL}/telemetry"
curl -s ${ENDPOINT} | jq .
curl -s -X POST ${ENDPOINT} | jq .
PAYLOAD='{"timestamp": "2023-01-31T12:34:56.789Z", "device_id": "abc123","memory_usage": 0.45, "cpu_usage": 0.23}'
jq . <<< ${PAYLOAD}
curl -s -X POST -H "Content-Type: application/json" -d "${PAYLOAD}" ${ENDPOINT} | jq .
PAYLOAD='{"timestamp": "2023-01-31T12:34:56.789Z", "device_id": "abc123","memory_usage": 0.45, "cpu_usage": 1.23}'
curl -s -X POST -H "Content-Type: application/json" -d "${PAYLOAD}" ${ENDPOINT} | jq .
```



## Test Driven Development (TDD) Philosophy

Writing code is easy, writing good, clean and efficient code is harder.

While this lesson demonstrates how to complete the requirement we should use better practices, write diligent and clean code.

To simplify this lesson not all steps are validated above. However a good and diligent engineer should both write "repeatable/re-runable code" when possible, and you should "test and verify each dependency" as well as ensure you document and "cleanup" to be a cost concesious and responsible engineer.


Re-runable code. We test and apply only if required, this means this code is re-runable.
```
[[ $(aws s3 ls s3://${S3_BUCKET} 2>/dev/null) -ne 0 ]] && aws s3 mb s3://${S3_BUCKET}
```

This is an example as how we would test and verify the bucket does what it should before we actually use it.
```
TMP_DIR=${TMP_DIR:-/tmp}
TMP_FILE="${TMP_DIR}/test.$$"
touch ${TMP_FILE}
aws s3 cp ${TMP_FILE} s3://${S3_BUCKET}
aws s3 ls s3://${S3_BUCKET}
aws s3 rm s3://${S3_BUCKET}/$(basename ${TMP_FILE})
rm -f ${TMP_FILE}
```


## Cleanup

And this is how we would cleanup after our lab.

```
#export AWS_DEFAULT_REGION=us-east-2
sam delete --stack-name ${STACK_NAME} --no-prompts --region ${AWS_DEFAULT_REGION}

# Delete bucket
aws s3 rm s3://${S3_BUCKET}
```


This ends the lesson.
