# DOT PMS

## Setup for development
(This has been tested for Python 3.12)

1. Setup a python virtual environment and activate it. Your preferred way works but for example
```
python -m venv .venv
source .venv/bin/activate
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Run migrations and create a superuser for yourself
```
mkdir db
# activate .env variables
python manage.py migrate
python manage.py createsuperuser
```
4. Run the server
```
python manage.py runserver
```

5. Create a party
The root path will give an error initially. Log in to your admin account and create a party in http://127.0.0.1:8000/admin/party/party/add/. You will also need to create a compo before some features are visible.