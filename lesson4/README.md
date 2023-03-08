# Lesson 4

// NOTE: This lesson is a WIP, see TODOs

## Setup a Python Virtual Environment

For this lesson we install different Python packages so we will use a dedicated virtual environment.

```
python -m venv .venv
source .venv/bin/activate
```

//TODO mysql-connector-python failed, reverted to pymysql (AWS lambda examples)

## Install needed Python Packages

```
pip install -r src/requirements.txt
```

## Create an Aurora MySQL Cluster


```
. rds-functions
create-mysql-cluster
sql
```
//TODO Launch a Serverless cluster, not a normal cluster

For access to these [RDS one-liners](https://doitintl.atlassian.net/wiki/spaces/CRE/pages/160989240/Data+Environment+Customer+Emulation) ask for repo access.


## Deploy Tables and User permissions

//TODO We have hardcoded schema/user/password that should be parameterized for productization into template.yaml
//     ideally in a AWS secret

```
cd sql/aurora-mysql

mysql> source 01-schema.sql
mysql> source 02-tables.sql
mysql> source 03-user.sql
```

## Deploy the Lambda Stack onto S3 (From Lesson 2)

To deploy this as a Lambda we require a top-level S3 bucket.

```
. .envrc   # future direnv handling
[[ $(aws s3 ls s3://${S3_BUCKET} 2>&1 >/dev/null) -ne 0 ]] && aws s3 mb s3://${S3_BUCKET}
```

### VPC Connectivity

By default the Lambda is not associated to your VPC. You need to add a `VpcConfig` to your CloudFormation template.

//TODO redo template.yaml to parameterized VPC contents

Deploy this to AWS  (Same as from Lesson 2)

```
source bin/deploy.sh
```

## Testing on Lambda

We repeat the same steps as in prior lessons with the deployed Lambda HTTP url.

```
bin/validate-endpoint.sh
```

If you have issues, you can also deploy locally on an EC2 instance (See [Lesson 2](../lesson2/README.md)).
AWS Cloudwatch will also have detailed logs of lambda executions.

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

//TODO I guess I need a better numpy randomization777



## Cleanup

And this is how we would cleanup after our lab.

```
bin/cleanup.sh
```

```
. rds-functions
cd ~/config/aurora-mysql-<name>
delete-aurora-cluster
```

This ends the lesson.
