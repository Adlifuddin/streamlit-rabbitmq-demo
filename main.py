import pandas as pd 
import numpy as np
import streamlit as st
from producer import ProducerClient
import pika
import json

st.set_page_config(layout="wide")

st.title("News Web Scraper")

producer = ProducerClient()

st.warning('You can also scrape from many url links such that the format: [url], [url], ...')
st.warning(
    """
    Example links: https://www.bharian.com.my/berita/nasional/2021/09/865934/kegagalan-cerun-berlaku-terlalu-awal-jkr,
    https://www.bharian.com.my/berita/nasional/2021/09/865983/kenaikan-harga-makanan-ayam-hanya-sementara,
    """
)
url = st.text_area('Enter a News URL (from Berita Harian only [https://www.bharian.com.my/])', height=100)
links = url.split(',')

# remove null in links
for l in range(len(links)):
    if links[l] == "":
        links.pop(l)

if st.button('Start Crawl'):

    data = producer.crawl(links)

    st.write(data)

if st.button('Start Pub/Sub'):
    st.write(data)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    channel.basic_publish(exchange='logs', routing_key='', body=json.dumps(data))
    
    connection.close()

if st.button('Start Work Queues'):
    st.write(data)