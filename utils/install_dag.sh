#!/bin/bash

# Arguments: CONTAINER_NAME 
#
# CONTAINER_NAME : path (not counting project) to container engine e.g., 
#                github-globalfishingwatch-anchorages_pipeline:test-image-building)

echo "Installing $1"

IFS=':' read -ra PARTS <<< "$1"
DEST_PATH=$AIRFLOW_HOME/dags/${PARTS[0]}

# This is the path to the directory we want to mount on the host system
HOST_DEST_PATH=${HOST_DAGS}/${PARTS[0]}

echo "Creating $DEST_PATH as destination"
# TODO: What to do if path exists?
mkdir $DEST_PATH

echo "Executing install.sh from docker_file"
CONTAINER=gcr.io/world-fishing-827/$1
docker run -v $HOST_DEST_PATH:/dags $CONTAINER /bin/bash install.sh

POST_INSTALLER=$DEST_PATH/post_install.sh
echo "Executing $POST_INSTALLER"
/bin/bash $POST_INSTALLER $1
