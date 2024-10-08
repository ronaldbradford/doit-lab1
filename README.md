# Doit - Lab 1 - Telemetry Collector Specs

See [SPECS.md](SPECS.md) for information regarding the purpose of this Application Modernization lab exercise.

# Pre-requisites

The following lab steps have been developed for execution on a MacOS. They should also run on an AWS EC2 instance with the same pre-requisites dependencies.

- [awscli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- A working AWS profile (e.g. correctly configured `~/.aws/credentials`)
   - Applicable AWS IAM role and policies are not detailed here
- [jq](https://stedolan.github.io/jq/)
- [Python 3](https://python.org) I would recommend using [pyenv](https://github.com/pyenv/pyenv)
- curl

## Lab installed pre-requisites

During the lab the following products are installed with detailed instructions in the applicable lesson
- [AWS Serverless Application Model (sam)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- [Locust](https://locust.io/)

# Step 1

Write an API to support the initial lab requirements. For this example we will use:

- [Python 3](https://www.python.org/).
  - Ideally we want 3.10 or 3.11, however AWS lambda only supports 3.9 😔
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
  - 3.10 features are not possible

With just a few lines of code we can create an API that accepts the required JSON payload at the `/telemetry` endpoint and validates that the input matches the required validation specification.

Checkout [Lesson 1](lesson1/README.md) for step-by-step instructions.

This lesson completes the initial [SPECS.md](SPECS.md) points:
- a RESTful API
- a POST /telemetry endpoint
  - but it is not HTTPS
- A validated request payload
- Bonus: Self documented API specification

# Step 2

Deploy the API to a cloud serverless provider. In this case we are going to be using [AWS Lambda](https://aws.amazon.com/lambda/).

Checkout [Lesson 2](lesson2/README.md) for step-by-step instructions.

This lesson completes the initial [SPECS.md](SPECS.md) points:
- Using a Cloud platform (AWS)
- a RESTful API
- HTTPS
- a POST /telemetry endpoint
- a validated request payload
- Serverless Implementation
- Reproducible (Version Control and README instructions)
- **Bonus**: Self documented API specification


# Step 3

Using the deployed serverless application from Lesson 2 we can perform load testing of the API endpoint.

Checkout [Lesson 3](lesson3/README.md) for step-by-step instructions.

In addition to the prior lessons completed [SPECS.md](SPECS.md) points.
* Handle 1k rps
* Maybe low latency (data is not yet persisted)

# Step 4 - RDS Aurora

We must now decide how to persist the data per API call. This is the more traditional 'n' tier architecture approach of inserting the data, whereas streaming the collected data to a producer (aka Kinesis or MKS) would enable different applications to consume the data anyway they like.  To evaluate the potential options, we will consider the traditional RDBMS database approach first, just because this is safe.

The overall objective of this lab is to use Serverless technologies when possible to reduce cost.
The lab also has specific analytic queries as part of the initial requirements which leads towards a SQL based solution.  Possible AWS options for storage using serverless compute may include:

* RDS Aurora serverless RDBMS
* Redshift Serverless data warehouse
* Amazon Timesteam - serverless time-stream database
* DynamoDB key-value store (we discount this as it will not provide the analytics functionality)


Checkout [Lesson 4](lesson4/README.md) for step-by-step instructions.

In addition to the prior lessons completed [SPECS.md](SPECS.md) points.
* Persist the data
* Demonstrate Analytics via SQL

# Next Steps

There are many improvements that can be made, however time while providing customer support is limiting. Some points would include:

- Secure the endpoint. This is a HttpApi endpoint `AWS::Serverless::HttpAp`, whereas a RestApi offers additional benefits. More information
  - https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html
  - https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-setup-api-key-with-console.html
- Provide an admin view summary data endpoint. The first iteration would be to provide a summary of the workload as demonstrated by the backend `watch` command.  A second iteration would enable parameters such as to/from dates.
- Use a better optimized persistent store.  Redshift would likely be a more ideal solution.
- Review the original [SPECS.md](SPECS.md) for goals of this lab.
- Review Lambda and API Gatway configuration for optimizations, only the defaults are used.
