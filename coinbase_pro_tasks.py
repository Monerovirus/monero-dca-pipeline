import json, logging, time

def cbpVerifyOrder(client, orderId):
    tryCount = 0
    retryCount = 15
    waitSeconds = 10
    result = None
    while tryCount < retryCount:
        result = client.get_order(orderId)
        if "status" in result and result["status"] == "done" and float(result["filled_size"]) > 0:
            logging.info(f"Verified order {orderId} was filled.")
            return result
        elif retryCount-1 > 0:
            if "status" in result or ("message" in result and result["message"] == "NotFound"):
                time.sleep(waitSeconds)
                tryCount += 1
                continue
        return {"Error": f"Failed to get order {orderId}.\n {result}"}
    
    return {"Error": f"Failed to verify order after {retryCount} tries.\n{result}"}

def cbpPlaceOrder(client, cryptoName, fiatName, amount):
    logging.info(f"Ordering ({fiatName}){str(amount)} of {cryptoName}")
    result = client.place_market_order(product_id=f"{cryptoName}-{fiatName}", side="buy", funds=amount)
    if "specified_funds" in result and "funds" in result:
        spentAmountFiat = result["specified_funds"]
        filledAmountFiat = result["funds"]
        logging.info(f"Successfully placed order for ({fiatName}){str(filledAmountFiat)} of {cryptoName}")
        return cbpVerifyOrder(client, result["id"])
    
    return {"Error":f"Unexpected result after placing order:\n{result}"}

def cbpGetFiatBalance(client, fiatCurrency):
    logging.info(f"Getting {fiatCurrency} balance.")
    result = client.get_accounts()
    if isinstance(result, list):
        for account in result:
            if account["currency"] == fiatCurrency:
                balance = round(float(account["balance"]), 2)
                logging.info(f"{fiatCurrency} balance is: {str(balance)}.")
                return account
        return {"Error": f"Unable to find account for currency {fiatCurrency}."}
    return {"Error": f"Error getting accounts:\n{result}"}


def cbpGetBankId(client, bankIdentifier):
    result = client.get_payment_methods()
    for bank in result:
        if bankIdentifier in bank["name"]:
            logging.info("Using payment method: " + bank["name"])
            return bank["id"]
    return {"Error": f"Unable to find payment method using bank identifier {bankIdentifier}."}

def cbpVerifyTransfer(client, transferId, retryCount, waitSeconds):
    tryCount = 0
    result = None
    while tryCount < retryCount:
        logging.debug(f"Attempting verify transfer {transferId}")
        result = client.get_transfer(transferId)
        if "completed_at" in result and "canceled_at" in result:
            if result["canceled_at"] != None:
                canceledAt = response["canceled_at"]
                return {"Error":f"Transfer {transferId} canceled at {canceledAt}."}
            elif result["completed_at"] == None:
                logging.debug(f"Transfer {transferId} still in progress.")
            else:
                completedAt = result["completed_at"]
                logging.info(f"Transfer {transferId} completed at {completedAt}")
                return result
        tryCount += 1
        time.sleep(waitSeconds)
    return {"Error": f"Could not verify deposit after {retryCount} tries.\n{result}"}

def cbpTryDepositFromBank(client, fiatCurrency, amount, bankIdentifier):
    bankId = cbpGetBankId(client, bankIdentifier)
    if "Error" in bankId:
        return bankId
    
    logging.info(f"Requesting deposit for {amount} of {fiatCurrency}.")
    result = client.deposit(amount, fiatCurrency, bankId)
    
    if "amount" in result and "id" in result:
        depositedAmount = str(result["amount"])
        logging.info(f"Successfully requested deposit for {depositedAmount} of {fiatCurrency} into Coinbase Pro.")
        return cbpVerifyTransfer(client, result["id"], 15, 10)
    else:
        return {"Error": f"Deposit failed. {result}"}

def cbpGetAccountId(client, cryptoName):
    result = client.get_accounts()
    for group in result:
        if "currency" in group and group["currency"] == cryptoName:
            return group["id"]
    
    return {"Error": f"Unable to get account id for currency {cryptoName}."}

def cbpTryWithdrawCrypto(client, cryptoName, amount, destinationAddress, destinationMemo):
    logging.info(f"Withdrawing {amount} {cryptoName} to address {destinationAddress}.")
    result = client.crypto_withdraw(amount, cryptoName, destinationAddress, destinationMemo)
    if "amount" in result and "id" in result:
        withdrawnAmount = str(result["amount"])
        logging.info(f"Successfully initiated withdrawal for {withdrawnAmount} of {cryptoName} to address {destinationAddress}.")
        return cbpVerifyTransfer(client, result["id"], 45, 120)
    
    return {"Error":f"Withdrawal request failed.\n{result}"}
