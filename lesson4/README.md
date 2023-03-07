# Lesson 4

## Setup a Python Virtual Environment

For this lesson we install different Python packages so we will use a dedicated virtual environment.

```
python -m venv .venv
source .venv/bin/activate
```

//TODO mysql-connector-python failed, reverted to pymysql (AWS lambda examples)

## Install needed Python Packages

```
cd src
pip install -r requirements.txt
```

## Create an Aurora MySQL Cluster

//TODO Serverless

```
. rds-functions
create-mysql-cluster
sql
```
For access to these [RDS one-liners](https://doitintl.atlassian.net/wiki/spaces/CRE/pages/160989240/Data+Environment+Customer+Emulation) ask for repo access.


## Deploy Tables and User permissions

```
cd sql/aurora-mysql

mysql> source 01-schema.sql
mysql> source 02-tables.sql
mysql> source 03-user.sql
```



## Deploy the Lambda Stack onto S3 (From Lesson 2)

To deploy this as a Lambda we require a top-level S3 bucket.

```
S3_BUCKET=${USER}-doit-lab1 # Must be top level bucket
[[ $(aws s3 ls s3://${S3_BUCKET} 2>&1 >/dev/null) -ne 0 ]] && aws s3 mb s3://${S3_BUCKET}
```

Deploy this to AWS  (From Lesson 2)
```
STACK_NAME="DoitLab1onLambda"
sam build
sam deploy --stack-name "${STACK_NAME}" --s3-bucket ${S3_BUCKET} --capabilities CAPABILITY_IAM | tee deploy.log
URL=$(grep ^Value deploy.log | awk '{print $2}')
echo ${URL}
```

//TODO I'm unsure if build is part of deploy?

## Connectivity

By default the Lambda is not associated to your VPC.

//TODO redo my lambda to be added to VPC programmatically  

## Testing on Lambda

We repeat the same steps as in prior lessons with the deployed Lambda HTTP url.

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

If you have issues, you can also deploy locally on an EC2 instance (See [Lesson 2](../lesson2/README.md)).  AWS Cloudwatch will also have detailed logs of lambda executions.

## Load Testing

Use [Lesson 3](../lesson3/README.md) to send traffic to your endpoint that persists data to AWS Aurora MySQL.

## Analytics


### Number of requests per device id

```
SELECT device_id, COUNT(*) AS requests
FROM telemetry
GROUP BY device_id
ORDER BY 2 DESC
LIMIT 10;
```

```
+-----------+----------+
| device_id | requests |
+-----------+----------+
| abc41     |      852 |
| abc58     |      850 |
| abc24     |      850 |
| abc79     |      844 |
| abc93     |      843 |
| abc38     |      840 |
| abc27     |      839 |
| abc96     |      839 |
| abc67     |      839 |
| abc46     |      838 |
+-----------+----------+
```

### AVG and MAX CPU for a given time period (time period is input)


```
SELECT COUNT(*) AS data_points,
       FORMAT(avg(data->>'$.cpu_usage'),2) AS avg_cpu,
       FORMAT(max(data->>'$.cpu_usage'),2) as max_cpu
FROM telemetry;
```

```
+-------------+---------+---------+
| data_points | avg_cpu | max_cpu |
+-------------+---------+---------+
|       79151 | 0.50    | 1.0     |
+-------------+---------+---------+
1 row in set (0.12 sec)
```

\\TODO I guess I need a better numpy randomization



## Cleanup

And this is how we would cleanup after our lab.

```
cd ~/config/aurora-mysql-<name>
delete-aurora-cluster
```

```
#export AWS_DEFAULT_REGION=us-east-2
sam delete --stack-name ${STACK_NAME} --no-prompts --region ${AWS_DEFAULT_REGION}

# Delete bucket
aws s3 rm s3://${S3_BUCKET}
```


This ends the lesson.
