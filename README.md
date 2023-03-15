# weavebio-challenge

## How run this project

First: fill your neo4j host, port, login and password parameters on config.json file on /dags/configs
as the example below
```json
{
    "neo4j": {
        "host": "172.27.0.8",
        "port": "7687",
        "login": "neo4j",
        "password": "********"
    },

    "root_path": "/opt/airflow/",
    "file_path": "dags/data/Q9Y261.xml"
}

```

there is no need to change file_path and root_path


### Running script.

we will need [docker](https://docs.docker.com/engine/install/) and [docker composer](https://docs.docker.com/compose/)
 to execute this project



After filling the database info, you just need to run

```bash
./script
```

and an airflow container will start
