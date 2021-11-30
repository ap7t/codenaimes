FROM python:3.8.2

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["/app/bin/gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--chdir", "/usr/src/", "app:app"]
