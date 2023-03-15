#!/bin/bash

# echo "Starting setup"
# rm -rf ./dags ./logs ./plugins
# mkdir -p ./dags ./logs ./plugins ./plugins/python_code
# echo "moving files"
# cp ./code/dag_process_xml.py ./dags
# cp ./code/process_xml.py ./plugins/python_code/
# cp -r ./data ./dags/
# cp -r ./config ./dags/

echo -e "AIRFLOW_UID=$(id -u)" > .env

# echo "Starting  neo4j"
# docker run -d --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data neo4j

echo "Building Airflow Image"
docker build ./ -t my_airflow

echo "Setting up Airflow"
docker-compose up airflow-init
docker-compose up   
echo "airflow setup finished"
