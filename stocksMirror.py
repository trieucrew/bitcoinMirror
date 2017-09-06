import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.widget import Widget
from functools import partial
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.uix.carousel import Carousel

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
        global prevPrices
        self.rawData=self.query()
        for coin in coins:
            coinName=self.rawData[coin]['USD']
            prevPrices.append(coinName['PRICE'])
        print(prevPrices)

    def update(self):
        global prevPrices
        self.rawData = self.query()
        pricesAndPercentages=[]

        for index, coin in enumerate(coins):
            coinName=self.rawData[coin]['USD']

            #update previous price and current price
            self.previousPrice=prevPrices[index]
            prevPrices[index]=self.currentPrice=coinName['PRICE']

            self.percentage=(self.currentPrice-self.previousPrice)/self.previousPrice
            pricesAndPercentages.append({'name': str(coinName['FROMSYMBOL']), 'price': self.currentPrice, 'percentage': self.percentage})

        return pricesAndPercentages


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

class CarouselDisplay(Widget):

    def update(self):
        App.get_running_app().data=App.get_running_app().stocks.update()
        print(App.get_running_app().data)

    Clock.schedule_interval(partial(update), 5)

class MirrorApp(App):
    stocks=Stocks()
    data=[]

    def build(self):
        carouselDisplay=CarouselDisplay()
        carousel = Carousel(direction='right', loop=True)
        for i in range(0, 10):
            text = Factory.Label(text=str(i))
            carousel.add_widget(text)

        Clock.schedule_interval(carousel.load_next, 1)
        carouselDisplay.add_widget(carousel)
        return carouselDisplay

if __name__ == '__main__':
    MirrorApp().run()
    #stock = Stocks()
