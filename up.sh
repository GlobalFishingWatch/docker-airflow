#!/bin/bash

mkdir -p temp-dags
rm -rf temp-dags/*
docker-compose -f docker-compose-test.yaml up -d

