# Doit - Lab 1 - Telemetry Collector Specs

See [SPECS.md](SPECS.md) for information regarding this lab.

# Step 1

Write an API to support the requirements.

* [Python 3](https://www.python.org/).  
** Ideally we want 3.10 or 3.11, however AWS lambda only supports 3.9 😔
* [FastAPI](https://fastapi.tiangolo.com/)
* [Pydantic](https://docs.pydantic.dev/)

With just a few lines of code we can create an API that accepts the required JSON payload at the `/telementy` endpoint and validates the input.

Checkout [Lesson 1](lesson1/README.md)

NOTE: This ticks of an REST API endpoint with a POST /telemetry, but it is not HTTPS.
