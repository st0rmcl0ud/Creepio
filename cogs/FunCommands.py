# Import statements
import random
from other.CommonBotFunctions import *


class FunCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(help='You kill either another person or yourself')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def kill(self, ctx, target: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            self_kill_messages = ['decided to off themselves.', 'has transcended existence.', 'wants to try making toast in a bath.', 'is holding a thermal detonator.']
            kill_messages = ['shoots', 'force chokes', 'runs over', 'hired Cad Bane to kill', 'hired Asajj Ventress to kill', 'hired Boba Fett to kill', 'executed order 66 on']

            if target == ctx.author:
                await ctx.send(f'{ctx.author.display_name} {random.choice(self_kill_messages)}')
            else:
                await ctx.send(f'{ctx.author.display_name} {random.choice(kill_messages)} {target.display_name}.')

    @commands.command(help='Says what you want it to, add "-hide" to hide your message')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def say(self, ctx, *, speechbubble):
        if not is_banned(ctx) and not channel_banned(ctx):
            if speechbubble.endswith('-hide'):

                hiddenspeechbubble = speechbubble[:-5]

                await ctx.message.delete()

                await ctx.send(hiddenspeechbubble)
            else:
                await ctx.send(speechbubble)


    @commands.command(help='Decides whether you or the specifed user are superior')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def superior(self, ctx, superioree: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            is_sup = ['is literally superior to', 'falsely believes they\'re superior to']

            await ctx.send(f'{ctx.author.display_name} {random.choice(is_sup)} {superioree.display_name}')

    @commands.command(help='Quotes Master Yoda')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def quote(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            yoda_quotes = [ 'Fear is the path to the Darkside. Fear leads to anger, anger leads to hate, hate leads to suffering.', 'In a dark place we find ourselves, and a little more knowledge lights the way', 'Train yourself to let go of everything you fear to lose.', 'Death is a natural part of life. Rejoice for those around you who transform into the force. Mourn them do not. Miss them do not. Attachment leads to jealousy. The shadow of greed, that is.', 'Do or do not. There is no try.', 'Many of the truths that we cling to depend on our point of view.', 'If no mistake you have made, losing you are. A different game you should play.']

            yoda_quote = discord.Embed(
                description=random.choice(yoda_quotes),
                color=discord.Color.green()
            )
            await ctx.send(embed=yoda_quote)

   

    @commands.command(help='Press F to pay respects (target optional)')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def f(self, ctx, *, target=''):
        if not is_banned(ctx) and not channel_banned(ctx):
            if target == '':
                f_message = f'Press f to pay respects'
            else:
                f_message = f'Press f to pay respects to {target}'

            message = await ctx.send(embed=f_message)
            await message.add_reaction('🇫')


    @commands.command(help='Does nothing')
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.guild_only()
    async def nothing(self, ctx):
        return

    @commands.command(aliases=['dumbfucker'], help='The specified user is dumb asf')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def dumb_fucker(self, ctx, bad_person: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.send(f'{bad_person.display_name} is one dumb motherfucker.')




def setup(client):
    client.add_cog(FunCommands(client))
