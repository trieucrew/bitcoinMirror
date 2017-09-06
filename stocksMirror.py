from kivy.app import App
from kivy.uix.widget import Widget
import threading
import requests
import json
import time

coins=['BTC', 'ETH', 'LTC', 'DASH', 'OMG', 'NAV', 'IOT', 'SC', 'STEEM', 'XMR', 'BAT', 'NEO', 'ARK']
prevPrices=[]
currencies=['BTC', 'USD']
apiUrl='https://min-api.cryptocompare.com/data/pricemultifull?'
#placeholder for when the app starts up so it
#Call update every 30 minutes, update then queries the api endpoint for new data and then caluculate
class Stocks():
    def __init__(self):
        for coin in coins:
            prevPrices.append(1)
        for i in range(0,3):
            rawData = self.query()

            print("------------" + str(i))
            for index, coin in enumerate(coins):
                self.update(rawData[coin], 'USD', index,)
            print(prevPrices)
            #time.sleep(60)

    def update(self, coin, curr, index):
        global prevPrices
        coin=coin[curr]
        #update previous price and current price
        self.previousPrice=prevPrices[index]
        prevPrices[index]=self.currentPrice=coin['PRICE']

        self.percentage=(self.currentPrice-self.previousPrice)/self.previousPrice
        print('Current Price for ' + coin['FROMSYMBOL'] + ': ' + str(self.currentPrice))
        print('Percentage: ' + str(self.percentage))


    def query(self):
        url=self.concatenateReqURL(apiUrl)
        req=requests.get(url)
        response=json.loads(req.text)
        return response['RAW'] #return the raw data

    def concatenateReqURL(self, url):
        fromSymbs='fsyms'
        toSymbs='tsyms'
        #concatenate the coin symbols
        url=url+fromSymbs+'='
        for index, coin in enumerate(coins):
            if index==len(coins)-1:
                url=url+coin+'&'
                break
            url=url+coin+','
        #concatenate the currency symbols
        url=url+toSymbs+'='
        for index, currency in enumerate(currencies):
            if index==len(currencies)-1:
                url=url+currency
                break
            url=url+currency+','
        return url

class CoinDisplay(Widget):
    stocks = Stocks()
    pass

class MirrorApp(App):
    def build(self):
        return CoinDisplay()

if __name__ == '__main__':
    MirrorApp().run()
    #stock = Stocks()
