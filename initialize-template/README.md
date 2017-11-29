# Connection and Variables Intialization

To set up local initialization for connections and variables

- Copy initialize_template/* to initialize/*

- Edit connection.json and varaibles.json 

- For the GCP connection, copy the service account json file into the initialize folder and reference it from connection.json

in docker-compose, mount this volume
    - ./initialize:/usr/local/airflow/initialize
