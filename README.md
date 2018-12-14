[![Build Status](https://travis-ci.org/Raywire/iReporter.svg?branch=ft-user-endpoins-162357018)](https://travis-ci.org/Raywire/iReporter)
[![Coverage Status](https://coveralls.io/repos/github/Raywire/iReporter/badge.svg?branch=develop)](https://coveralls.io/github/Raywire/iReporter?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/1569388b5eb50371ab82/maintainability)](https://codeclimate.com/github/Raywire/iReporter/maintainability)

Project: iReporter
Description:iReporter enables any citizen to bring any form of corruption to the notice of appropriate authorities and the
general public. Users can also report on things that needs government intervention.

GitHub Pages Link: https://raywire.github.io/iReporter/

## Getting Started

git clone https://github.com/Raywire/iReporter

### Prerequisites

A database called ireporter with a user called raywire and password is required
You can also add your username and password to app/db_config.py
```
sudo -u postgres psql
postgres=# create database ireporter;
postgres=# create user raywire with encrypted password 'password';
postgres=# grant all privileges on database ireporter to raywire;
```
Contents of .env file
```
source venv/bin/activate

export FLASK_ENV="development"

export DATABASE_URL="dbname='ireporter' host='localhost' port='5432' user='raywire' password='password'"
export DATABASE_URL_TEST="dbname='test_ireporter' host='localhost' port='5432' user='raywire' password='password'"
export SECRET_KEY="secret-key-goes-here"

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
Run the command to install all requirements inside the virtual environment

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

Tests check all interventions, user sign up and login endpoints
Note an admin user is created by default in case none is present upon running the tests

```
source .env
pytest --cov=app/
```


## Deployment on Heroku

https://pure-wildwood-82378.herokuapp.com/api/v2/signup

## Built With

* [Flask](http://flask.pocoo.org/docs/dev/) - Flask


## API Endpoints

versioning for the endpoints
/api/v2/

## API Documentation
https://web.postman.co/collections/5905120-3d945622-5406-4eb7-97a0-d4b439dd7f4a?workspace=17077477-b7d0-4571-89d7-427b4b5a1bd8	 	


## Author

* **Ryan Simiyu** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details