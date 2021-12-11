from binance import Client,ThreadedWebsocketManager, ThreadedDepthCacheManager
import config, requests, json, requests
from bs4 import BeautifulSoup

# Getting data from Binance
def getDataFromBinance(apiKey, secretKey,coin):
    client = Client(apiKey, secretKey)
    tickers = client.get_all_tickers()
    price = 0.0
    for i in tickers:
        if(i['symbol'] == coin):
            price = i['price']
            break
    return float(price)

# Getting data from Bank
def getDataFromBank(url,dataType): # BUYING or SELLING
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    soupIndex = soup.find_all('span')

    buying = soupIndex[4]
    buying = str(buying).translate({ord(i): None for i in '<span>/ TL'})
    buying = buying.replace(',','.')
    buying = float(buying)

    selling = soupIndex[5]
    selling = str(selling).translate({ord(i): None for i in '<span>/ TL'})
    selling = selling.replace(',','.')
    selling = float(selling)

    if dataType == 'BUYING':
        return buying
    elif dataType == 'SELLING':
        return selling

#print(getDataFromBank(config.BANK_URL,'SELLING'))
#print(getDataFromBinance(config.BINANCE_API,config.BINANCE_SECRET,config.BINANCE_COIN))
#getCoinList()
#getDataFromBtc()