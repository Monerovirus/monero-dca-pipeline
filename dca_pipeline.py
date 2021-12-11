# dependent on Path (pip install pathlib)
# and cbpro (pip install git+git://github.com/Monerovirus/coinbasepro-python.git)

import math, os, sys, logging, cbpro
import json_io
from coinbase_pro_tasks import cbpPlaceOrder, cbpGetFiatBalance, cbpTryDepositFromBank, cbpTryWithdrawCrypto

logging.basicConfig(filename='log.txt', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def succeeded(data):
    if "Error" in data and data["Error"] != None:
        logging.error(taskResult.data["Error"])
        return False
    return True

def runTasks(amount):
    auth_info = json_io.getJsonFile("auth.json")
    coinbase_auth_info = auth_info["coinbase"]
    cb_client = cbpro.AuthenticatedClient(coinbase_auth_info["key"], coinbase_auth_info["secret"], coinbase_auth_info["password"])
    settings = json_io.getJsonFile("settings.json")
    
    

#start
if len(sys.argv) != 2:
    print("Usage: python coinbasepro-dca.py [fiat amount]")
else:
    runTasks(int(sys.argv[1]))
