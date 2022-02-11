import math, os, sys, logging, cbpro
import json_io
from coinbase_pro_tasks import cbpPlaceOrder, cbpGetFiatBalance, cbpTryDepositFromBank, cbpTryWithdrawCrypto
from changenow_tasks import cnStartExchange, cnVerifyExchange
from history_tasks import writeHistory

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__)) + "/"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(SCRIPT_PATH + 'log.txt', 'w', 'utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler(sys.stdout))

def succeeded(data):
    if "Error" in data and data["Error"] != None:
        logging.error(data["Error"])
        return False
    return True

def runTasks(amount):
    auth_info = json_io.getJsonFile("auth.json")
    coinbase_auth_info = auth_info["coinbase"]
    changenow_auth_info = auth_info["changenow"]
    cb_client = cbpro.AuthenticatedClient(coinbase_auth_info["key"], coinbase_auth_info["secret"], coinbase_auth_info["password"])
    settings = json_io.getJsonFile("settings.json")

    result = cbpPlaceOrder(cb_client, settings["transfer_crypto_name"], settings["fiat_name"], amount)
    if not succeeded(result):
        return
    writeHistory(SCRIPT_PATH + "history.csv", result)

    transferCryptoAmount = result["funds"]

    result = cnStartExchange(changenow_auth_info["key"], settings["transfer_crypto_name"], settings["final_crypto_name"], settings["final_crypto_address"], transferCryptoAmount)
    if not succeeded(result):
        return

    cnExchangeId = result["id"]
    cnPayinAddress = result["payinAddress"]
    cnPayinMemo = result["payinExtraId"]

    result = cbpTryWithdrawCrypto(cb_client, settings["transfer_crypto_name"], transferCryptoAmount, cnPayinAddress, cnPayinMemo)
    if not succeeded(result):
        return

    result = cnVerifyExchange(changenow_auth_info["key"], cnExchangeId)
    if not succeeded(result):
        return
    writeHistory(SCRIPT_PATH + "history.csv", result)

    result = cbpGetFiatBalance(cb_client, settings["fiat_name"])
    if not succeeded(result):
        return

    fiatBalance = float(result["balance"])

    if fiatBalance < settings["topup_threshold"]:
        result = cbpTryDepositFromBank(cb_client, settings["fiat_name"], settings["topup_amount"], settings["bank_identifier"])

    logging.info("Finished tasks successfully.")

    return

#start
if len(sys.argv) != 2:
    print("Usage: python coinbasepro-dca.py [fiat amount]")
else:
    try:
        runTasks(int(sys.argv[1]))
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}.")
