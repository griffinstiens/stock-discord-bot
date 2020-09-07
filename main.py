import os
from discord.ext import commands
from discord import Embed
from dotenv import load_dotenv
from decouple import config
import finnhub
import requests
import json
from tabulate import tabulate
# Importing Stock class
from classes.stock import Stock
import websocket

load_dotenv()
TOKEN = config('DISCORD_TOKEN')
DISCORD_SERVER_NAME = config('DISCORD_NAME')
FINN_API_KEY = config('FINN_KEY')

# Setting command prefix
bot = commands.Bot(command_prefix='!')

# Outputs success message to terminal on successful connection of bot to server
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# When member joins, bot will DM a little message
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Sup {member.name}...Welcome to the resistance'
    )


# !stonk [ticker] - open, close data
@bot.command(name='stonk')
async def get_stock_quote(ctx, ticker, price = None):
    # Instantiating Stock class
    stocks = Stock(ticker, price, FINN_API_KEY)
    # Returning stock data
    stock_quote = await stocks.get_stock_quote()
    

    # Response when only a ticker is passed to the bot command
    default_msg = (tabulate([[
        "Current Price","Open","Previous Close","High","Low"
        ],
            [stock_quote['currentPrice'],
            stock_quote['openPrice'],
            stock_quote['prevClose'],
            stock_quote['highPrice'],
            stock_quote['lowPrice']]], 
                headers="firstrow"))

    if price == None:
        await ctx.send("Loading...")
        await ctx.send(f'```{default_msg}```')
    elif price == 'current':
        await ctx.send("Current Price: " + stock_quote['currentPrice'])
    elif price == 'open':
        await ctx.send("Open Price: " + stock_quote['openPrice'])
    elif price == 'close':
        await ctx.send("Previous Close Price: " + stock_quote['prevClose'])
    elif price == 'high':
        await ctx.send("Today's High: " + stock_quote['highPrice'])
    elif price == 'low':
        await ctx.send("Today's Low: " + stock_quote['lowPrice'])
    else:
        await ctx.send(stock_quote)

@bot.command(name='company_info')
async def get_company_profile(ctx, ticker, price = None):

    stocks = Stock(ticker, price, FINN_API_KEY)
    company_profile = await stocks.get_company_profile_data()
    # print(company_profile)

    companyName = 'Company Name: ' + company_profile['Company_Name']
    companyCountry = 'Country: ' + company_profile['Company_Country']
    companyIPO = 'IPO: ' + company_profile['Company_IPO']
    companyTicker = 'Ticker Symbol: ' + company_profile['Company_Ticker_Symbol']
    companyWebsite = 'Website: ' + company_profile['Company_Website']
    companyIndustry = 'Industry: ' + company_profile['Company_Industry']
    companyLogo = company_profile['Company_Logo']
    logo = Embed()
    logo.set_image(url=companyLogo)

    profile_msg = companyName + "\n" + companyCountry + "\n" + companyIPO + "\n" + companyTicker + "\n" + companyWebsite + "\n" + companyIndustry

    await ctx.send(embed=logo)
    await ctx.send(f'```{profile_msg}```')



@bot.command(name='web-socket')
async def websocket_test(ctx):
  
    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={FINN_API_KEY}")
    ws.send('{"type":"subscribe","symbol":CRWD')
    
    ws.on_open = on_open
    ws.run_forever()

    await ctx.send(ws)





bot.run(TOKEN)
