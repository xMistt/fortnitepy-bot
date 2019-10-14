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

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

try:
    import fortnitepy
    from fortnitepy.errors import *
    import asyncio
    import time as delay
    import datetime
    import json
    import aiohttp
    import time
    import logging
    import sys
    from colorama import init
    init(autoreset=True)
    from colorama import Fore, Back, Style

except ModuleNotFoundError:
    print(color.RED + f'[FORTNITEPY] [N/A] [ERROR] Failed to import 1 or more modules, run "INSTALL PACKAGES.bat".' + color.END)
    exit()

print(color.BOLD + f'[FORTNITEPY] [{time}] fortnitepy-bot made by xMistt. credit to Terbau for creating the library.')

def debugOn():
    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

with open('config.json') as f:
    time = datetime.datetime.now().strftime('%H:%M:%S')
    print(f'[FORTNITEPY] [{time}] Loading config.')
    data = json.load(f)[0]
    print(f'[FORTNITEPY] [{time}] Config loaded.')
    
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
    platform=fortnitepy.Platform(data['platform'])
)

BEN_BOT_BASE = 'http://benbotfn.tk:8080/api/cosmetics/search/multiple'

async def fetch_cosmetic_id(display_name, cosmeticType):
    try:
        idint = 0
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(BEN_BOT_BASE, params={'displayName': display_name}) as r:
                    data = await r.json()
                    backendType = data[idint]["backendType"]
                    if backendType == cosmeticType:
                                id = data[idint]["id"]
                                return id
                    else:
                        idint += 1
    except IndexError:
        print('Failed to find' + display_name)

@client.event
async def event_ready():
    time = datetime.datetime.now().strftime('%H:%M:%S')
    print(Fore.GREEN + '[FORTNITEPY] [' + time + '] Client ready as {0.user.display_name}.'.format(client))

@client.event
async def event_party_invite(invite):
    try:
        await invite.accept()
        time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f'[FORTNITEPY] [{time}] Accepted party invite.')
    except fortnitepy.PartyError:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        print(Fore.RED + f"[FORTNITEPY] [{time}] Couldn't accept invitation, incompatible net_cl." + Fore.WHITE)

@client.event
async def event_friend_request(request):
    time = datetime.datetime.now().strftime('%H:%M:%S')
    print(f"[FORTNITEPY] [{time}] Recieved friend request from: {request.display_name}.")

    if (data['friendaccept'] == "true") or (data['friendaccept'] == "True"):
        await request.accept()
        print(f"[FORTNITEPY] [{time}] Accepted friend request from: {request.display_name}.")
    else:
        await request.decline()
        print(f"[FORTNITEPY] [{time}] Declined friend request from: {request.display_name}.")

@client.event
async def event_party_member_join(member):
    time = datetime.datetime.now().strftime('%H:%M:%S')

    await client.user.party.me.set_outfit(asset=data['cid'])
    await client.user.party.me.set_backpack(asset=data['bid'])
    await client.user.party.me.set_banner(icon=data['banner'], color=data['banner_colour'], season_level=data['level'])
    delay.sleep(2)
    await client.user.party.me.set_emote(asset=data['eid'])
    await client.user.party.me.set_battlepass_info(has_purchased=True, level=data['bp_tier'], self_boost_xp=data['self_xp_boost'], friend_boost_xp=data['friend_xp_boost'])
    
    if client.user.display_name != member.display_name:
        print(f"[FORTNITEPY] [{time}] {member.display_name} has joined the lobby.")

