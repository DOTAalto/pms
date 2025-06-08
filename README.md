# DOT PMS

## Key features over typical party systems
- Uploading entries don't require vote key. Only voting does.
- Entry metadata has a later deadline than the file deadline.
- Live vote is synchronized to slides.
- Entry slide can be previewed by submitters exactly as they are on the big screen.
- Text templates for YouTube titles and descriptions with entry name, compo name, score, etc.
- Polished metadata form, for example making it clean which info is public vs private, checkbox if the demo has audio, if it exits automatically.

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
