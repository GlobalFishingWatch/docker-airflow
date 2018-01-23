# VERSION 1.8.1
# AUTHOR: Matthieu "Puckel_" Roisil
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t puckel/docker-airflow .
# SOURCE: https://github.com/puckel/docker-airflow

FROM debian:jessie
MAINTAINER Puckel_

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=1.8.1
ARG AIRFLOW_HOME=/usr/local/airflow

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN set -ex \
    && buildDeps=' \
        python-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        build-essential \
        libblas-dev \
        liblapack-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        python-pip \
        python-requests \
        apt-utils \
        curl \
        netcat \
        locales \
        iptables \
        init-system-helpers \
        libapparmor1 \
        libltdl7 \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && python -m pip install -U pip \
    && pip install six==1.10.0 \
    && pip install Cython \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install google-api-python-client \
    && pip install pandas-gbq \
    && pip install https://github.com/apache/incubator-airflow/archive/1.9.0rc1.tar.gz \
    && pip install psycopg2 \
    && pip install celery[redis]==3.1.17 \
    && apt-get remove --purge -yqq $buildDeps \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

# Install docker (from https://docs.docker.com/engine/installation/linux/docker-ce/debian/#upgrade-docker-ce and
#                  and https://github.com/docker-library/docker/blob/master/Dockerfile.template)

RUN curl -L -o docker.deb \
       "https://download.docker.com/linux/debian/dists/jessie/pool/stable/amd64/docker-ce_17.03.2~ce-0~debian-jessie_amd64.deb" \
  && dpkg -i docker.deb

# Download and install google cloud. See the dockerfile at
# https://hub.docker.com/r/google/cloud-sdk/~/dockerfile/
RUN  \
  export CLOUD_SDK_APT_DEPS="curl gcc python-dev python-setuptools apt-transport-https lsb-release openssh-client git" && \
  export CLOUD_SDK_PIP_DEPS="crcmod" && \
  apt-get -qqy update && \
  apt-get install -qqy $CLOUD_SDK_APT_DEPS && \
  pip install -U $CLOUD_SDK_PIP_DEPS && \
  export CLOUD_SDK_VERSION="184.0.0" && \
  export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
  echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
  apt-get update && \
  apt-get install -y google-cloud-sdk=${CLOUD_SDK_VERSION}-0 && \
  gcloud config set core/disable_usage_reporting true && \
  gcloud config set component_manager/disable_update_check true && \
  gcloud config set metrics/environment github_docker_image

COPY script/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

RUN mkdir ${AIRFLOW_HOME}/utils 
COPY utils/* ${AIRFLOW_HOME}/utils/
RUN mkdir ${AIRFLOW_HOME}/dags


RUN chown -R airflow: ${AIRFLOW_HOME}

EXPOSE 8080 5555 8793

USER root
WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["/entrypoint.sh"]
