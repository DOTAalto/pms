FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app/
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

RUN python manage.py collectstatic --noinput

EXPOSE 8000

#CMD ["gunicorn"]
ENTRYPOINT ["/app/entrypoint.sh"]
