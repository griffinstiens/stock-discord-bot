import os
from discord.ext import commands
from dotenv import load_dotenv
from decouple import config
import finnhub
import requests
# Importing Stock class
from classes.stock import Stock

load_dotenv()
TOKEN = config('DISCORD_TOKEN')
DISCORD_SERVER_NAME = config('DISCORD_NAME')
FINN_API_KEY = config('FINN_KEY')

# Setup Finnhub client
# It took me awhile to realize the line below this is pretty much pointless for what I've been doing
# finnhub_client = finnhub.Client(api_key=FINN_API_KEY)

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
async def grab_stonks(ctx, ticker: str, price = None):
    # Instantiating Stock class
    stocks = Stock(ticker, price, FINN_API_KEY)
    # Returning stock data
    stock_data = await stocks.get_data()

    # Checking for an empty json response from API
    if (stock_data == True):
        await ctx.send("Error: Ticker does not exist")

    #
    currentPrice = str(stock_data['c'])
    openPrice = str(stock_data['o'])
    prevClose = str(stock_data['pc'])
    highPrice = str(stock_data['h'])
    lowPrice = str(stock_data['l'])

    if price == None:
        msg = f'Current Price: {currentPrice}\nOpen: {openPrice}\nPrevious Close: {prevClose}\nHigh: {highPrice}\nLow: {lowPrice}'
        await ctx.send("Loading...")
        await ctx.send(msg)
    elif price == 'current':
        await ctx.send("Current Price: " + currentPrice)
    elif price == 'open':
        await ctx.send("Open Price: " + openPrice)
    elif price == 'close':
        await ctx.send("Previous Close Price: " + prevClose)
    elif price == 'high':
        await ctx.send("Today's High: " + highPrice)
    elif price == 'low':
        await ctx.send("Today's Low: " + lowPrice)
    else:
        await ctx.send(stock_data)

bot.run(TOKEN)
