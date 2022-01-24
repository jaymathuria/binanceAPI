from functions import *
import csv

## Step 1: Setting up binance connection. Using testnet for this script
client=binance_conn()

## Step 2:  Get latest timestamp from binance
timestamp = API_call(client,"timestamp",'')

## Step 3:  Get historical proce for BTCUSDT
gemini_data =API_call(client,"klines", timestamp)

## Step 4:  Writing actual data to file
if (gemini_data):
    with open('gemini.csv', 'w') as d:
        for line in gemini_data:
            d.write(f'BTCUSD, {line[1]}, {line[4]}, {line[2]}, {line[3]},{line[7]},{line[5]},{line[8]},{line[0]},{line[6]}\n')
else:
    print("No Market Data from Binance")
    exit();
     
        
## Step 5: Get all orders for BTCUSDT
orders =API_call(client,"get_all_orders", '')## Since no order was actually placed in my dummy account. It has no data.

## Step 6:  Writing actual data to file
if (orders):
    with open('gemini_order_data.csv', 'w') as d1:
        for line in gemini_order_data:
            d1.write(f'{line[symbol]}, {line[orderID]}, {line[Price]}, {line[origQty]},{line[executedQty]},{line[status]},{line[type]},{line[side]}\n')
else:
    print("No Order Data from Binance")
    

## Create AWS session                
session = aws_session()

## Create bucket
s3_bucket = make_bucket('gemini-dataset1212', 'public-read')  

## Upload file 1
s3_url = upload_file_to_bucket('gemini-dataset1212', 'gemini.csv')  if (gemini_data) else print("No upload of market file to AWS") ## Upload only if data was retrieved from Binance

## Upload file 2
s3_url = upload_file_to_bucket('gemini-dataset1212', 'gemini_order_data.csv')  if (orders) else print("No upload of order file to AWS")  ## Since no order was actually placed in my dummy account. It has no data

## File upload location
## https://gemini-dataset1212.s3.amazonaws.com/gemini.csv.csv

