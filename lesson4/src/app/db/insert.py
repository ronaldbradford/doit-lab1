""" [Inefficient] example of a MySQL database insert of telemetry data """
import json
import os
import pymysql
from .. import models

dba_user = os.getenv('DBA_USER')
dba_passwd = os.getenv('DBA_PASSWD')
instance_endpoint = host = os.getenv('INSTANCE_ENDPOINT')
schema = os.getenv('DATABASE')


def insert(data):
    """ Insert the provided telemetry data into MySQL table """
    #dba_user = 'api'
    #dba_passwd = 'Doit#Lab1@2023'
    #instance_endpoint = 'aurora-mysql-bb-0.c4s5ds0rk545.us-east-2.rds.amazonaws.com'
    #schema = 'lab1'

    try:
        conn = pymysql.connect(user = dba_user,
                               password = dba_passwd,
                               host = instance_endpoint,
                               database = schema)
    except pymysql.MySQLError:
        return models.Status(success=False, error="Unable to get connection")

    try:
        cursor = conn.cursor()
        stmt = f"INSERT INTO telemetry (data) VALUES ('{json.dumps(data)}')"
        cursor.execute(stmt, data)
        conn.commit()
    except pymysql.MySQLError:
        return models.Status(success=False,  error="Insert Failed")

    try:
        cursor.close()
        conn.close()
    except pymysql.MySQLError:
        pass

    return models.Status(success=True)
