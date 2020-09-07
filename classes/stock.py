import os
from decouple import config
import finnhub
import requests
import json


class Stock:
    #Initializer
    def __init__(self, ticker, price, apiKey):
        self.ticker = ticker
        self.price = price
        self.apiKey = apiKey
    
    # Setting returned data from stock quote method
    def set_stock_quote_data(self, data):
        errorMsg = True

        if data == {}:
            return errorMsg
        else:
            data = {
                'currentPrice': str(data['c']),
                'openPrice': str(data['o']),
                'prevClose': str(data['pc']),
                'highPrice': str(data['h']),
                'lowPrice': str(data['l'])
            }
            return data

    def set_company_data(self, data):
        errorMsg = True

        if data == {}:
            return errorMsg
        else:
            data = {
                'Company_Name': data['name'],
                'Company_Country': data['country'],
                'Company_IPO': data['ipo'],
                'Company_Ticker_Symbol': data['ticker'],
                'Company_Website': data['weburl'],
                'Company_Logo': data['logo'],
                'Company_Industry': data['finnhubIndustry']
            }
            return data
            
    #Grabbing stock quote from API - Current Price, Open, Previous Close, High, Low - https://finnhub.io/docs/api#quote
    async def get_stock_quote(self):
        daily_data_query = {'symbol': self.ticker, 'token': self.apiKey}
        res = requests.get('https://finnhub.io/api/v1/quote', params=daily_data_query)
        output = res.json()
        set_data = self.set_stock_quote_data(output)

        return set_data

    #Grabbing stock's company info - https://finnhub.io/docs/api#company-profile2
    async def get_company_profile_data(self):
        company_profile = {'symbol': self.ticker, 'token': self.apiKey}
        res = requests.get('https://finnhub.io/api/v1/stock/profile2', params=company_profile)
        output = res.json()
        set_data = self.set_company_data(output)

        return set_data

        


    