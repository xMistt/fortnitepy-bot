"""
MIT License

Copyright (c) 2019 Oli

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import fortnitepy
from fortnitepy.errors import *
import time as delay
import datetime
import json
import aiohttp
import time
import logging
import sys

time = datetime.datetime.now().strftime('%H:%M:%S')
print(f'[FORTNITEPY] [{time}] fortnitepy-bot made by xMistt. credit to Terbau for creating the library.')

def debugOn():
    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

with open('config.json') as f:
    data = json.load(f)[0]

if data['debug'] == 'True':
    time = datetime.datetime.now().strftime('%H:%M:%S')
    print(f'[FORTNITEPY] [{time}] Debug logging is on, prepare for a shitstorm.')
    debugOn()
else:
    time = datetime.datetime.now().strftime('%H:%M:%S')
    print(f'[FORTNITEPY] [{time}] Debug logging is off.')

client = fortnitepy.Client(
    email=data['email'],
    password=data['password'],
    net_cl=data['netcl'],
    status=data['status'],
    platform=fortnitepy.Platform.XBOX
)

BEN_BOT_BASE = 'http://benbotfn.tk:8080/api/cosmetics/search/multiple'

@client.event
async def event_ready():
    time = datetime.datetime.now().strftime('%H:%M:%S')
    print('[FORTNITEPY] [' + time + '] Client ready as {0.user.display_name}.'.format(client))

@client.event
async def event_party_invite(invitation):
    try:
        await invitation.accept()
        time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f'[FORTNITEPY] [{time}] Accepted party invite.')
    except fortnitepy.errors.PartyError:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[FORTNITEPY] [{time}] Couldn't accept invitation, incompatible net_cl.")

@client.event
async def event_friend_request(request):
    if data['friendaccept'] == "true":
        await request.accept()
    else:
        await request.decline()

@client.event
async def event_party_member_join(member):
    await client.user.party.me.set_outfit(asset=data['cid'])
    await client.user.party.me.set_backpack(asset=data['bid'])
    await client.user.party.me.set_banner(icon=data['banner'], color=data['banner_colour'], season_level=data['level'])
    delay.sleep(2)
    await client.user.party.me.set_emote(asset=data['eid'])
    await client.user.party.me.set_battlepass_info(has_purchased=True, level=data['bp_tier'], self_boost_xp=data['self_xp_boost'], friend_boost_xp=data['friend_xp_boost'])

async def fetch_cosmetic_cid(display_name):
    idint = 0
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(BEN_BOT_BASE, params={'displayName': display_name}) as r:
                data = await r.json()
                type = data[idint]["type"]
                if type == "Outfit":
                            id = data[idint]["id"]
                            return id
                else:
                    idint += 1

async def fetch_cosmetic_eid(display_name):
    idint = 0
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(BEN_BOT_BASE, params={'displayName': display_name}) as r:
                data = await r.json()
                type = data[idint]["type"]
                if type == "Emote":
                            id = data[idint]["id"]
                            return id
                else:
                    idint += 1

async def fetch_cosmetic_pid(display_name):
    idint = 0
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(BEN_BOT_BASE, params={'displayName': display_name}) as r:
                data = await r.json()
                type = data[idint]["type"]
                if type == "Harvesting Tool":
                            id = data[idint]["id"]
                            return id
                else:
                    idint += 1
                    
async def fetch_cosmetic_bid(display_name):
    idint = 0
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(BEN_BOT_BASE, params={'displayName': display_name}) as r:
                data = await r.json()
                type = data[idint]["type"]
                if type == "Back Bling":
                            id = data[idint]["id"]
                            return id
                else:
                    idint += 1


@client.event
async def event_friend_message(message):
    time = datetime.datetime.now().strftime('%H:%M:%S')
    args = message.content.split()
    split = args[1:]
    joinedArguments = " ".join(split)
    print('[FORTNITEPY] [' + time + '] {0.author.display_name}: "{0.content}"'.format(message))

    if "!skin" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        id = await fetch_cosmetic_cid(' '.join(split))
        await client.user.party.me.set_outfit(
            asset=id
        )
        await message.reply('Skin set to ' + id)
        print(f"[FORTNITEPY] [{time}] Client's CID set to: " + id)
        
    if "!backpack" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        id = await fetch_cosmetic_bid(' '.join(split))
        await client.user.party.me.set_backpack(
            asset=id
        )
        await message.reply('Backpack set to ' + id)

    if "!emote" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        id = await fetch_cosmetic_eid(' '.join(split))
        await client.user.party.me.set_emote(
            asset=id
        )

        await message.reply('Emote set to ' + id)

    if "!cidFinder" in args[0]:
        i = 1
        cidnumber = 10
        while i == 1:
            print(cidnumber)
            await client.user.party.me.set_outfit(asset='CID_3' + str(cidnumber) + '_Athena_Commando_M_DummyS11BotAMammt')
            cidnumber += 1

    if "!rawbackpack" in args[0]:
        rawBackpack = await client.user.party.me.backpack_variants('6c2ce028998a4b35a5ebf0ba655d1236')
        print(rawBackpack)

    if "!pickaxe" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        id = await fetch_cosmetic_pid(' '.join(split))
        await client.user.party.me.set_pickaxe(
            asset=id
        )

        await message.reply('Pickaxe set to ' + id)

    if "!purpleskull" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        variants = client.user.party.me.create_variants(
           clothing_color=1
        )

        await client.user.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Purple Skull Trooper!')

    if "!purpleportal" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        variants = client.user.party.me.create_variants(
            item='AthenaBackpack',
            particle_config='Particle',
            particle=1
        )

        await client.user.party.me.set_backpack(
            asset='BID_105_GhostPortal',
            variants=variants
        )

        await message.reply('Skin set to Purple Skull Trooper!')

    if "!banner" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=args[3])

    if "CID_" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await client.user.party.me.set_outfit(
            asset=args[0]
        )

        await message.reply('Skin set to ' + args[0])

    if "!variants" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        args3 = int(args[3])
        variants = client.user.party.me.create_variants(**{args[2]: args3})

        await client.user.party.me.set_backpack(
            asset=args[1],
            variants=variants
        )

        await message.reply('Skin set to checkered Renegade Raider!')

    if "!checkeredrenegade" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')

        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
            variants=variants
        )

        await message.reply('Skin set to ' + args[0] + '!')

    if "EID_" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await client.user.party.me.set_emote(asset="StopEmote")
        await client.user.party.me.set_emote(
            asset=args[0]
        )
        await message.reply('Emote set to ' + args[0] + '!')
        
    if "!stop" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await client.user.party.me.set_emote(
            asset="StopEmote"
        )
        await message.reply('Stopped emoting.')

    if "BID_" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await client.user.party.me.set_backpack(
            asset=args[0]
        )

        await message.reply('Backbling set to ' + message.content + '!')

    if "!help" in args[0]:
        await message.reply('For a list of commands, goto; https://github.com/xMistt/fortnitepy-bot')

    if "PICKAXE_ID_" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await client.user.party.me.set_pickaxe(
                asset=args[0]
        )

        await message.reply('Pickaxe set to ' + args[0] + '!')

    if "!pettest" in args[0]:
        await client.user.party.me.set_backpack(
                asset='PetCarrier_001_Dog'
        )

    if "!legacypickaxe" in args[0]:
        await client.user.party.me.set_pickaxe(
                asset=args[1]
        )

        await message.reply('Pickaxe set to ' + args[1] + '!')

    if "!ready" in args[0]:
        await client.user.party.me.set_ready(True)
        await message.reply('Ready!')

    if "!unready" in args[0]:
        await client.user.party.me.set_ready(False)
        await message.reply('Unready!')

    if "!bp" in args[0]:
        await client.user.party.me.set_battlepass_info(has_purchased=True, level=args[1], self_boost_xp=args[2], friend_boost_xp=args[3])

    if "!point" in args[0]:
        await client.user.party.me.set_pickaxe(asset=args[1])
        await client.user.party.me.set_emote(asset='EID_IceKing')

        await message.reply('Pickaxe set to ' + args[1] + ' & Point It Out played.')

    if "!searchpoint" in args[0]:
        id = await fetch_cosmetic_pid(' '.join(split))
        await client.user.party.me.set_pickaxe(asset=id)
        await client.user.party.me.set_emote(asset='EID_IceKing')

        await message.reply('Pickaxe set to ' + args[1] + ' & Point It Out played.')

    if "!update" in args[0]:
        with open('config.json', 'r') as f:
            data = json.load(f)
            emailjson = data[0]['email']
            passwordjson = data[0]['password']
            netcljson = data[0]['netcl']
            cid = data[0]['cid']
            bid = data[0]['bid']
            eid = data[0]['eid']
            banner = data[0]['banner']
            banner_colour = data[0]['banner_colour']
            level = data[0]['level']
            bp_tier = data[0]['bp_tier']
            self_xp_boost = data[0]['self_xp_boost']
            friend_xp_boost = data[0]['friend_xp_boost']
            friendaccept = data[0]['friendaccept']
        await message.reply('Updated config.json!')

    if "!echo" in args[0]:
        await client.user.party.send(joinedArguments)

@client.event
async def event_party_message(message):
    ### NO LONGER REQUIRED! ###
    print('Received message from {0.author.display_name} | Content: "{0.content}"'.format(message))

client.run()
