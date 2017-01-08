#!/usr/bin/python

import json
import rpy2.robjects as robjects
import boto3
import os
import shutil
import time

s3 = boto3.resource('s3')

pre ='''
.libPaths( "/tmp/rpackages" )
suppressMessages(library(dplyr))
suppressMessages(library(ggplot2))
suppressMessages(library(gridExtra))

sumRows <- function(d, ... ) {
  by_vars <- group_by_(d, ...)
  summed_groups <- summarise_if(by_vars, .predicate = function(x) is.numeric(x), funs("sum"))
  return(ungroup(summed_groups))
}

generateLeaderboard <- function(d, sortCol, sortDir, keyCols) {
  sortExpr = sprintf("%s(%s)", sortDir, sortCol)
  allCols = c(keyCols, sortCol)
  leaders <- arrange_(d, sortExpr)
  leaders <- selectWithKeys(leaders, keyCols, sortCol)
  leaders <- filter(leaders, row_number() <= 10L)
  p <- tableGrob(leaders)
  gp <- grid.arrange(p)
  ggsave(filename="output.svg", gp)
}

selectWithKeys <- function(d, keyCols, ...) {
  allCols = c(keyCols, c(...))
  return(select(d, one_of(allCols)))
}
'''
dfMap = { 'ROOT': '/tmp/datasources', 'Lahman_Batting': { 'source': 'data/lahman/Batting.csv', 'keyCols': ['playerID', 'stint', 'yearID'] } }

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

def doJob(jobId, config):
    # Create working directory
    workdir = '/tmp/rwork/{}'.format(jobId)
    if os.path.isdir(workdir):
        shutil.rmtree(workdir)
    os.makedirs(workdir)

    # Set working directory
    robjects.r('setwd("{}")'.format(workdir))

    # Load default functions
    robjects.r(pre)

    # Load dataset and keyCols
    dsConfig = dfMap[config['dataset']]
    robjects.r('df <- read.csv("{}/{}")'.format(dfMap['ROOT'], dsConfig['source']))
    keyString = 'c("'
    first = True
    for k in dsConfig['keyCols']:
        if first:
            first = False
        else:
            keyString += ',"'
        keyString += k
        keyString += '"'
    keyString += ')'
    robjects.r('keyCols <- {}'.format(keyString))

    # Manipulate data
    if 'transformations' in config:
        for manip in config['transformations']:
            if manip['type'] == "columnSelect":
                colList = ""
                first = True
                for col in manip['columns']:
                    if first:
                        first = False
                    else:
                        colList += ","
                    colList += '"{}"'.format(col)
                robjects.r('df <- selectWithKeys(df, keyCols, {})'.format(colList))
            elif manip['type'] == "rowSelect":
                colName = manip['column']
                colOp = manip['operator']
                colCriteria = manip['criteria']
                robjects.r('df <- filter(df, {} {} {})'.format(colName, colOp, colCriteria)) 
            elif manip['type'] == "columnDefine":
                colName = manip['column']
                colExpr = manip['expression']
                robjects.r('df <- mutate(df, {} = {})'.format(colName, colExpr))
            elif manip['type'] == "rowSum":
                colList = ""
                first = True
                for col in manip['columns']:
                    if first:
                        first = False
                    else:
                        colList += ","
                    colList += '"{}"'.format(col)
                robjects.r('df <- sumRows(df, {})'.format(colList))
                robjects.r('keyCols <- c({})'.format(colList))

    # Produce output
    outputConfig = config['output']
    if outputConfig['type'] == "leaderboard":
        robjects.r('generateLeaderboard(df, "{}", "{}", keyCols)'.format(outputConfig['column'], outputConfig['direction']))

    # Upload to s3
    s3.Bucket('baseball-workbench-data').upload_file('output.svg', 'jobs/{}/output.svg'.format(jobId))

    # Reset R session
    robjects.r('rm(list=setdiff(ls(all.names=TRUE), lsf.str(all.names=TRUE)))')
    robjects.r('setwd("/tmp")')

    # Remove output files
    shutil.rmtree('{}/'.format(workdir))

def updateForSuccess(jobId):
    print('Updating job record for success')
    response =  dynamo.update_item(
        Key={
            'job-id': jobId
        },
        UpdateExpression="set #K = :m",
        ExpressionAttributeNames={
            "#K":"job-status"
        },
        ExpressionAttributeValues={
            ':m': "COMPLETE",
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

def updateForError(jobId):
    print('Updating job record for error')

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
            jobId = message.body
            jobInfo = extractSingleJob(jobId)
            if jobInfo is not None:
                print('Doing the work')
                doJob(jobId, jobInfo['job-details'])
                updateForSuccess(jobId)
                message.delete()
