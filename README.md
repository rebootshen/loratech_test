

Note: change the DATABASE_URL value to your database url,
also change JWT_SECRET_KEY value to whatever you want to use as your secret key

--------------------------------------
## 1. Install dependencies

Project Pre-requisites & Dependencies:
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

pip install pipenv

pipenv shell

pipenv install flask flask-sqlalchemy psycopg2 flask-migrate flask-script marshmallow flask-bcrypt pyjwt manage

if "pipenv install xxx" not working for some package, you may need run "pip install xxx"
```

--------------------------------------

## 2. Set up environment

Run the following from your terminal (if windows, if linux change SET for $ export)
```
SET PORT=5432
SET FLASK_ENV=development
SET JWT_SECRET_KEY=LongLongAgoThereIsASecret
SET DATABASE_URL=postgresql://postgres:test@localhost:5432/temp_project
SET DATABASE_TEST_URL=postgresql://postgres:test@localhost:5432/temp_project
```

or you can put all in .env file under src

--------------------------------------

## 3. Run unit test


pytest src


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

~ Get Prices by date and time window > 90  ~
POST http://127.0.0.1:5000/prices/long
          -Body raw JSON-
{ "ticker": "000001.CN", "day": "2018-04-26", "time_window": "91" }

          -headers-
"api_token": jwt_token copied from users/login response
"Content-Type":"application/json"  
          
```
===================================

### Testing USER on POSTMAN

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