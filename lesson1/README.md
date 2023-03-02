# Lesson 1

## Setup a Python Virtual Environment

```
python -m venv .venv
source .venv/bin/activate
```

## Install needed Python Packages

```
cd src
pip install -r requirements.txt
```

## Launch our API in a webapp container

Show code to be executed
```
cat app/__init__.py
```

Run webcontainer
```
uvicorn app:app --reload
```

When running in an interactive window you will get logging to `stdout`
```
INFO:     Will watch for changes in these directories: ['/Users/ronald/git/doit-lab1/step1/src']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [24304] using StatReload
INFO:     Started server process [24306]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Test our webapp container

NOTE: Perform the following in a different session

```
curl -s http://127.0.0.1:8000 | jq .
```

Your response should be
```
{
  "detail": "Not Found"
}
```

And our container logs show
```
INFO:     127.0.0.1:52915 - "GET / HTTP/1.1" 404 Not Found
```

This confirms the container is running.

## Test our endpoint

```
ENDPOINT="http://127.0.0.1:8000/telemetry"
curl -s ${ENDPOINT} | jq .
```

Expected Output
```
{
  "detail": "Method Not Allowed"
}
```

And our container logs show
```
INFO:     127.0.0.1:52933 - "GET /telemetry HTTP/1.1" 405 Method Not Allowed
```

This confirms the endpoint exists but our HTTP method is invalid

## Test our endpoint as a POST

### Request
```
curl -s -X POST ${ENDPOINT} | jq .
```

### Response
```
{
  "detail": [
    {
      "loc": [
        "body"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}

### Container Logs
```
And our container logs show
```
INFO:     127.0.0.1:52935 - "POST /telemetry HTTP/1.1" 422 Unprocessable Entity
```

This confirms the POST endpoint exists and we are missing Payload

## Test our endpoint with a valid POST payload

```
PAYLOAD='{"timestamp": "2023-01-31T12:34:56.789Z", "device_id": "abc123","memory_usage": 0.45, "cpu_usage": 0.23}'
jq . <<< ${PAYLOAD}
curl -s -X POST -H "Content-Type: application/json" -d "${PAYLOAD}" ${ENDPOINT} | jq .
```

A successful response will return the JSON provided, for example.

```
{
  "timestamp": "2023-01-31T12:34:56.789000+00:00",
  "device_id": "abc123",
  "memory_usage": 0.45,
  "cpu_usage": 0.23
}
```

And a web log of
```
INFO:     127.0.0.1:52996 - "POST /telemetry HTTP/1.1" 200 OK
```

## Testing

You should always test your API endpoints. Here is an example of the original specification.

```
PAYLOAD='{"timestamp": "2023-01-31T12:34:56.789Z", "device_id": "abc123","memory_usage": 0.45, "cpu_usage": 0.23,}'
curl -s -X POST -H "Content-Type: application/json" -d "${PAYLOAD}" ${ENDPOINT} | jq .
```

And here is why this is invalid
```
{
  "detail": [
    {
      "loc": [
        "body",
        104
      ],
      "msg": "Expecting property name enclosed in double quotes: line 1 column 105 (char 104)",
      "type": "value_error.jsondecode",
      "ctx": {
        "msg": "Expecting property name enclosed in double quotes",
        "doc": "{\"timestamp\": \"2023-01-31T12:34:56.789Z\", \"device_id\": \"abc123\",\"memory_usage\": 0.45, \"cpu_usage\": 0.23,}",
        "pos": 104,
        "lineno": 1,
        "colno": 105
      }
    }
  ]
}
```

The purpose of this lesson is not to detail a test driven development (TDD) approach, however you can do manual testing to validate that the pydantic libraries are doing precisely what they are defined to do, i.e. data validation

```
PAYLOAD='{"timestamp": "2023-01-31T12:34:56.789Z", "device_id": "abc123","memory_usage": 0.45, "cpu_usage": 1.23}'
curl -s -X POST -H "Content-Type: application/json" -d "${PAYLOAD}" ${ENDPOINT} | jq .
```

And you would receive an applicable error and non 200 response.
```
{
  "detail": [
    {
      "loc": [
        "body",
        "cpu_usage"
      ],
      "msg": "ensure this value is less than or equal to 1.0",
      "type": "value_error.number.not_le",
      "ctx": {
        "limit_value": 1
      }
    }
  ]
}
```

## Bonsus

FastAPI offers a number of benefits, including self documenting APIs. Check out these pages http://localhost:8000/docs & http://localhost:8000/redoc

```
open http://localhost:8000/docs
open http://localhost:8000/redoc
```

This ends the lesson.
