#imports

import discord
import os
import keepBotAlive
from discord.ext import commands
import logging
import json
from other import CommonBotFunctions



#declarations 

with open('token.txt', 'r') as DISCORD_TOKEN:
    token = DISCORD_TOKEN.read()
intents = discord.Intents.default()
intents.members = True
logging.basicConfig(level=logging.INFO)
