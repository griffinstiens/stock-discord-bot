import os
from discord.ext import commands
from dotenv import load_dotenv
from decouple import config
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import finnhub
import requests

load_dotenv()
TOKEN = config('DISCORD_TOKEN')
DISCORD_SERVER_NAME = config('DISCORD_NAME')
FINN_API_KEY = config('FINN_KEY')

# Setup Finnhub client
finnhub_client = finnhub.Client(api_key=FINN_API_KEY)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Sup {member.name}...little bitch'
    )

# !stonk [ticker] - open, close data
@bot.command(name='stonk')
async def grab_stonk_history(ctx, ticker: str, price = None):
    # user will pass ticker name
    # need a check to make sure it exists

    query = {'symbol': ticker, 'token': FINN_API_KEY}
    res = requests.get('https://finnhub.io/api/v1/quote', params=query)

    output = res.json()

    if output == {}:
        await ctx.send("Ticker not found - Please try again")
    
    currentPrice = str(output['c'])
    openPrice = str(output['o'])
    prevClose = str(output['pc'])
    highPrice = str(output['h'])
    lowPrice = str(output['l'])

    if price == None:
        msg = f'Current Price: {currentPrice}\nOpen: {openPrice}\nPrevious Close: {prevClose}\nHigh: {highPrice}\nLow: {lowPrice}'
        await ctx.send("Loading...")
        await ctx.send(msg)
    elif price == 'current':
        print(ticker)
        await ctx.send("Current Price: " + str(output['c']))
    elif price == 'open':
        await ctx.send("Open Price: " + str(output['o']))
    elif price == 'close':
        await ctx.send("Previous Close Price: " + str(output['pc']))
    elif price == 'high':
        await ctx.send("Today's High: " + str(output['h']))
    elif price == 'low':
        await ctx.send("Today's Low: " + str(output['l']))
    else:
        await ctx.send(output)



bot.run(TOKEN)
