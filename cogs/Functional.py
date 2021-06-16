# Import statements
from discord.ext import tasks
import random
import discord.utils
from other.CommonBotFunctions import *

# Variables
statuses = []


class Functional(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Other
    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(random.choice(statuses)))

    # Events
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        # do some extra stuff here
        if message.author is not self.client.user:
            with open('jsons/dumbPeople.json', 'r') as file:
                dumb_people = json.load(file)

            if str(message.author.id) + str(message.guild.id) in dumb_people:
                await message.delete()

            if not is_banned(message) and not channel_banned(message):
                if message.content.lower() == 'hello' or message.content.lower() == 'こんにちは':
                    await message.channel.send(f'Hello {message.author.display_name}!')

                return
        else:
            return

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as: {self.client.user}\nDiscord.py version: {discord.__version__}\n')
        self.change_status.start()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not is_banned(ctx) and not channel_banned(ctx):
            if isinstance(error, commands.UserInputError):
                await ctx.send(f'{ctx.author.display_name} please pass in correct arguments. For more information, '
                               f'use >help '
                               f'\'command\'.')
            if isinstance(error, commands.MissingPermissions):
                await ctx.send(f'**{ctx.author.display_name}**, you do not have the required permissions for that '
                               f'command.')
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f'**{ctx.author.display_name}**, this command is on cooldown for you!')

    # Commands
    @commands.command(help='Returns the bot\'s ping')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ping(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.send(f'Latency: {int(self.client.latency * 1000)} ms.')

    @commands.command(help='Clears the specified number of messages (defaults to 5)')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def clear(self, ctx, amount: int = 5):
        if not is_banned(ctx) and not channel_banned(ctx) and is_superuser_or_admin(ctx.author):
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f'Cleared {amount} messages.')

    @commands.command(aliases=['dm'], help='dm\'s the specified user with the specified message')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def direct_message(self, ctx, messagee: discord.Member, *, message):
        if not is_banned(ctx) and not channel_banned(ctx) and is_superuser_or_admin(ctx.author):
            await messagee.send(message)
            await ctx.send(f':upside_down: {ctx.author.display_name} sent!')



    @commands.command(help='Changes the prefix for the bot on the server')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def change_prefix(self, ctx, new_prefix):
        if not is_banned(ctx) and not channel_banned(ctx) and is_superuser_or_admin(ctx.author):
            with open('jsons/prefixes.json', 'r') as file:
                prefixes = json.load(file)

            prefixes[str(ctx.guild.id)] = new_prefix

            with open('jsons/prefixes.json', 'w') as file:
                json.dump(prefixes, file, indent=4)

            await ctx.send(f'Server prefix changed to \'{prefix}\'')

    @commands.command(help='Gives a votable message with the content provided')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def vote(self, ctx, *, question):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.channel.purge(limit=1)
            op_msg = discord.Embed(
                description=f'{question}',
                color=discord.Color.purple()
            )
            message = await ctx.send(embed=op_msg)
            await message.add_reaction('❎')
            await message.add_reaction('✅')




    @commands.command(help='Returns the discord ID of the targeted user', aliases=['checkid'])
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def check_id(self, ctx, target: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.send(f'{target.display_name}\'s discord id is {target.id}')




    @commands.command(help='Bans a user from using the bot')
    async def ban(self, ctx, target: discord.User):
        if not is_banned(ctx) and not channel_banned(ctx) and is_owner(ctx):
            with open('jsons/banned.json', 'r') as file:
                banned_users = json.load(file)

            banned_users.append(str(target.id))

            with open('jsons/banned.json', 'w') as file:
                json.dump(banned_users, file, indent=4)

            await ctx.send(f'{ctx.author.display_name}, {target.display_name} can no longer use me.')
        else:
            await ctx.send(f'{ctx.author.display_name} you cannot do this.')

    @commands.command(help='Unbans a user from using the bot')
    async def unban(self, ctx, target: discord.User):
        if not is_banned(ctx) and not channel_banned(ctx) and is_owner(ctx):
            with open('jsons/banned.json', 'r') as file:
                banned_users = json.load(file)

            banned_users.remove(str(target.id))

            with open('jsons/banned.json', 'w') as file:
                json.dump(banned_users, file, indent=4)

            await ctx.send(f'{ctx.author.display_name}, {target.display_name} can now use me again.')
        else:
            await ctx.send(f'{ctx.author.display_name} you cannot do this.')

    @commands.command(help='Bans a text channel from using the bot')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ban_channel(self, ctx, target: discord.TextChannel):
        if not is_banned(ctx) and not channel_banned(ctx) and is_superuser_or_admin(ctx.author):
            with open('jsons/bannedChannels.json', 'r') as file:
                banned_users = json.load(file)

            banned_users.append(str(target.id))

            with open('jsons/bannedChannels.json', 'w') as file:
                json.dump(banned_users, file, indent=4)

            ban_msg = discord.Embed(
                description=f'{ctx.author.display_name}, I can no longer be used in {target.name}.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=ban_msg)

    @commands.command(help='Unbans a text channel from using the bot')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unban_channel(self, ctx, target: discord.TextChannel):
        if not is_banned(ctx) and not channel_banned(ctx) and is_superuser_or_admin(ctx.author):
            with open('jsons/bannedChannels.json', 'r') as file:
                banned_users = json.load(file)

                banned_users.remove(str(target.id))

            with open('jsons/bannedChannels.json', 'w') as file:
                json.dump(banned_users, file, indent=4)

            ban_msg = discord.Embed(
                description=f'{ctx.author.display_name}, I now usable in {target.name}.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=ban_msg)



    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def guild_info(self, ctx, limit=5):
        if is_superuser_or_admin(ctx.author):
            async for entry in ctx.guild.audit_logs(limit=limit):
                embed = discord.Embed(
                    title=f'**User**: {entry.user}',
                    description=f'**Action:** {entry.action}\n**target**: {entry.target}\n'
                                f'**Reason**: {entry.reason}\n**Extras:** {entry.extra}\n**Time:** {entry.created_at}\n'
                                f'**Was:** {entry.before}\n**Is:** {entry.after}',
                    color=discord.Color.purple()
                )
                await ctx.author.send(embed=embed)

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def guild_info_user(self, ctx, user: discord.Member, limit=5):
        if is_superuser_or_admin(ctx.author):
            async for entry in ctx.guild.audit_logs(limit=limit, user=user):
                embed = discord.Embed(
                    title=f'**User**: {entry.user}',
                    description=f'**Action:** {entry.action}\n**target**: {entry.target}\n'
                                f'**Reason**: {entry.reason}\n**Extras:** {entry.extra}\n**Time:** {entry.created_at}\n'
                                f'**Was:** {entry.before}\n**Is:** {entry.after}',
                    color=discord.Color.purple()
                )
                await ctx.author.send(embed=embed)

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def guild_info_action(self, ctx, action=None, limit=5):
        if is_superuser_or_admin(ctx.author):
            async for entry in ctx.guild.audit_logs(limit=limit, action=action):
                embed = discord.Embed(
                    title=f'**User**: {entry.user}',
                    description=f'**Action:** {entry.action}\n**target**: {entry.target}\n'
                                f'**Reason**: {entry.reason}\n**Extras:** {entry.extra}\n**Time:** {entry.created_at}\n'
                                f'**Was:** {entry.before}\n**Is:** {entry.after}',
                    color=discord.Color.purple()
                )
                await ctx.author.send(embed=embed)

    @commands.command(hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.guild_only()
    async def list_roles(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            list_of_roles = ctx.author.roles
            for i in range(len(list_of_roles)):
                if i != 0:
                    await ctx.send(f'{i}: {list_of_roles[i]}')

    @commands.command(hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.guild_only()
    async def remove_role(self, ctx, element_number: int):
        if not is_banned(ctx) and not channel_banned(ctx):
            list_of_roles = ctx.author.roles
            if element_number > len(list_of_roles):
                await ctx.send(f'You must use the number of a role you have. To see these, use the list_roles command!')
                return
            await ctx.author.remove_roles(list_of_roles[element_number])
            await ctx.send(f'Done!')

    @commands.command(hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.guild_only()
    async def funny(self, ctx, target: discord.Member, reason: str):
        if ctx.author.id == 763462011869986871:
            await ctx.guild.ban(target, reason=reason)
            await ctx.send(f'Done!')

            
    @commands.command(aliases=['powercheck'], help='Check if you are either a superuser or an admin')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def power_check(self, ctx, member: discord.Member = ''):
        if not is_banned(ctx) and not channel_banned(ctx):
            if member == '':
                member = ctx.author
                if is_superuser_or_admin(member):
                    await ctx.send('You do have superuser or admin')
                else:
                    await ctx.send('You do not have superuser or admin')
            else:
                if is_superuser_or_admin(member):
                    await ctx.send(f'{member.display_name} does have superuser or admin')
                else:
                    await ctx.send(f'{member.display_name} does not have superuser or admin')

    @commands.command(help='Makes the mentioned user a superuser', aliases=['superuser'])
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def super_user(self, ctx, member: discord.Member):
        if is_owner(ctx):
            user = User(member)
            user.super_user()
            user.save()
        else:
            if not is_banned(ctx) and not channel_banned(ctx):
                await ctx.send(f'{ctx.author.mention} you may not use this command.')


def setup(client):
    client.add_cog(Functional(client))
