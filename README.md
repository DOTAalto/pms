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
python manage.py migrate
python manage.py createsuperuser
```
4. Run the server
```
python manage.py runserver
```