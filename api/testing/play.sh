#!/bin/bash

cluster="BTR-standard-ECSCluster-PCPU2E2BPZZQ"
definition="arn:aws:ecs:us-east-1:235079478010:task-definition/baseball-dev-WorkerTaskDefinition-963P1KUD9Z9O:1"
aws ecs run-task --task-definition ${definition} --cluster ${cluster}
