import fortnitepy
from discord.ext import commands
import discord

discord_bot = commands.Bot(
    command_prefix='!',
    description='My discord + fortnite bot!',
    case_insensitive=True
)

fortnite_client = fortnitepy.Client(
    email='',
    password='',
    loop=discord_bot.loop
)

@discord_bot.event
async def on_ready():
    print('Discord bot ready')
    activity = discord.Game(name="fortnite.py")
    await discord_bot.change_presence(status=discord.Status.idle, activity=activity)
    await fortnite_client.start()

@fortnite_client.event
async def event_ready():
    print('Fortnite client ready')

@discord_bot.event
async def on_message(message):
    print('Received message from {0.author.display_name} | Content "{0.content}"'.format(message))
    if message.content == "!stats":
        await fetch_profile(TrapxPlug, cache=True, raw=False)

@fortnite_client.event
async def event_friend_message(message):
    print('Received message from {0.author.display_name} | Content "{0.content}"'.format(message))
    await fetch_profile(TrapxPlug, cache=True, raw=False)
    
# discord command
@discord_bot.command()
async def mycommand(ctx):
    await ctx.send('Hello there!')

@commands.command()
async def test(ctx, arg):
    await ctx.send(arg)

@discord_bot.event
async def on_message(message):
    if message.content.startswith('!news1'):
        await fortnite_client.fetch_br_news()
        channel = message.channel
        news = await fortnite_client.fetch_br_news()
        #await message.channel.send(news[0].body)
        embed = discord.Embed(title=news[0].title, description=news[0].body, color=0x00ff00)
        embed.set_image(url=news[0].image)
        await message.channel.send(embed=embed)

    if message.content.startswith('!news2'):
        await fortnite_client.fetch_br_news()
        channel = message.channel
        news = await fortnite_client.fetch_br_news()
        #await message.channel.send(news[0].body)
        embed1 = discord.Embed(title=news[1].title, description=news[1].body, color=0x00ff00)
        embed1.set_image(url=news[1].image)
        await message.channel.send(embed=embed1)

    if message.content.startswith('!news3'):
        await fortnite_client.fetch_br_news()
        channel = message.channel
        news = await fortnite_client.fetch_br_news()
        #await message.channel.send(news[0].body)
        embed2 = discord.Embed(title=news[2].title, description=news[2].body, color=0x00ff00)
        embed2.set_image(url=news[2].image)
        await message.channel.send(embed=embed2)

discord_bot.run('PUT TOKEN HERE')
