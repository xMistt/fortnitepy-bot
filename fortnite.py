import fortnitepy
import json
import aiohttp
import asyncio

with open('config.json', 'r') as f:
    data = json.load(f)
    emailjson = data[0]['email']
    passwordjson = data[0]['password']
    netcljson = data[0]['netcl']

client = fortnitepy.Client(
    email=emailjson,
    password=passwordjson,
    net_cl=netcljson,
)

print('fortnitepy-bot made by xMistt. credit to Terbau for creating the library.'.format(client))

global displayName
displayName = "ghoul"

@client.event
async def event_ready():
    print('Client ready as {0.user.display_name}'.format(client))

@client.event
async def event_party_invite(invitation):
    await invitation.accept()
    # if you want the bot to join with stuff on, put in here.
    # await invite(user_id) (Invite other bots/people to your lobby when the main bot joins.)

@client.event
async def event_friend_request(request):
    # await request.accept() // If you want the bot to acccept all friend requests.
    await request.decline()

@client.event
async def event_friend_message(message):
    args = message.content.split()
    arguments = args[1:]
    displayName = arguments
    print('Received message from {0.author.display_name} | Content: "{0.content}"'.format(message))

    if "!purpleskull" in args[0]:
        variants = client.user.party.me.create_variants(
           clothing_color=1
        )

        await client.user.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Purple Skull Trooper!')

    if "!banner" in args[0]:
        await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=None)

    if "CID_" in args[0]:
        await client.user.party.me.set_outfit(
            asset=args[0]
        )

    if "!variants" in args[0]:
        args3 = int(args[3])
        variants = client.user.party.me.create_variants(**{args[2]: args3})

        await client.user.party.me.set_outfit(
            asset=args[1],
            variants=variants
        )

        await message.reply('Skin set to' + args[1])

    if "!renegaderaider" in args[0]:

        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
            variants=variants
        )

        await message.reply('Skin set to' + args[0] + '!')

    if "EID_" in args[0]:
        await client.user.party.me.set_emote(
            asset=args[0]
        )
        await message.reply('Emote set to' + args[0] + '!')
        
    if "!stop" in args[0]:
        await client.user.party.me.set_emote(
            asset="StopEmote"
        )
        await message.reply('Stopped emoting.')

    if "BID_" in args[0]:
        await client.user.party.me.set_backpack(
            asset=args[0]
        )

        await message.reply('Backbling set to' + message.content + '!')

    if "!echo" in args[0]:
        await event_party_message.reply(arguments)

    await message.reply('Backbling set to' + message.content + '!')

    if "!help" in args[0]:
        await message.reply('My commands are; !purpleskull, !renegaderaider, !variants, CID_, EID_, BID_, PICKAXE_ID_ !banner, !stop & !help')

    if "PICKAXE_ID_" in args[0]:
        await client.user.party.me.set_pickaxe(
                asset=args[0]
        )

    URL = "http://benbotfn.tk:8080/api/cosmetics/search/multiple"

    # // ignore this it doesn't work rn
    if args[0] == "!skin":
        await benbot()

# // ignore this it doesn't work rn
URL = "http://benbotfn.tk:8080/api/cosmetics/search/multiple"
async def benbot():
    idint = 0
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(URL, params={"displayName": displayName}) as r:
                json_data = await r.json()
                list_type = json_data[idint]["type"]
                print(idint)

            if list_type == "Outift":
                list_id = json_data[idint]["id"]
                await client.user.party.me.set_outfit(asset=list_id)
                print(list_id)
                break
            else:
                print(f"{list_type} did not == Outfit")
                idint += 1

@client.event
async def event_party_message(message):
    # only type these if you're alone in your lobby + you're on console.
    args = message.content.split()
    print('Received message from {0.author.display_name} | Content: "{0.content}"'.format(message))

    if "!purpleskull" in args[0]:
        variants = client.user.party.me.create_variants(
           clothing_color=1
        )

        await client.user.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Purple Skull Trooper!')

    if "!banner" in args[0]:
        await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=None)

    if "CID_" in args[0]:
        await client.user.party.me.set_outfit(
            asset=args[0]
        )

    if "!variants" in args[0]:
        args3 = int(args[3])
        variants = client.user.party.me.create_variants(**{args[2]: args3})

        await client.user.party.me.set_outfit(
            asset=args[1],
            variants=variants
        )

        await message.reply('Skin set to' + args[1])

    if "!renegaderaider" in args[0]:

        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
            variants=variants
        )

        await message.reply('Skin set to' + args[0] + '!')

    if "EID_" in args[0]:
        await client.user.party.me.set_emote(
            asset=args[0]
        )
        await message.reply('Emote set to' + args[0] + '!')
        
    if "!stop" in args[0]:
        await client.user.party.me.set_emote(
            asset="StopEmote"
        )
        await message.reply('Stopped emoting.')

    if "BID_" in args[0]:
        await client.user.party.me.set_backpack(
            asset=args[0]
        )

        await message.reply('Backbling set to' + message.content + '!')

    if "!help" in args[0]:
        await message.reply('My commands are; !purpleskull, !renegaderaider, !variants, CID_, EID_, BID_, PICKAXE_ID_ !banner, !stop & !help')

    if "PICKAXE_ID_" in args[0]:
        await client.user.party.me.set_pickaxe(
                asset=args[0]
        )

        await message.reply('Pickaxe set to' + args[0] + '!')

client.run()