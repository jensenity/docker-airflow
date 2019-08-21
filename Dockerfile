# VERSION 1.10.2
# AUTHOR: Matthieu "Puckel_" Roisil
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t puckel/docker-airflow .
# SOURCE: https://github.com/puckel/docker-airflow

FROM python:3.6-slim
LABEL maintainer="Puckel_"

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=1.10.3
ARG AIRFLOW_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_GPL_UNIDECODE yes

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
        openssh-server \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        # mysql-server \
        # libmysqlclient-dev \
        # mysql-python \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
        pigz \
        ssh \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && pip install --upgrade pip \
    && pip install -U pip setuptools wheel \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install kafka-python \
    && pip install apache-airflow[crypto,celery,postgres,password,s3,slack,redis,hive,jdbc,mysql,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} \
    && pip install "celery[redis]>=4.2.1, <4.3.0" \
    && pip install -U pip==19.0.1 setuptools==40.7.0 wheel==0.32.3 \
    && pip install pytz==2018.9  \
    && pip install pyOpenSSL==19.0.0 \
    && pip install ndg-httpsclient==0.5.1 \
    && pip install pyasn1==0.4.5 \
    && pip install psycopg2==2.7.7 \
    && pip install ethereum-etl \
    && pip install httplib2 \
    && pip install google-auth-httplib2 \
    && pip install google-cloud-bigquery \
    && pip install --upgrade google-api-python-client \
    && pip install --upgrade google-cloud-storage \
    && pip install gspread \
    && pip install oauth2client \
    && pip install pandas_gbq \
    && pip install boto3 \
    && pip install bs4 \
    && pip install pandas \
    && pip install pyspark \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi 


#COPY create-user.py /create-user.py
COPY script/entrypoint.sh /entrypoint.sh
# COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY config/airflow-2.cfg ${AIRFLOW_HOME}/airflow.cfg
#COPY config/webserver_config.py /usr/local/airflow/webserver_config.py

# Git Clone with Personal Token on klaytn-etl (GitHub, Settings --> Developer Settings)
RUN git clone https://1f15f18763ae4a449af2c3ffc58dd093683c0ae2@github.com/ground-x/klaytn-etl.git

RUN apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

RUN chown -R airflow: ${AIRFLOW_HOME}

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"] # set default arg for entrypoint