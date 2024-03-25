FROM apache/airflow:2.0.1


# Switch to root user to install dependencies
USER root

# Install Git, SSH-Agent, and jq
RUN apt-get update && \
    apt-get install -y git openssh-client jq && \
    rm -rf /var/lib/apt/lists/*

# Create SSH directory and add Bitbucket to known hosts
RUN mkdir -p /root/.ssh && \
    ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts

# Copy the SSH private key
COPY id_rsa /tmp/id_rsa
RUN chmod 600 /tmp/id_rsa

# Start the SSH agent, add the key, clone the repo, then clean up
RUN eval $(ssh-agent -s) && \
    ssh-add /tmp/id_rsa && \
    mkdir -p /opt/airflow/data && \
    git clone -b harsh/airflow_airbnb_los_upstream_monitoring git@bitbucket.org:syedsanahassan/pricelabs-reporting.git /opt/airflow/data && \
    ssh-agent -k 
    # && \
    # rm -f /tmp/id_rsa


# Copy the SSH private key and set permissions
COPY id_rsa /home/airflow/.ssh/id_rsa
RUN chmod 600 /home/airflow/.ssh/id_rsa && \
    chown airflow:airflow /home/airflow/.ssh/id_rsa


# Allow aiurflow user to access this file
RUN chmod 600 /tmp/id_rsa && \
    chown airflow:airflow /tmp/id_rsa


# Copy environment variable JSON and set_env script
COPY env_var.json /opt/airflow/env_var.json
COPY set_env.py /opt/airflow/set_env.py
RUN python /opt/airflow/set_env.py

# # Switch back to the airflow user for remaining operations
USER airflow

# Install dependencies
RUN pip install --user --upgrade pip && pip install --no-cache-dir --user -r /opt/airflow/data/requirements_airflow.txt


# Run Airflow webserver
CMD ["airflow", "webserver"]
