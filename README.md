# Doit - Lab 1 - Telemetry Collector Specs

See [SPECS.md](SPECS.md) for information regarding the purpose of this Application Modernization lab execise.

# Pre-requisites

The following lab has been developed for execution on a MacOS. It should run on an EC2 instance the same pre-requites. It requires the following dependencies.

* [awscli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* A working AWS Profile (e.g. correctly configured ~/.aws/credentials)
** Applicable AWS IAM role and policies are not detailed here
* [jq](https://stedolan.github.io/jq/)
* [Python 3](https://python.org) I would recommend using [pyenv](https://github.com/pyenv/pyenv)
* curl

## Lab installed pre-requisites

During the lab the following products are installed with detailed instructions in each lesson
* [AWS Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
* [Locust](https://locust.io/)

# Step 1

Write an API to support the initial lab requirements. For this example we will use:

* [Python 3](https://www.python.org/).  
** Ideally we want 3.10 or 3.11, however AWS lambda only supports 3.9 😔
* [FastAPI](https://fastapi.tiangolo.com/)
* [Pydantic](https://docs.pydantic.dev/)

With just a few lines of code we can create an API that accepts the required JSON payload at the `/telementy` endpoint and validates the input matches the required specification.

Checkout [Lesson 1](lesson1/README.md) for step-by-step instructions.

This lesson completes:
* a RESTful API
* a POST /telemetry endpoint
** but it is not HTTPS
* A validated request payload
* Bonus: Self documented API specification

# Step 2

Deploy the API to a cloud serverless provider. In this case we are going to be using [AWS Lambda](https://aws.amazon.com/lambda/).

Checkout [Lesson 2](lesson2/README.md) for step-by-step instructions.

This lesson completes:
* Using a Cloud platform (AWS)
* a RESTful API
* HTTPS
* a POST /telemetry endpoint
* a validate request payload
* Serverless Implementation
* Reproducible (Version Control and README instructions)
* Bonus: Self documented API specification
