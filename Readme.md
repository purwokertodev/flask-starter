## Python starter project with Flask and Docker

### Getting started
- create virtual env 
```shell
$ virtualenv env -p python3 --no-site-packages
```
- activate virtual env
```shell
$ source env/bin/activate
```

- install dependencies
```shell
$ pip install -r requirements.txt
$ pip freeze > requirements.txt
```

- create database
```shell
$ psql postgres
$ postgres=# CREATE DATABASE flask_auth;
```

- run migration
```shell
$ python main.py create_db
```

- run
```shell
$ python main.py runserver
```