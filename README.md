# Doit - Lab 1 - Telemetry Collector Specs

See [SPECS.md](SPECS.md) for information regarding this lab.

# Step 1

Write an API to support the requirements. For this example we will use:

* [Python 3](https://www.python.org/).  
** Ideally we want 3.10 or 3.11, however AWS lambda only supports 3.9 😔
* [FastAPI](https://fastapi.tiangolo.com/)
* [Pydantic](https://docs.pydantic.dev/)

With just a few lines of code we can create an API that accepts the required JSON payload at the `/telementy` endpoint and validates the input specification.

Checkout [Lesson 1](lesson1/README.md) for step-by-step instructions.

This lesson completes:
* an RESTful API
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
* Serverless
* Reproducible (Version Control and README instructions)
* Bonus: Self documented API specification
