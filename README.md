[![Build Status](https://travis-ci.org/Raywire/iReporter.svg?branch=ft-user-endpoins-162357018)](https://travis-ci.org/Raywire/iReporter)
[![Coverage Status](https://coveralls.io/repos/github/Raywire/iReporter/badge.svg?branch=develop)](https://coveralls.io/github/Raywire/iReporter?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/1569388b5eb50371ab82/maintainability)](https://codeclimate.com/github/Raywire/iReporter/maintainability)

Project: iReporter
Description:iReporter enables any citizen to bring any form of corruption to the notice of appropriate authorities and the
general public. Users can also report on things that needs government intervention.

GitHub Pages Link: https://raywire.github.io/iReporter/UI

## Getting Started

git clone https://github.com/Raywire/iReporter

### Prerequisites

A postgres database is required
You can add your username and password to app/db_config.py

**Setting up the database with a user who has all privileges**
```
sudo -u postgres psql
postgres=# create database your-database;
postgres=# create user your-username with encrypted password 'your-password';
postgres=# grant all privileges on database your-database to your-username;
```
Contents of .env file
```
source venv/bin/activate

export FLASK_ENV="development"
export FLASK_CONFIG="development"
export DATABASE_URL="dbname='your-database' host='localhost' port='5432' user='your-username' password='your-password'"
export DATABASE_URL_TEST="dbname='your-test-database' host='localhost' port='5432' user='your-username' password='your-password'"
export SECRET_KEY="secret-key-goes-here"
export MAIL_USERNAME="your-gmail-account"
export MAIL_PASSWORD="your-password"
export SUPER_USER_PASSWORD="your-password"
export SUPER_USER_USERNAME="your-username"
export SUPER_USER_EMAIL="your-email"
export SUPER_USER_FIRSTNAME="your-name"
export SUPER_USER_LASTNAME="your-name"
export SUPER_USER_OTHERNAMES="your-name"
export SUPER_USER_PHONENUMBER="your-phone-number"

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
Set FLASK_CONFIG to testing on your .env file before running tests

### Break down into end to end tests

Tests check all interventions, user sign up and login endpoints
Note a super user is created by default in case none is present upon running the app

```
source .env
pytest --cov=app/
```


## Deployment on Heroku

[Heroku Application Link](https://enigmatic-inlet-54773.herokuapp.com/api/v2/auth/signup)

## Built With

* [Flask](http://flask.pocoo.org/docs/dev/) - Flask


## API Endpoints

versioning for the endpoints
/api/v2/

## API Documentation
[Postman Documentation Link](https://web.postman.co/collections/5905120-3d945622-5406-4eb7-97a0-d4b439dd7f4a?workspace=17077477-b7d0-4571-89d7-427b4b5a1bd8)

[Apiary API Documentation](https://ireporter14.docs.apiary.io/#)


## Author

* **Ryan Simiyu** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details