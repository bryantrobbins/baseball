#!/usr/bin/python

import boto3
import json
import os
import time
import pyparsing

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from pyparsing import Word, alphas, ParseException

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

def parseExpression(expr):
    greet = Word( alphas ) + "," + Word( alphas ) + "!" # <-- grammar defined here
    try:
        parsed = greet.parseString(expr)
        return(True)
    except ParseException, e:
        print('Parse exception')
        return(False)

def errorOut(message):
    print(message)
    # TODO: Update db row to report error

print('Starting job')

# TODO: Set these through ECS task/container defs
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["JOB_TABLE"] = "baseball-jobs"
os.environ["JOB_QUEUE"] = "baseball-jobs-queue"

# Load vars
jobTable = os.environ['JOB_TABLE']
jobQueue = os.environ['JOB_QUEUE']

# Init clients
#dynamo = boto3.resource('dynamodb').Table(jobTable)
#queue = boto3.resource('sqs').get_queue_by_name(QueueName=jobQueue)
#
#while True:
#    messages = queue.receive_messages()
#    if (len(messages) == 0):
#        print('There are no messages; sleeping')
#        time.sleep(10)
#    else:
#        print('Processing {} messages'.format(len(messages)))
#        for message in messages:
#            jobInfo = extractSingleJob(message.body)
#            if jobInfo is not None:
#                # Call R
#                # Do upload
#                # Update DB entry
#                # Delete message
#                print('Doing the work')
jobInfo = '{ "colDefs": [ { "colName": "custom1", "expr": "Hello, World!"}, { "colName": "custom2", "expr": "Fuck, Me!" } ] }'
config = json.loads(jobInfo)
# Validate column definitions
for c in config['colDefs']:
    result = parseExpression(c['expr'])
    if ( not result ):
        errorOut('Expression for column {} does not parse. Please report this error (or at least stop trying to hack the backend).'.format(c['colName']))
# If we make it this far, we can start calling R
