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
