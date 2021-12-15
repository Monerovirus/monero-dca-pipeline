# dependent on Path (pip3 install pathlib)
# and cbpro (pip3 install git+git://github.com/Monerovirus/coinbasepro-python.git)

import math, os, sys, logging, cbpro, csv
import json_io
from coinbase_pro_tasks import cbpPlaceOrder, cbpGetFiatBalance, cbpTryDepositFromBank, cbpTryWithdrawCrypto

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(SCRIPT_PATH + 'log.txt', 'w', 'utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler(sys.stdout))

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__)) + "/"

def succeeded(data):
    if "Error" in data and data["Error"] != None:
        logging.error(data["Error"])
        return False
    return True

def writeToCsv(SCRIPT_PATH + fileName, data):
    isNew = not os.path.exists(fileName)
    with open(fileName, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        if isNew:
            writer.writeheader()
        writer.writerow(data)

def runTasks(amount):
    auth_info = json_io.getJsonFile("auth.json")
    coinbase_auth_info = auth_info["coinbase"]
    cb_client = cbpro.AuthenticatedClient(coinbase_auth_info["key"], coinbase_auth_info["secret"], coinbase_auth_info["password"])
    settings = json_io.getJsonFile("settings.json")

#start
if len(sys.argv) != 2:
    print("Usage: python coinbasepro-dca.py [fiat amount]")
else:
    try:
        runTasks(int(sys.argv[1]))
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}.")