@client.event
async def event_friend_message(message):
    time = datetime.datetime.now().strftime('%H:%M:%S')
    args = message.content.split()
    split = args[1:]
    joinedArguments = " ".join(split)
    print('[FORTNITEPY] [' + time + '] {0.author.display_name}: {0.content}'.format(message))

    if "!skin" in args[0].lower():
        time = datetime.datetime.now().strftime('%H:%M:%S')
        id = await fetch_cosmetic_id(' '.join(split), 'AthenaCharacter')
        await client.user.party.me.set_outfit(
            asset=id,
            variants=None
        )
        await message.reply('Skin set to ' + id)
        print(f"[FORTNITEPY] [{time}] Client's CID set to: " + id)
        
    if "!backpack" in args[0].lower():
        time = datetime.datetime.now().strftime('%H:%M:%S')
        id = await fetch_cosmetic_id(' '.join(split), 'AthenaBackpack')
        await client.user.party.me.set_backpack(
            asset=id
        )
        await message.reply('Backpack set to ' + id)
        print(f"[FORTNITEPY] [{time}] Client's BID set to: " + id)

    if "!emote" in args[0].lower():
        time = datetime.datetime.now().strftime('%H:%M:%S')
        id = await fetch_cosmetic_id(' '.join(split), 'AthenaDance')
        await client.user.party.me.set_emote(asset='EID_ClearEmote')
        await client.user.party.me.set_emote(
            asset=id
        )

        await message.reply('Emote set to ' + id)
        print(f"[FORTNITEPY] [{time}] Client's EID set to: " + id)

    if "!pickaxe" in args[0].lower():
        time = datetime.datetime.now().strftime('%H:%M:%S')
        id = await fetch_cosmetic_id(' '.join(split), 'AthenaPickaxe')
        await client.user.party.me.set_pickaxe(
            asset=id
        )

        await message.reply('Pickaxe set to ' + id)
        print(f"[FORTNITEPY] [{time}] Client's PICKAXE_ID set to: " + id)

    if "!pet" in args[0].lower():
        time = datetime.datetime.now().strftime('%H:%M:%S')
        id = await fetch_cosmetic_id(' '.join(split), 'AthenaPetCarrier')
        await client.user.party.me.set_backpack(
                asset="/Game/Athena/Items/Cosmetics/PetCarriers/" + id + "." + id
        )

        await message.reply('Pet set to ' + id)
        print(f"[FORTNITEPY] [{time}] Client's PetCarrier set to: " + id)

    if "!emoji" in args[0].lower():
        time = datetime.datetime.now().strftime('%H:%M:%S')
        id = await fetch_cosmetic_id(' '.join(split), 'AthenaDance')
        await client.user.party.me.set_emote(asset='EID_ClearEmote')
        await client.user.party.me.set_emote(
                asset="/Game/Athena/Items/Cosmetics/Dances/Emoji/" + id + "." + id
        )

        await message.reply('Emoji set to ' + id)
        print(f"[FORTNITEPY] [{time}] Client's Emoji set to " + id)

    if "!purpleskull" in args[0].lower():
        time = datetime.datetime.now().strftime('%H:%M:%S')
        variants = client.user.party.me.create_variants(
           clothing_color=1
        )

        await client.user.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Purple Skull Trooper!')

    if "!purpleportal" in args[0].lower():
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

        await message.reply('Backpack set to Purple Ghost Portal!')

    if "!banner" in args[0].lower():
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=args[3])

        await message.reply(f'Banner set to; {args[1]} {args[2]} {args[3]}')
        print(f"[FORTNITEPY] [{time}] Banner set to; " + args[1] + args[2] + args[3])

    if "CID_" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await client.user.party.me.set_outfit(
            asset=args[0]
        )

        await message.reply(f'Skin set to {args[0]}')
        await print(f'[FORTNITEPY] [{time}] Skin set to ' + args[0])

    if "!variants" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        args3 = int(args[3])

        if 'CID' in args[1]:
            variants = client.user.party.me.create_variants(**{args[2]: args3})
            await client.user.party.me.set_outfit(
                asset=args[1],
                variants=variants
            )
        elif 'BID' in args[1]:
            variants = client.user.party.me.create_variants(item='AthenaBackpack', **{args[2]: args3})
            await client.user.party.me.set_backpack(
                asset=args[1],
                variants=variants
            )
        elif 'PICKAXE_ID' in args[1]:
            variants = client.user.party.me.create_variants(item='AthenaPickaxe', **{args[2]: args3})
            await client.user.party.me.set_pickaxe(
                asset=args[1],
                variants=variants
            )

        await message.reply(f'Set variants of {args[1]} to {args[2]} {args[3]}.')
        print(f'[FORTNITEPY] [{time}] Set variants of {args[1]} to {args[2]} {args[3]}.')

    if "!checkeredrenegade" in args[0].lower():
        time = datetime.datetime.now().strftime('%H:%M:%S')

        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
            variants=variants
        )

        await message.reply('Skin set to Checkered Renegade!')

    if "EID_" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await client.user.party.me.set_emote(asset="StopEmote")
        await client.user.party.me.set_emote(
            asset=args[0]
        )
        await message.reply('Emote set to ' + args[0] + '!')
        
    if "!stop" in args[0].lower():
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await client.user.party.me.clear_emote()
        await message.reply('Stopped emoting.')

    if "BID_" in args[0]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await client.user.party.me.set_backpack(
            asset=args[0]
        )

        await message.reply('Backbling set to ' + message.content + '!')

    if "!help" in args[0].lower():
        await message.reply('For a list of commands, goto; https://github.com/xMistt/fortnitepy-bot')

    if "PICKAXE_ID_" in args[0].lower():
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await client.user.party.me.set_pickaxe(
                asset=args[0]
        )

        await message.reply('Pickaxe set to ' + args[0] + '!')

    if "PetCarrier_" in args[0]:
        await client.user.party.me.set_backpack(
                asset="/Game/Athena/Items/Cosmetics/PetCarriers/" + args[0] + "." + args[0]
        )

    if "Emoji_" in args[0]:
        await client.user.party.me.set_emote(asset='EID_ClearEmote')
        await client.user.party.me.set_emote(
                asset="/Game/Athena/Items/Cosmetics/Dances/Emoji/" + args[0] + "." + args[0]
        )

    if "!legacypickaxe" in args[0].lower():
        await client.user.party.me.set_pickaxe(
                asset=args[1]
        )

        await message.reply('Pickaxe set to ' + args[1] + '!')

    if "!ready" in args[0].lower():
        await client.user.party.me.set_ready(True)
        await message.reply('Ready!')

    if ("!unready" in args[0].lower()) or ("!sitin" in args[0].lower()):
        await client.user.party.me.set_ready(False)
        await message.reply('Unready!')

    if "!sitout" in args[0].lower():
        await client.user.party.me.set_ready('SittingOut')
        await message.reply('Sitting Out!')

    if "!bp" in args[0].lower():
        await client.user.party.me.set_battlepass_info(has_purchased=True, level=args[1], self_boost_xp=args[2], friend_boost_xp=args[3])

    if "!echo" in args[0].lower():
        await client.user.party.send(joinedArguments)

    if "!status" in args[0].lower():
        await client.set_status(joinedArguments)

        await message.reply(f'Status set to {joinedArguments}')
        print(f'[FORTNITEPY] [{time}] Status set to {joinedArguments}.')

    if "!leave" in args[0].lower():
        await client.user.party.me.set_emote('EID_Wave')
        delay.sleep(2)
        await client.user.party.me.leave()
        await message.reply('Bye!')
        print(f'[FORTNITEPY] [{time}] Left the party as I was requested.')

    if "!kick" in args[0].lower():
        user = await client.fetch_profile(joinedArguments)
        member = client.user.party.members.get(user.id)
        if member is None:
            await message.reply("Couldn't find that user, are you sure they're in the party?")
        else:
            try:
                await member.kick()
                await message.reply(f"Kicked user: {member.display_name}.")
                print(f"[FORTNITEPY] [{time}] Kicked user: {member.display_name}")
            except fortnitepy.PartyPermissionError:
                await message.reply(f"Couldn't kick {member.display_name}, as I'm not party leader.")
                print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Failed to kick member as I don't have the required permissions." + Fore.WHITE)

    if "!promote" in args[0].lower():
        user = await client.fetch_profile(joinedArguments)
        member = client.user.party.members.get(user.id)
        if member is None:
            await message.reply("Couldn't find that user, are you sure they're in the party?")
        else:
            try:
                await member.promote()
                await message.reply(f"Promoted user: {member.display_name}.")
                print(f"[FORTNITEPY] [{time}] Promoted user: {member.display_name}")
            except fortnitepy.PartyPermissionError:
                await message.reply(f"Couldn't promote {member.display_name}, as I'm not party leader.")
                print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Failed to promote member as I don't have the required permissions." + Fore.WHITE)

    if "Playlist_" in args[0]:
        try:
            await client.user.party.set_playlist(playlist=args[0])
        except fortnitepy.PartyPermissionError:
                await message.reply(f"Couldn't set gamemode to {args[1]}, as I'm not party leader.")
                print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Failed to set gamemode as I don't have the required permissions." + Fore.WHITE)

@client.event
async def event_party_message(message):
    ### NO LONGER REQUIRED! ###
    print('Received message from {0.author.display_name} | Content: "{0.content}"'.format(message))

try:
    client.run()
except fortnitepy.AuthException:
    print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Couldn't log into the account, is config.json filled out?")
