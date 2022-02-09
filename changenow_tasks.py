import json, logging, time, requests

api_url = "https://api.changenow.io/v1/transactions/"

def get(url):
    r = requests.get(url)

    if r.status_code == 200:
        return r.json()
    else:
        return {"Error": f"Status code {str(r.status_code)}."}

def post(url, body=None):
    if body is None:
        body = {}
    json_data = json.dumps(body)
    r = requests.post(url, data=json_data)

    if r.status_code == 200:
        return r.json()
    else:
        return {"Error": f"Status code {str(r.status_code)}."}

def cnVerifyExchange(apiKey, idString):
    url = api_url + idString + "/" + apiKey

    return get(url)

def cnStartExchange(apiKey, fromName, toName, address, amount, extraId='', refundAddress='', refundExtraId='', email=''):
    url = api_url + apiKey

    transaction_data = {
            'from': fromName,
            'to': toName,
            'address': address,
            'amount': amount,
            'extraId': extraId,
            'refundAddress': refundAddress,
            'refundExtraId': refundExtraId,
            'userId': '',
            'payload': {},
            'contactEmail': email
        }


    logging.info(f"Starting exchange of {str(amount)} {fromName} for {toName}.")

    result = post(url, transaction_data)
    if "Error" in result:
        return result

    recieveAmount = result["amount"]
    resultFrom = result["fromCurrency"]
    resultTo = result["toCurrency"]
    logging.info(f"Successfully started exchange from {str(amount)} {resultFrom} to {str(recieveAmount)} {resultTo}.")
    return result
