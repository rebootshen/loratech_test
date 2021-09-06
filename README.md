

Note: change the DATABASE_URL value to your database url,
also change JWT_SECRET_KEY value to whatever you want to use as your secret key

--------------------------------------
## 1. Install dependencies

### Project Pre-requisites & Dependencies:
```python
python3.x
postgresql
pipenv

flask
flask sqlalchemy
psycopg2
flask-migrate
flask-script
marshmallow
flask-bcrypt
pyjwt
manage
```

### Setup virtual environment
```
pip install pipenv
pipenv shell  
pipenv --venv 

pipenv install
pipenv graph 
```


if failed you may need install missing packages one by one:

```
pipenv install pytest

pipenv install flask flask-sqlalchemy psycopg2 flask-migrate flask-script marshmallow flask-bcrypt pyjwt manage
```

if "pipenv install xxx" not working for some packages, you may need run "pip install xxx"

--------------------------------------

## 2. Setup project environment

Run the following from your terminal (if windows, if linux change SET for $ export)
```
SET PORT=5000
SET FLASK_ENV=development
SET JWT_SECRET_KEY=LongLongAgoThereIsASecret
SET DATABASE_URL=postgresql://postgres:test@localhost:5432/temp_project
SET DATABASE_TEST_URL=postgresql://postgres:test@localhost:5432/temp_project
SET SQLALCHEMY_TRACK_MODIFICATIONS=False
```

or you can put all in ".env" file under src
```
PORT=5000
FLASK_ENV=development
JWT_SECRET_KEY=LongLongAgoThereIsASecret
DATABASE_URL=postgresql://postgres:test@localhost:5432/temp_project
DATABASE_TEST_URL=postgresql://postgres:test@localhost:5432/temp_project
SQLALCHEMY_TRACK_MODIFICATIONS=False
```
--------------------------------------

## 3. Run unit test


pytest src


This step will create User table in postgresql database.

--------------------------------------

## 4. Startup the web server:

python run.py

======================================

## 5. Testing on POSTMAN:


### Testing PRICES on POSTMAN:

```
~ Get Prices by date and time window <= 90  ~
POST http://127.0.0.1:5000/prices/short
          -Body raw JSON-
{ "ticker": "000001.CN", "day": "2018-04-26", "time_window": "10" }

          -headers-
"Content-Type":"application/json"  
          
---------------

~ Get Prices by date and time window <= 90 , will fail if time_window > 90 ~
POST http://127.0.0.1:5000/prices/short
          -Body raw JSON-
{ "ticker": "000001.CN", "day": "2018-04-26", "time_window": "91" }

          -headers-
"Content-Type":"application/json"  
          
---------------

~ Get Prices by date and time window > 90  ~
POST http://127.0.0.1:5000/prices/long
          -Body raw JSON-
{ "ticker": "000001.CN", "day": "2018-04-26", "time_window": "91" }

          -headers-
"api_token": jwt_token copied from users/login response
"Content-Type":"application/json"  
          
```
===================================

### Testing USERS on POSTMAN

```
~ Create User POST ~
POST http://127.0.0.1:5000/users/
          -Body raw JSON-
{
"email": "test@mail.com",
"password": "test",
"name": "test"
}

          -headers-
"Content-Type":"application/json"  

Responsed with jwt_token, could be used to get prices

---------------

~ Login POST ~
POST http://127.0.0.1:5000/users/login
          -Body raw JSON-
{
"email": "test@mail.com",
"password": "test"
}
(copy jwt-token from login call)

          -headers-
"Content-Type":"application/json"  

---------------

```
