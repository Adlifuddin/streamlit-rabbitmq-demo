import pandas as pd 
import numpy as np
import streamlit as st
from producer import ProducerClient
import pika
import json

st.set_page_config(layout="wide")

st.title("Demo")

text = st.text_area('Enter a Message', height=100)

if st.button('Start RPC'):

    producer = ProducerClient()
    producer.call(text)

if st.button('Start Pub/Sub'):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    channel.basic_publish(exchange='logs', routing_key='', body=json.dumps(text))
    
    connection.close()

if st.button('Start Work Queues'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(text),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    
    connection.close()