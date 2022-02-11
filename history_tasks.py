import os, csv

def convertData(incoming):
    result = {'id':incoming['id']}

    buying = ''
    selling = ''
    if 'product_id' in incoming:
        products = incoming['product_id'].split("-")
        buying = products[0]
        selling = products[1]
    elif 'fromCurrency' in incoming and 'toCurrency' in incoming:
        buying = incoming['toCurrency']
        selling = incoming['fromCurrency']
    result['buying'] = buying
    result['selling'] = selling

    spent = 0
    if 'specified_funds' in incoming:
        spent = incoming['specified_funds']
    elif 'amountSend' in incoming:
        spent = incoming['amountSend']
    result['spent'] = spent

    received = 0
    if 'filled_size' in incoming:
        received = incoming['filled_size']
    elif 'amountReceive' in incoming:
        received = incoming['amountReceive']
    result['received'] = received

    datetime = ''
    if 'done_at' in incoming:
        datetime = incoming['done_at']
    elif 'depositReceivedAt' in incoming:
        datetime = incoming['depositReceivedAt']
    result['datetime'] = datetime

    return result

def writeHistory(fullPath, data):
    nData = convertData(data)
    isNew = not os.path.exists(fullPath)
    with open(fullPath, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=nData.keys())
        if isNew:
            writer.writeheader()
        writer.writerow(nData)
