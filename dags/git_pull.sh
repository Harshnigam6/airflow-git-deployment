#!/bin/bash

# Start the SSH agent
eval $(ssh-agent -s)

# Add your SSH key
ssh-add /tmp/id_rsa

# Ensure strict host key checking is off to avoid host verification issues
export GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"

# Clone or pull the repository
if [ -d "/opt/airflow/temp/.git" ]; then
    cd /opt/airflow/temp && git pull
else
    git clone -b "PUT_YOUR_GIT_REPO_LINK" /opt/airflow/temp
fi

# Kill the SSH agent
ssh-agent -k
