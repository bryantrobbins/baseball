from __future__ import print_function

import boto3
import json
import os
import btr3baseball
import logging

logging.basicConfig(level=logging.INFO)

jobTable = os.environ.get('JOB_TABLE')
jobQueue = os.environ.get('JOB_QUEUE')
jobBucket = os.environ.get('JOB_BUCKET')
dsRepo = btr3baseball.DatasetRepository()
if jobQueue:
    queue = boto3.resource('sqs').get_queue_by_name(QueueName=jobQueue)
if jobTable:
    print(jobTable)
    jobRepo = btr3baseball.JobRepository(jobTable)
if jobBucket:
    s3_client = boto3.client('s3')

def main(event, context):
    method = event['method']
    if 'data' in event:
        data = event['data']
    else:
        data = None

    print(data)

    if method == 'getOutputImage':
        return getOutputImage(data['jobId'])
    elif method == 'submitJob':
        return submitJob(data)
    elif method == 'validateJob':
        return validateJob(data)
    elif method == 'getJob':
        return getJob(data['jobId'])
    elif method == 'listDatasets':
        return listDatasets()
    elif method == 'getDataset':
        return getDataset(data['datasetId'])
    else:
        return None

def getOutputImage(jobId):
    logging.info("Downloading image for job {}".format(jobId))
    response = s3_client.get_object(Bucket=jobBucket,Key="jobs/{}/output.svg".format(jobId))
    print(response)
    contents = response['Body'].read()
    ind1 = contents.find('\n')
    contents = contents[ind1+1:].replace('\n', '')
    return contents

def submitJob(configBodyString):
    print(configBodyString)
    # Validate configuration object
    configValidator = btr3baseball.ConfigValidator(configStr = configBodyString)
    configValidator.validateConfig()

    # Put initial entry in dynamo db
    jobId = jobRepo.createJob(configBodyString)

    # Put the job ID on the SQS queue
    response = queue.send_message(MessageBody=jobId)

    # Update the DB entry with sqs message ID for traceability
    return jobRepo.updateWithMessageId(jobId, response.get('MessageId')) 

def validateJob(configBodyString):
    res = {}

    # Validate configuration object
    configValidator = btr3baseball.ConfigValidator(configObj = configBodyString)
    configValidator.validateConfig()

    res['result'] = True
    return res

def getJob(jobId):
    return jobRepo.getJob(jobId)

def listDatasets():
    return dsRepo.listDatasets()

def getDataset(datasetId):
    return dsRepo.getDataset(datasetId)
