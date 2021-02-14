import os
import ccxt

ftx_client = ccxt.ftx({
    'apiKey': os.getenv('FTX_API_KEY'),
    'secret': os.getenv('FTX_API_SECRET'),
    'hostname': 'ftx.us',
})
