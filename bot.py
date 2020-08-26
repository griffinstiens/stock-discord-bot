import os

from discord.ext import commands
from dotenv import load_dotenv
from decouple import config
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime

load_dotenv()
TOKEN = config('DISCORD_TOKEN')
DISCORD_SERVER_NAME = config('DISCORD_NAME')

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

# @bot.event
# async def on_message(message):
#     if message.author == client.user:
#         return

    # stonk_response = 'we aint ready yet bruv'

    # if message.content == '!stonks':
    #     response = stonk_response
    #     await message.channel.send(response)
    # elif message.content == 'raise-exception':
    #     raise discord.DiscordException

# !stonk [ticker] - open, close data
@bot.command(name='stonk')
async def grab_stonk_history(ctx, ticker: str):
    # user will pass ticker name
    # need a check to make sure it exists
    data = yf.download({ticker}, start="2020-08-01")
    if data.empty == True:
        response = "That ticker doesn't exist --- Please enter a valid ticker symbol"
        await ctx.channel.send(response)
        return
    data_info = data.info()

    open_cost = data.Open
    close_cost = data.Close

    await ctx.send(open_cost)

# @bot.event
# async def on_error(event, *args, **kwargs):
#     with open('err.log', 'a') as f:
#         if event == 'on_message':
#             f.write(f'Unhandled message: {args[0]}\n')
#         else:
#             raise
       

bot.run(TOKEN)