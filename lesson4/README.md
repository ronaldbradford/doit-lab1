# Lesson 4

**<span style="color:red">NOTE: This lesson is a WIP, see TODOs</span>**

## Setup a Python Virtual Environment

For this lesson we install different Python packages so we will use a dedicated virtual environment.

```
python -m venv .venv
source .venv/bin/activate
```

* <span style="color:red">TODO mysql-connector-python failed, reverted to pymysql (AWS lambda examples)</span>

## Install needed Python Packages

```
pip install -r src/requirements.txt
```

## Create an Aurora MySQL Cluster

We will start with using an RDS MySQL RDBMS due to comfort level and simplicity. The following references can help you create this resource.

- [Creating an Amazon Aurora DB cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.CreateInstance.html) (amazon.com)
- [AWS CLI Tutorials](https://github.com/ronaldbradford/aws-tutorial) - Fully cut/paste ready (github.com/ronaldbradford)

After understanding the attributes and steps of an RDS Cluster, internally you can request repo access to these [RDS one-liners](https://doitintl.atlassian.net/wiki/spaces/CRE/pages/160989240/Data+Environment+Customer+Emulation) under development in my personal focus time.

```
. rds-functions
create-mysql-cluster
sql
```

* <span style="color:red">TODO Launch a Serverless cluster, not a normal cluster</span>



## Deploy Tables and User permissions

* <span style="color:red">TODO We have hardcoded schema/user/password that should be parameterized for productization into template.yaml</span>
* <span style="color:red">ideally in a AWS secret</span>

```
cd sql/aurora-mysql

mysql> source 01-schema.sql
mysql> source 02-tables.sql
mysql> source 03-user.sql
```

## Parameterization

The following deployment scripts use a per environment customizable `.envrc` which include certain values specific to your individual AWS Account.

See [Create Security Group for RDS Aurora](https://github.com/ronaldbradford/aws-tutorial/blob/main/ec2/create-rds-security-group.md) for AWS CLI statements to create the EC2 security group (which you would have done when creating the cluster)

* <span style="color:red">TODO This should be refactored in CloudFormation template.</span>

You can obtain these values with the `aws` cli.

```
VPC_ID=$(aws ec2 describe-vpcs --query '*[0].VpcId' --output text)
SUBNET_IDS=$(aws ec2 describe-subnets --filters Name=vpc-id,Values=${VPC_ID} | jq -r '.Subnets[].SubnetId' | tr '\n' ',' | sed -e "s/,\$"//)
SG_NAME="rds-aurora-sg"
SG_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values=${SG_NAME} --query '*[].GroupId' --output text)
echo ${VPC_ID},${SG_NAME},${SG_ID},${SUBNET_IDS}
```

For example:

```
vpc-0a03225585506c531,rds-aurora-sg,sg-03a3319858d105443,"subnet-08e92295ef7d56f04","subnet-01974903db219cd60","subnet-0198174dd811f621d"
```

Update accordingly

```
vi .envrc
```

## Deploy the Lambda Stack onto S3 (From Lesson 2)

To deploy this as a Lambda we require a top-level S3 bucket.

```
bin/setup.sh
```

### VPC Connectivity

By default a Lambda function is not associated to your VPC. This was not an issue in prior lessons.
You need to add a `VpcConfig` to your CloudFormation template.

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

### Number of devices

```
SELECT COUNT(DISTINCT device_id) AS total_devices
FROM telemetry;
```

```
+---------------+
| total_devices |
+---------------+
|          1846 |
+---------------+
```

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

### Metrics of devices with most data points

We delete some random samples, hoping that this throws the avg/max off.

```
DELETE FROM telemetry WHERE MOD(id,155) IN (0,42,99) and id > 0;
```

This is the top devices metrics for a given time period
```
SELECT device_id,
       COUNT(*) AS data_points,
       FORMAT(min(data->>'$.cpu_usage'),2) AS min_cpu,
       FORMAT(avg(data->>'$.cpu_usage'),2) AS avg_cpu,
       FORMAT(max(data->>'$.cpu_usage'),2) AS max_cpu,
       FORMAT(min(data->>'$.memory_usage'),2) AS min_memory,
       FORMAT(avg(data->>'$.memory_usage'),2) AS avg_memory,
       FORMAT(max(data->>'$.memory_usage'),2) AS max_memory,
       MAX(entry_ts) AS latest_ts
FROM telemetry
WHERE entry_ts > '2023-03-08 17:04:50'
GROUP BY device_id
ORDER BY 2 DESC
LIMIT 10
```

Example list of devices with top data points.

```
+-----------+-------------+---------+---------+---------+------------+------------+------------+---------------------+
| device_id | data_points | min_cpu | avg_cpu | max_cpu | min_memory | avg_memory | max_memory | latest_ts           |
+-----------+-------------+---------+---------+---------+------------+------------+------------+---------------------+
| abc119    |         864 | 0.10    | 0.41    | 0.89    | 0.00       | 0.21       | 0.89       | 2023-03-08 17:21:12 |
| abc140    |         857 | 0.09    | 0.44    | 0.99    | 0.00       | 0.22       | 1.00       | 2023-03-08 17:21:12 |
| abc114    |         852 | 0.10    | 0.42    | 0.97    | 0.00       | 0.21       | 0.99       | 2023-03-08 17:21:12 |
| abc147    |         851 | 0.10    | 0.46    | 1.00    | 0.00       | 0.24       | 0.97       | 2023-03-08 17:21:12 |
| abc130    |         846 | 0.11    | 0.43    | 0.94    | 0.00       | 0.21       | 0.93       | 2023-03-08 17:21:12 |
| abc120    |         837 | 0.11    | 0.42    | 0.92    | 0.00       | 0.21       | 0.89       | 2023-03-08 17:21:12 |
| abc121    |         835 | 0.12    | 0.43    | 0.98    | 0.00       | 0.21       | 0.00       | 2023-03-08 17:21:11 |
| abc151    |         831 | 0.10    | 0.44    | 1.00    | 0.00       | 0.23       | 0.99       | 2023-03-08 17:21:12 |
| abc131    |         829 | 0.10    | 0.43    | 0.99    | 0.00       | 0.21       | 0.97       | 2023-03-08 17:21:12 |
| abc155    |         826 | 0.09    | 0.44    | 0.99    | 0.00       | 0.22       | 0.88       | 2023-03-08 17:21:12 |
+-----------+-------------+---------+---------+---------+------------+------------+------------+---------------------+
10 rows in set (8.83 sec)
```

## Interactive Dashboard


```
watch --differences -n 0.5 ./status
```

status
```
mysql -u$DBA_USER -p$DBA_PASSWD -h${INSTANCE_ENDPOINT} lab1 < status.sql 2>&1 | grep -v Warning | column -t
```

status.sql

```
SELECT COUNT(*) AS entries, COUNT(DISTINCT device_id) AS unique_devices FROM telemetry;
SELECT device_id,
       COUNT(*) AS data_points,
       FORMAT(min(data->>'$.cpu_usage'),2) AS min_cpu,
       FORMAT(avg(data->>'$.cpu_usage'),2) AS avg_cpu,
       FORMAT(max(data->>'$.cpu_usage'),2) AS max_cpu,
       FORMAT(min(data->>'$.memory_usage'),2) AS min_memory,
       FORMAT(avg(data->>'$.memory_usage'),2) AS avg_memory,
       FORMAT(max(data->>'$.memory_usage'),2) AS max_memory,
       MAX(entry_ts) AS latest_ts
FROM telemetry
GROUP BY device_id
ORDER BY 2 DESC
LIMIT 10
```

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
