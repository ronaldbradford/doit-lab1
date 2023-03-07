# Telemetry Collector Specs

- Complete this lab before the March Breakroom session (Date TBD)
- Group work is welcome (divide-and-conquer)

## Requirements
- Any cloud platform
- Public REST API to accept HTTPS POST requests
- Request body as defined below (see curl example)
- Reproducible deployment (you might need this project in other Lab)

# Objective
- Accept POST requests with JSON payload (below)
- Persist the data
- Data should be ready for analytics within 15 seconds (data freshness)
- Run analytics to answer the following questions:
  - Number of requests per device id
  - Bucketed number of requests per device id (num/req per minute per device)
  - AVG and MAX CPU for a given time period (time period is input)
  - AVG and MAX Memory for a given time period (time period is input)
# Bonus
* Authentication
* Dashboard (Graphs or UI to view the analytics)
* Optimizations
** Handle an avg 1k rps with peaks of 5k rps
** Low latency (response and e2e)
** Global audience
** Cost reduction
** Mission critical data


Your function should accept curl requests as below:
```
curl -X POST -H "Content-Type: application/json" -d '{
  "timestamp": "2023-01-31T12:34:56.789Z",
  "device_id": "abc123",
  "memory_usage": 0.45,
  "cpu_usage": 0.23
}' "https://example.com/telemetry"
```


Payload details ([JSON Schema Ref](http://json-schema.org/understanding-json-schema/reference/index.html)):

```
{
  "timestamp": "2023-01-31T12:34:56.789Z", // RFC3339 UTC
  "device_id": "abc123", // STRING < 100 characters
  "memory_usage": 0.45, // NUMBER between 0 <= X <= 1
  "cpu_usage": 0.23 // NUMBER between 0 <= X <= 1
}
```

* timestamp: RFC3339 UTC
* device_id: STRING < 100 characters
* memory_usage: NUMBER between 0 <= X <= 1
* cpu_usage: NUMBER between 0 <= X <= 1

Note: [Sanitize and validate your inputs!](https://www.explainxkcd.com/wiki/index.php/Little_Bobby_Tables)


Source: https://docs.google.com/document/d/1tsFFqSYDCi6v0MZ3_uo_igIAKAmRxyNLo1t40EfXA50/edit#
