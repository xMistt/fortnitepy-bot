import fortnitepy
from discord.ext import commands

discord_bot = commands.Bot(
    command_prefix='!',
    description='My discord + fortnite bot!',
    case_insensitive=True
)

fortnite_client = fortnitepy.Client(
    email='email',
    password='password',
    loop=discord_bot.loop
)

@discord_bot.event
async def on_ready():
    print('Discord bot ready')
    await fortnite_client.start()

@fortnite_client.event
async def event_ready():
    print('Fortnite client ready')

@discord_bot.event
async def on_message(message):
    print('Received message from {0.author.display_name} | Content "{0.content}"'.format(message))

@fortnite_client.event
async def event_friend_message(message):
    print('Received message from {0.author.display_name} | Content "{0.content}"'.format(message))

# discord command
@commands.command()
async def mycommand(ctx):
    await ctx.send('Hello there!')

discord_bot.run('DISCORD TOKEN')
