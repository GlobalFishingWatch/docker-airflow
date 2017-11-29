#!/usr/bin/env bash

# Modify this to add custom variables and connections to your installation

MOUNT_PATH=/usr/local/airflow/initialize


# Install GCP Service Account
airflow connections --delete --conn_id=google_cloud_default
airflow connections --add \
  --conn_id=google_cloud_default \
  --conn_type=google_cloud_platform \
  --conn_extra="$(cat ${MOUNT_PATH}/connection.json)"


#Install Variables
airflow variables --import ${MOUNT_PATH}/variables.json
