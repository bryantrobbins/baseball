#!/usr/bin/python
from flask import Flask, jsonify, request, abort
import rpy2.robjects as robjects
import boto3
import os
import shutil
import time
import btr3baseball

app = Flask(__name__)

# TODO: Set these through external environment variables
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["JOB_TABLE"] = "baseball-jobs"

# Load vars
jobTable = os.environ['JOB_TABLE']

# Init clients
s3 = boto3.resource('s3')
repo = btr3baseball.JobRepository(jobTable)

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

@app.route('/baseball/work', methods=['POST'])
def create_task():
    if not request.json or not 'jobId' in request.json:
        abort(400)
    jobId = message.body
    jobInfo = repo.getJob(jobId)
    if jobInfo is not None:
        print('Doing the work')
        doJob(jobId, jobInfo['job-details'])
        repo.updateForSuccess(jobId)
    return jsonify({'task': task}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

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

