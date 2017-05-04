export JOB_TABLE="baseball-jobs"
export JOB_BUCKET="baseball-workbench-data"
export JOB_QUEUE="awseb-e-isz2m93ktp-stack-AWSEBWorkerQueue-1VUGPCHXODUM8"
jobConfig=$(<job.txt)
cmd="python -c 'from api import *; submitJob(\"${jobConfig}\")'"
echo ${cmd}
eval ${cmd}
