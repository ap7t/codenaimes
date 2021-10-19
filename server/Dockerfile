FROM python:3.8.2

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python" ]

EXPOSE 5000

CMD [ "app.py" ]
