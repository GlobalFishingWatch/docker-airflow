#!/usr/bin/env bash

# Modify this to add custom variables and connections to your installation

MOUNT_PATH=/usr/local/airflow/initialize


# Install GCP Service Account
airflow connections --add \
  --conn_id=google_cloud_default \
  --conn_type=google_cloud_platform \
  --conn_extra="$(cat ${MOUNT_PATH}/connection.json)"

# Install SLACK connection
airflow connections --add \
  --conn_id=slack_on_failure \
  --conn_type=http \
  --conn_host=https://hooks.slack.com/services \
  --conn_password=${SLACK_WEBHOOK_TOKEN}

#Install Variables
airflow variables --import ${MOUNT_PATH}/variables.json
airflow variables --set PIPELINE_START_DATE $(date -d "-3 days" +"%Y-%m-%d")

airflow pool -s dataflow 1 "Google Cloud Dataflow jobs"
airflow pool -s bigquery 1 "Google Bigquery jobs"
airflow pool -s k8operators_limit 3 "kubernetes"

if [ ! -z ${TEST_PIPELINE} ]; then
  /usr/local/airflow/dags/${TEST_PIPELINE}/post_install.sh gfw/${TEST_PIPELINE}
fi
