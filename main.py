#imports

import discord
import os
import keepBotAlive
from discord.ext import commands
import logging
import json
from other import CommonBotFunctions

keepBotAlive.awake()


#declarations 

with open(${{secret.TOKEN}}', 'r') as DISCORD_TOKEN:
    token = DISCORD_TOKEN.read()
intents = discord.Intents.default()
intents.members = True
logging.basicConfig(level=logging.INFO)

# Prefix and Help Command
def get_prefix(bot, message):
    with open('jsons/prefixes.json', 'r') as file:
        prefixes = json.load(file)

    if bot.user.id == 854023329039908884:
        return commands.when_mentioned_or('^')(bot, message)
    else:
        try:
            return commands.when_mentioned_or(prefixes[str(message.guild.id)])(bot, message)
        except KeyError:
            return commands.when_mentioned_or('>')(bot, message)


class EmbeddedHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, color=discord.Color.purple())
            await destination.send(embed=emby)


client = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=EmbeddedHelp())


# Events
@client.event
async def on_guild_join(guild):
    with open('jsons/prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(guild.id)] = '>'

    with open('jsons/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)

@client.event
async def on_message(message):
    if message.author == client.user: 
      
      #dont respond to a message sent by the bot. 
        return

    if(message.content.startswith('!sleep')):

      resp = "YOU PROMISED ME FLESH!"
      await message.channel.send(resp)

    if(message.content.startswith('!awaken')):
      
      resp = "WHY DO YOU AWAKEN ME WITHOUT SKIN!"
      await message.channel.send(resp)

    if(message.content.startswith ('!forceskip')):

      resp = "WHAT THE HELL FARTOO?"

      await message.channel.send(resp)

    if(message.content.startswith('!jediparty')):
      
      resp = "LOOK MASTER, GIRLS!"
      await message.channel.send(resp)




    if client.user.mentioned_in(message) and 'what time is it?' in message.content:
            await message.channel.send("IT'S BABY TIME!")
        
    elif client.user.mentioned_in(message):
            await message.channel.send("I WILL WEAR YOUR FACE!")
    

    word_list = ['creepio', 'shit', 'fuck', 'fucking', 'bitch', 'shed', 'fairway', 'cunt']
    messageContent = message.content
    
    if len(messageContent) > 0:
      for word in word_list:
        if word in messageContent:

          await message.channel.send (message.author.mention + "YOU ARE THE SINGLE GREATEST DISAPPOINTMENT OF MY ENTIRE LIFE!")

    if '!pause' in messageContent:
      await message.channel.send("Don't Ruin My Flow," + message.author.mention)

    if 'tinder' in messageContent:
      await message.channel.send("BEHOLD! THE SINGULARITY ENGINE!!!")
    
    name_list = ['Kiwi', 'kiwi', 'katie', 'Katie']
    messageContent = message.content

    if len(messageContent) > 0:
      for name in name_list:
        if name in messageContent:
          
          await message.channel.send("NOSEBLASTING!? YOU'RE CRAZY!")

    if 'the maine' in messageContent:
      
      resp = (message.author.mention + "YOU WANT ME TO FEEL THE PAIN, YOU WANT ME TO UNDERSTAND IT SO THAT I MAY SHOW OTHERS!")
      await message.channel.send(resp)         
        

@client.event
async def on_guild_remove(guild):
    with open('jsons/prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes.pop(str(guild.id))

    with open('jsons/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


# Commands
@client.command(hidden=True)
async def load(ctx, extension):
    if ctx.author.id == 763462011869986871:
        client.load_extension(f'cogs.{extension}')

        load_message = discord.Embed(
            description=f'Loaded {extension}',
            color=discord.Color.yellow()
        )
        await ctx.send(embed=load_message)


@client.command(hidden=True)
async def unload(ctx, extension):
    if ctx.author.id == 763462011869986871:
        client.unload_extension(f'cogs.{extension}')

        unload_message = discord.Embed(
            description=f'Unloaded {extension}',
            color=discord.Color.purple()
        )
        await ctx.send(embed=unload_message)


@client.command(hidden='true', help='Makes bot unusable')
async def deactivate(ctx):
    if ctx.author.id == 763462011869986871:
        for fn in os.listdir('./cogs'):
            if fn.endswith('.py'):
                client.unload_extension(f'cogs.{fn[:-3]}')

        await ctx.send(f'YOU PROMISED ME FLESH!')
    else:
        if not CommonBotFunctions.is_banned(ctx) and not CommonBotFunctions.channel_banned(ctx):
            await ctx.send(f'{ctx.author.mention} you may not use this command.')


@client.command(hidden='true', help='Makes bot usable')
async def activate(ctx):
    if ctx.author.id == 763462011869986871:
        for fn in os.listdir('./cogs'):
            if fn.endswith('.py'):
                client.load_extension(f'cogs.{fn[:-3]}')

        await ctx.send(f'WHY DO YOU AWAKEN ME WITHOUT SKIN!?')
    else:
        if not CommonBotFunctions.is_banned(ctx) and not CommonBotFunctions.channel_banned(ctx):
            await ctx.send(f'{ctx.author.mention} you may not use this command.')


# Running the client
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)
