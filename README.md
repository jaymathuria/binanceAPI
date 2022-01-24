This python package is designed to retrive data from binance API (for BTCUSDT) - kline, getting latest server timestamp and all_orders.

Secret keys and other config details are saved in seperate config file. Encryption of the secret keys can be done as part of future development.
All functions are part of seperate python script called as function.py

binance_conn is for making connection and API_call is used for calling APIs from specified binance url. These can be further optimized by removing redudant code for error handling as part of future development. 
Currently, as part of this assignent API call is hardocded for symbol BTCUSDT which can be parameterized for future enhancements.
Retry logic can also be implemented as par tof future release.

Current data is uploaded to AWS S3 using boto3 module.
