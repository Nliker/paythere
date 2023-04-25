FROM python:3.10

ADD requirements.txt /env/app/requirements.txt

WORKDIR /env/app

RUN pip install -r requirements.txt

ADD . /app

WORKDIR /app

CMD ["python","main.py"]
