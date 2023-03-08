#!/usr/bin/env bash

#
# Simple script to run a few validation checks for new API endpoint
#
echo "Checking required ENV variables"
[ -z "${URL}" ] && echo "ERROR: Correctly export URL" && exit 1

echo "Checking required dependencies"
[[ ! $(type -P jq) ]] && echo "ERROR: jq is not installed" && exit 1
[[ ! $(type -P curl) ]] && echo "ERROR: curl is not installed" && exit 1


ENDPOINT="${URL}/telemetry"
echo "Pinging Endpoint (should fail)"
curl -s "${ENDPOINT}" | jq .
echo "Pinging Endpoint as a POST (should fail)"
curl -s -X POST "${ENDPOINT}" | jq .
INVALID_PAYLOAD='{"timestamp": "2023-01-31T12:34:56.789Z", "device_id": "abc123","memory_usage": 0.45, "cpu_usage": 1.23}'
echo "Submitting to invalid data (should fail)"
curl -s -X POST -H "Content-Type: application/json" -d "${INVALID_PAYLOAD}" "${ENDPOINT}" | jq -r .
PAYLOAD='{"timestamp": "2023-01-31T12:34:56.789Z", "device_id": "abc123","memory_usage": 0.45, "cpu_usage": 0.23}'
jq . <<< "${PAYLOAD}"
echo "Submitting valid data (should return success)"
curl -s -X POST -H "Content-Type: application/json" -d "${PAYLOAD}" "${ENDPOINT}" | jq -r .

