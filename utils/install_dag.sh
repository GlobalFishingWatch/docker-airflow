#!/bin/bash

# Arguments: CONTAINER_NAME 
#
# CONTAINER_NAME : path to the docker image
#
#  For example, an image in google container engine
#    gcr.io/PROJECT_ID/github-globalfishingwatch-anchorages_pipeline:test-image-building
#  Or a local image
#    gfw/anchorages_pipeline:latest
#

display_usage() {
	echo "Usage \n$0 DOCKERIMAGE [post-install-args]"
	}


if [[ $# -le 0 ]]
then
    display_usage
    exit 1
fi

IFS=':' read -ra PARTS <<< "$1"
IFS='/' read -ra PARTS <<< "${PARTS[0]}"
IMAGE=${PARTS[${#PARTS[@]}-1]}

CONTAINER=$1
HOST_DAG_PATH=${HOST_DAGS}/${IMAGE}
AIRFLOW_DAG_PATH=${AIRFLOW_HOME}/dags/${IMAGE}
CONTAINER_DAG_PATH=/dags
POST_INSTALL=${AIRFLOW_DAG_PATH}/post_install.sh

echo "Updating docker image"
echo "  Container: $CONTAINER"

gcloud docker -- pull $CONTAINER

echo "Creating dag install folder"
echo "  Host path: $HOST_DAG_PATH"
echo "  Local path: $AIRFLOW_DAG_PATH"
echo "  Container path: $CONTAINER_DAG_PATH"

mkdir -p $AIRFLOW_DAG_PATH

echo ""
echo "Installing Dags"
echo "  Container: $CONTAINER"

gcloud docker -- run --entrypoint=/bin/bash -v $HOST_DAG_PATH:$CONTAINER_DAG_PATH $CONTAINER install.sh


echo ""
echo "Executing post install"
echo "  Script: $POST_INSTALL"

/bin/bash $POST_INSTALL "$@"

echo ""
echo "Done"
