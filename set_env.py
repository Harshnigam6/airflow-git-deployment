# set_env.py

import json
import os

def set_env_variables_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        for key, value in data.items():
            os.environ[key] = value
            print(os.environ[key], key)

if __name__ == "__main__":
    set_env_variables_from_json('/opt/airflow/env_var.json')
