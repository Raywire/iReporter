Project: iReporter
Description:iReporter enables any citizen to bring any form of corruption to the notice of appropriate authorities and the
general public. Users can also report on things that needs government intervention.

GitHub Pages Link: https://raywire.github.io/iReporter/

[![Build Status](https://travis-ci.org/Raywire/iReporter.svg?branch=ft-user-endpoins-162357018)](https://travis-ci.org/Raywire/iReporter)
[![Coverage Status](https://coveralls.io/repos/github/Raywire/iReporter/badge.svg?branch=ch-codecov-badge-162391750)](https://coveralls.io/github/Raywire/iReporter?branch=ch-codecov-badge-162391750)
[![Maintainability](https://api.codeclimate.com/v1/badges/1569388b5eb50371ab82/maintainability)](https://codeclimate.com/github/Raywire/iReporter/maintainability)

## Getting Started

git clone https://github.com/Raywire/iReporter

### Prerequisites

A database called ireporter with a user called raywire and password raywire2018 is required
You can also add your username and password to app/db_config.py
```
sudo -u postgres psql
postgres=# create database ireporter;
postgres=# create user raywire with encrypted password 'raywire2018';
postgres=# grant all privileges on database ireporter to raywire;
```
Contents of .env file
```
source venv/bin/activate

export FLASK_ENV="development"

export DATABASE_URL="dbname='ireporter' host='localhost' port='5432' user='raywire' password='raywire2018'"
export DATABBASE_URL_TEST="dbname='test_ireporter' host='localhost' port='5432' user='raywire' password='raywire2018'"
export SECRET_KEY="d01815253d8243a221d12a681589155e"

```
## Running the app
Cd into the iReporter folder

Create a virtual environment

```
python virtualenv venv
```
Run the virtual environment

```
source venv/bin/activate
```
Run the command to install all requirements

```
pip install -r requirements.txt
```
```
source .env
flask run
```

## Running the tests

Tests are to be run with pytest or py.test on the root of iReporter folder

### Break down into end to end tests

Tests check all redflag and user endpoints

```
source .env
pytest --cov=app/
```


## Deployment on Heroku

https://pure-wildwood-82378.herokuapp.com/api/v1/red-flags

## Built With

* [Flask](http://flask.pocoo.org/docs/dev/) - Flask


## API Endpoints

versioning for the endpoints
/api/v1/
	 	

|  Method  | Endpoint |  Description |
|---|---|---|
| POST  | /api/v1/red-flags  | Create a red-flag record  |
| GET  | /api/v1/red-flags  | Fetch all red-flag records  |
| GET  | /api/v1/red-flags/1  | Fetch a specific red-flag record  |
| PATCH  | /api/v1/red-flags/1/location  | Edit the location of a specific record  |
| PATCH  | /api/v1/red-flags/1/comment  | Edit the comment of a specific record  |
| DELETE  | /api/v1/red-flags/1   | Delete a specific red flag record  |
| PUT  | /api/v1/red-flags/1  | Edit the whole red-flag record at once  |
| POST  | /api/v1/users  | Create a user  |
| GET  | /api/v1/users  | Fetch all users  |
| GET  | /api/v1/users/1  | Fetch a specific user  |
| PATCH  | /api/v1/users/1/password  | Edit the password of a specific user  |
| PATCH  | /api/v1/users/1/status  | Edit the comment of a specific record  |
| DELETE  | /api/v1/users/1   | Delete a specific user  |
| PUT  | /api/v1/users/1  | Edit the whole user details  |
## Author

* **Ryan Simiyu** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details