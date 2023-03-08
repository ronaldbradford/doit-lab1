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
