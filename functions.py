import os

import boto3
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
load_dotenv(verbose=True)
from config import *

## Create binance connection
def binance_conn():
    client = Client(api_key, api_secret)
    client.API_URL = URL
    return client

## Make API call to binance
def API_call(client,name, timestamp):
    if name == 'klines':
        try:
            data=client.get_historical_klines('BTCUSDT', '1m', timestamp, limit=1000)
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
            exit()
        else:
            print("Kline API call successful")
            return data
    elif name == 'timestamp':
        try:
            data=client._get_earliest_valid_timestamp('BTCUSDT', '1m')
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
            exit()
        else:
            print("timestamp API call successful")
            return data
            
    elif name == "get_all_orders":     
        try:
            data=client.get_all_orders(symbol='BTCUSDT', limit=1000) 
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
            exit()
        else:
            print("get_all_orders  API call successful")
            return data   

## Create AWS session
def aws_session(region_name='us-east-1'):
    return boto3.session.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_ACCESS_KEY_SECRET'),
                                region_name=region_name)
            
## Create bucket - common for both files
def make_bucket(name, acl):
    session = aws_session()
    s3_resource = session.resource('s3')
    return s3_resource.create_bucket(Bucket=name, ACL=acl)

## Upload file function
def upload_file_to_bucket(bucket_name, file_path):
    session = aws_session()
    s3_resource = session.resource('s3')
    file_dir, file_name = os.path.split(file_path)

    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_file(
      Filename=file_path,
      Key=file_name,
      ExtraArgs={'ACL': 'public-read'}
    )

    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    return s3_url