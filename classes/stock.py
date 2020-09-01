import os
from decouple import config
import finnhub
import requests
from discord.ext import commands

class Stock:
    #Initializer
    def __init__(self, ticker, price, apiKey):
        self.ticker = ticker
        self.price = price
        self.apiKey = apiKey
    
    #Grabbing data from API, formatting and returning
    async def get_data(self):
        query = {'symbol': self.ticker, 'token': self.apiKey}
        res = requests.get('https://finnhub.io/api/v1/quote', params=query)
        output = res.json()

        errorMsg = True

        if output == {}:
            return errorMsg
        else:
            return output


    


        
