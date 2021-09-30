FROM python:3.8

WORKDIR app

RUN pip install pika numpy pandas selenium

COPY . .

CMD ["python", "worker.py"]