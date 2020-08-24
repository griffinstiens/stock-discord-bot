import os

from discord.ext import commands
from dotenv import load_dotenv
from decouple import config

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

@bot.command(name='stonks')
async def grab_stonks(ctx):
    message = 'We aint there yet but the bot responds to the command YEET'

    response = message
    await ctx.send(response)




# @bot.event
# async def on_error(event, *args, **kwargs):
#     with open('err.log', 'a') as f:
#         if event == 'on_message':
#             f.write(f'Unhandled message: {args[0]}\n')
#         else:
#             raise



bot.run(TOKEN)
