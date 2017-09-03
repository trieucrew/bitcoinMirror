from Tkinter import *
import threading
import requests
import json

coins=['BTC', 'ETH', 'LTC', 'DASH', 'OMG', 'NAV', 'IOT', 'SC', 'STEEM', 'XMR', 'BAT', 'NEO', 'ARK']
currencies=['BTC', 'USD']
apiUrl='https://min-api.cryptocompare.com/data/pricemultifull?'

#Call update every 30 minutes, update then queries the api endpoint for new data and then caluculate
class Stocks(Frame):
    def __init__(self):
        #Frame.__init__(self, parent, bg='black')
        rawData = self.query()
        for coin in coins:
            self.update(rawData[coin])
            break
        print(rawData)

    def update(self, coin):
        previousPrice=currentPrice
        currentPrice=coin['PRICE']
        percentageInc=currentPrice-previousPrice/previousPrice
        #get previous price
        #current price - previous price/ previous price = %increase or decrease
        #display current price
        pass

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

class FullScreenWindow:
    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background='black')
        self.bottomFrame = Frame(self.tk, background='black')
        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.mimimize)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def mimimize(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    stock = Stocks()
