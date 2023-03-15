#!/bin/bash

# echo "Starting setup"
# rm -rf ./dags ./logs ./plugins
# mkdir -p ./dags ./logs ./plugins ./plugins/python_code
# echo "moving files"
# cp ./code/dag_process_xml.py ./dags
# cp ./code/process_xml.py ./plugins/python_code/
# cp -r ./data ./dags/
# cp -r ./config ./dags/

NETWORK=$(basename "$(pwd)")_default

docker network create $NETWORK

echo -e "AIRFLOW_UID=$(id -u)" > .env

echo "Starting  neo4j"
docker start neo || docker restart neo || docker run -d -e NEO4J_AUTH=none --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --name neo --network $NETWORK neo4j


NEO4J_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' neo)
echo $NEO4J_IP

JSON="{
    \"neo4j\": {
        \"host\": \"$NEO4J_IP\",
        \"port\": \"7687\"
    },

    \"root_path\": \"/opt/airflow/\",
    \"file_path\": \"dags/data/Q9Y261.xml\"
}"

echo $JSON > ./dags/config/config.json
echo "Building Airflow Image"
docker build ./ -t my_airflow

echo "Setting up Airflow"
docker-compose up airflow-init
docker-compose up -d  
echo "airflow setup finished"


