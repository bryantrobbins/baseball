from __future__ import print_function

import boto3
import json
import os
import btr3baseball

jobTable = os.environ['JOB_TABLE']
jobQueue = os.environ['JOB_QUEUE']
repo = btr3baseball.JobRepository(jobTable)
queue = boto3.resource('sqs').get_queue_by_name(QueueName=jobQueue)

def submitJob(event, context):
    # Put initial entry in dynamo db
    jobId = repo.createJob(event)

    # Put the job ID on the SQS queue
    response = queue.send_message(MessageBody=jobId)

    # Update the DB entry with sqs message ID for traceability
    repo.updateWithMessageId(jobId, response.get('MessageId')) 

def getJob(event, context):
    repo.getJob(event['jobId'])
