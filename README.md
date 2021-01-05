# GCP Flask Template

This is solid starting point for Flask apps running on GCP using the following:

- Python 3.9 (GA)
- Cloud SQL PostgreSQL 12
- App Engine Standard

The application has some basic Oauth Flows and CRUD actions to get you started

Install and Connect to [Cloud SQL Proxy](https://cloud.google.com/sql/docs/postgres/quickstart-proxy-test)

Check the link and find your OS. For MacOS 64bit, the command would look something like:

#### Install Cloud SQL Proxy
```
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64
chmod +x cloud_sql_proxy
```
#### Run Cloud SQL Proxy
```
./cloud_sql_proxy -instances=<INSTANCE_CONNECTION_NAME>=tcp:5432
```

#### Copy env and app.yaml examples
```
cp .env.example .env && cp app.yaml.example app.yaml # don't commit secrets in app.yaml or .env
```

#### Create virtual env and run the app
```
python3 -m venv venv # creates a directory in ./ where all modules live
source venv/bin/activate # activate the virtural environment
pip install -r requirements.txt # grabs modules
export FLASK_APP=main.py
flask db upgrade
flask run
```

## TODO

- support for GAE Flex and Cloud Run
- update Dockerfile
