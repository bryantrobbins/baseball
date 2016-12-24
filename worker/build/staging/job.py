#!/usr/bin/python

import boto3
import json
import os
import time
import scipy as sp
import rpy2.robjects as ro

from numpy import *
from pandas import *
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def extractSingleJob(jobId):
    print('Processing job {}'.format(jobId))
    try:
        response = dynamo.get_item(
            Key={
                'job-id': jobId
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
    else:
        item = response['Item']
        return item

print('Starting job')

# Needed for R <-> Python conversions
pandas2ri.activate()

# TODO: Set these through ECS task/container defs
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["JOB_TABLE"] = "baseball-jobs"
os.environ["JOB_QUEUE"] = "baseball-jobs-queue"

# Load vars
jobTable = os.environ['JOB_TABLE']
jobQueue = os.environ['JOB_QUEUE']

# Init clients
dynamo = boto3.resource('dynamodb').Table(jobTable)
queue = boto3.resource('sqs').get_queue_by_name(QueueName=jobQueue)

while True:
    messages = queue.receive_messages()
    if (len(messages) == 0):
        print('There are no messages; sleeping')
        time.sleep(10)
    else:
        print('Processing {} messages'.format(len(messages)))
        for message in messages:
            jobInfo = extractSingleJob(message.body)
            if jobInfo is not None:
                # Call R
                # Do upload
                # Update DB entry
                # Delete message
                print('Doing the work')
