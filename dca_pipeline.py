# dependent on Path (pip install pathlib)
# and cbpro (pip install git+git://github.com/Monerovirus/coinbasepro-python.git)

import math, os, sys, logging, cbpro, csv
import json_io
from coinbase_pro_tasks import cbpPlaceOrder, cbpGetFiatBalance, cbpTryDepositFromBank, cbpTryWithdrawCrypto

logging.basicConfig(filename='log.txt', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def succeeded(data):
    if "Error" in data and data["Error"] != None:
        logging.error(data["Error"])
        return False
    return True

def writeToCsv(fileName, data):
    isNew = not os.path.exists(fileName)
    with open(fileName, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        if isNew:
            writer.writeheader()
        writer.writerow(data)

def runTasks(amount):
    auth_info = json_io.getJsonFile("auth.json")
    coinbase_auth_info = auth_info["coinbase"]
    #cb_client = cbpro.AuthenticatedClient(coinbase_auth_info["key"], coinbase_auth_info["secret"], coinbase_auth_info["password"])
    cb_client = cbpro.AuthenticatedClient(coinbase_auth_info["key"], coinbase_auth_info["secret"], coinbase_auth_info["password"], api_url="https://api-public.sandbox.pro.coinbase.com")
    settings = json_io.getJsonFile("settings.json")

#start
if len(sys.argv) != 2:
    print("Usage: python coinbasepro-dca.py [fiat amount]")
else:
    runTasks(int(sys.argv[1]))
