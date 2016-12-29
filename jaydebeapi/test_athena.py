#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Downloading the Athena JDBC Driver
# https://s3.amazonaws.com/athena-downloads/drivers/AthenaJDBC41-1.0.0.jar
#
# OSX require legacy Java 6 runtime
# https://support.apple.com/kb/DL1572
from __future__ import print_function

import jaydebeapi


REGION = 'us-west-2'
CONNECTION_STRING = 'jdbc:awsathena://athena.{region}.amazonaws.com:443/'.format(region=REGION)
DRIVER_CLASS_NAME = 'com.amazonaws.athena.jdbc.AthenaDriver'
JAR_PATH = './lib/AthenaJDBC41-1.0.0.jar'

AWS_ACCESS_KEY = 'YOUR_ACCESS_KEY'
AWS_SECRET_ACCESS_KEY = 'YOUR_SECRET_ACCESS_KEY'
S3_STAGING_DIR = 's3://YOUR_S3_BUCKET/'


def main():
    conn = jaydebeapi.connect(DRIVER_CLASS_NAME,
                              [
                                  CONNECTION_STRING,
                                  {
                                      'user': AWS_ACCESS_KEY,
                                      'password': AWS_SECRET_ACCESS_KEY,
                                      's3_staging_dir': S3_STAGING_DIR
                                  }
                              ], JAR_PATH,)
    curs = conn.cursor()
    curs.execute("""
    SELECT table_schema, table_name, column_name
    FROM information_schema.columns
    WHERE table_schema NOT IN ('pg_catalog', 'information_schema');
    """.strip())
    print(curs.fetchall())
    curs.close()
    conn.close()


if __name__ == '__main__':
    main()
