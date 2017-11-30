#!/bin/bash

# Argument is path (not counting project to container engine name e.g., 
# github-globalfishingwatch-anchorages_pipeline:test-image-building)
echo "Installing $1"

IFS=':' read -ra PARTS <<< "$1"
DEST_PATH=$AIRFLOW_HOME/dags/${PARTS[0]}
echo "Creating $DEST_PATH as destination"
# TODO: What to do if path exists?
mkdir $DEST_PATH

echo "Executing install.sh from docker_file"
CONTAINER=gcr.io/world-fishing-827/$1
docker run -v $DEST_PATH:/dags $CONTAINER /bin/bash install.sh


# POST_INSTALLER=$DEST_PATH/post_install.sh
# echo "Executing $POST_INSTALLER"
# /bin/bash $POST_INSTALLER
