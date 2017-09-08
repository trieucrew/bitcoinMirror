from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.uix.carousel import Carousel

import requests
import json
import time

coins=['BTC', 'ETH', 'LTC', 'DASH', 'OMG', 'NAV', 'IOT', 'SC', 'STEEM', 'XMR', 'BAT', 'NEO', 'ARK']
currencies=['BTC', 'USD']
apiUrl='https://min-api.cryptocompare.com/data/pricemultifull?'
#placeholder for when the app starts up so it
#Call update every 30 minutes, update then queries the api endpoint for new data and then caluculate
class Stocks():
    def __init__(self):
        self.data={}
        self.rawData=self.query()
        for coin in coins:
            coinName=self.rawData[coin]['USD']
            self.data[coinName['FROMSYMBOL']]={'price': coinName['PRICE'], 'percentage': 0}
        print(self.data)

    def update(self):
        self.rawData = self.query()

        for index, coin in enumerate(coins):
            coinName=self.rawData[coin]['USD']

            #update previous price and current price
            self.previousPrice=self.data[coin]['price']
            self.data[coin]['price']=self.currentPrice=coinName['PRICE']

            self.percentage=(self.currentPrice-self.previousPrice)/self.previousPrice
            self.data[coin]['percentage']=self.percentage

        return self.data

    def toString(self, coin):
        coinName = self.data[coin]
        return 'Price: ' + str(coinName['price']) + ' Percentage: ' + str(coinName['percentage'])


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
    def __init__(self, **kwargs):
        super(CarouselDisplay, self).__init__(**kwargs)

    def update(self):
        data=App.get_running_app().stocks.update()
        print(data)
        labels=App.get_running_app().labels
        stocks=App.get_running_app()
        for coin in coins:
            labels[coin].text=text=coin + ' ' + App.get_running_app().stocks.toString(coin)

    Clock.schedule_interval(partial(update), 30)

class MirrorApp(App):
    stocks=Stocks()
    labels = {}

    def build(self):
        labels=App.get_running_app().labels
        layout=BoxLayout(orientation='vertical')
        carouselDisplay=CarouselDisplay(height=500, width=500)
        carousel = Carousel(direction='right', loop=True)
        for coin in coins:
            labels[coin]=Factory.Label(text=coin + ' ' + App.get_running_app().stocks.toString(coin))
            carousel.add_widget(labels[coin])

        Clock.schedule_interval(carousel.load_next, 3)

        layout.add_widget(carousel)
        layout.add_widget(carouselDisplay)

        return layout

if __name__ == '__main__':
    MirrorApp().run()
    #stock = Stocks()
