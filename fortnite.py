"""
“Commons Clause” License Condition v1.0
Copyright Oli 2019

The Software is provided to you by the Licensor under the
License, as defined below, subject to the following condition.

Without limiting other conditions in the License, the grant
of rights under the License will not include, and the License
does not grant to you, the right to Sell the Software.

For purposes of the foregoing, “Sell” means practicing any or
all of the rights granted to you under the License to provide
to third parties, for a fee or other consideration (including
without limitation fees for hosting or consulting/ support
services related to the Software), a product or service whose
value derives, entirely or substantially, from the functionality
of the Software. Any license notice or attribution required by
the License must also include this Commons Clause License
Condition notice.

Software: fortnitepy-bot

License: Apache 2.0
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
    import BenBotAsync
    import asyncio
    import time as delay
    import datetime
    import json
    import aiohttp
    import time
    import logging
    import sys
    import random
    from colorama import init
    init(autoreset=True)
    from colorama import Fore, Back, Style
except ModuleNotFoundError:
    print(Fore.RED + f'[FORTNITEPY] [N/A] [ERROR] Failed to import 1 or more modules, run "INSTALL PACKAGES.bat".')
    exit()

time = datetime.datetime.now().strftime('%H:%M:%S')
print(f'  ')
print(color.CYAN + f'   ██████╗ ██╗   ██╗     ██████╗  ██████╗ ████████╗')
print(color.CYAN + f'   ██╔══██╗╚██╗ ██╔╝     ██╔══██╗██╔═══██╗╚══██╔══╝')
print(color.CYAN + f'   ██████╔╝ ╚████╔╝█████╗██████╔╝██║   ██║   ██║   ')
print(color.CYAN + f'   ██╔═══╝   ╚██╔╝ ╚════╝██╔══██╗██║   ██║   ██║   ')
print(color.CYAN + f'   ██║        ██║        ██████╔╝╚██████╔╝   ██║   ')
print(color.CYAN + f'   ╚═╝        ╚═╝        ╚═════╝  ╚═════╝    ╚═╝   ')
print(f'  ')

def debugOn():
    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

def getTime():
    time = datetime.datetime.now().strftime('%H:%M:%S')
    return time

with open('config.json') as f:
    print(f' [PYBOT] [{getTime()}] Loading config.')
    data = json.load(f)
    print(f' [PYBOT] [{getTime()}] Config loaded.')
    
if data['debug'] == 'True':
    print(f' [PYBOT] [{getTime()}] Debug logging is on.')
    debugOn()
else:
    print(f' [PYBOT] [{getTime()}] Debug logging is off.')

client = fortnitepy.Client(
    email=data['email'],
    password=data['password'],
    status=data['status'],
    platform=fortnitepy.Platform(data['platform'])
)

@client.event
async def event_ready():
    print(Fore.GREEN + ' [PYBOT] [' + getTime() + '] Client ready as {0.user.display_name}.'.format(client))

@client.event
async def event_party_invite(invite):
    if data['joinoninvite'].lower() == 'true':
        try:
            await invite.accept()
            print(Fore.GREEN + f' [PYBOT] [{getTime()}] Accepted party invite from {invite.sender.display_name}.')
        except Exception as e:
            pass
    if data['joinoninvite'].lower() == 'false':
        if invite.sender.display_name in data['FullAccess']:
            await invite.accept()
            print(Fore.GREEN + f' [PYBOT] [{getTime()}] Accepted party invite from {invite.sender.display_name}.')
        else:
            print(Fore.GREEN + f' [PYBOT] [{getTime()}] Never accepted party invite from {invite.sender.display_name}.')
            await invite.sender.send(f"I can't join you right now.")

@client.event
async def event_friend_request(request):
    if data['friendaccept'].lower() == 'true':
        try:
            await request.accept()
            print(f" [PYBOT] [{getTime()}] Accepted friend request from: {request.display_name}.")
        except Exception as e:
            pass
    if data['friendaccept'].lower() == 'false':
        print(f" [PYBOT] [{getTime()}] Never accepted friend request from: {request.display_name}.")

@client.event
async def event_party_member_join(member):
    variants = client.user.party.me.create_variants(**{data['variants-type']: data['variants']})
    await client.user.party.me.set_outfit(asset=data['cid'], variants=variants)
    await client.user.party.me.set_backpack(asset=data['bid'])
    await client.user.party.me.set_pickaxe(asset=data['pid'])
    await client.user.party.me.set_banner(icon=data['banner'], color=data['banner_colour'], season_level=data['level'])
    delay.sleep(2)
    await client.user.party.me.set_emote(asset=data['eid'])
    await client.user.party.me.set_battlepass_info(has_purchased=True, level=data['bp_tier'], self_boost_xp='0', friend_boost_xp='0')
    
    if client.user.display_name != member.display_name:
        print(f" [PYBOT] [{getTime()}] {member.display_name} has joined the lobby.")

@client.event
async def event_friend_message(message):
    args = message.content.split()
    split = args[1:]
    joinedArguments = " ".join(split)
    print(' [PYBOT] [' + getTime() + '] {0.author.display_name}: {0.content}'.format(message))

    if "!skin" in args[0].lower():
        id = await BenBotAsync.getSkinId(joinedArguments)
        if id == None:
            await message.reply(f"Couldn't find a skin with the name: {joinedArguments}")
        else:
            await client.user.party.me.set_outfit(asset=id)
            await message.reply('Skin set to ' + id)
            print(f" [PYBOT] [{getTime()}] Set Skin to: " + id)
        
    if "!backpack" in args[0].lower():
        if len(args) == 1:
            await client.user.party.me.set_backpack(asset='none')
            await message.reply('Backpack set to None')
            print(f" [PYBOT] [{getTime()}] Set Backpack to None")
        else:
            id = await BenBotAsync.getBackpackId(joinedArguments)
            if id == None:
                await message.reply(f"Couldn't find a backpack with the name: {joinedArguments}")
            else:
                await client.user.party.me.set_backpack(asset=id)
                await message.reply('Backpack set to ' + id)
                print(f" [PYBOT] [{getTime()}] Set Backpack to: " + id)

    if "!emote" in args[0].lower():
        await client.user.party.me.clear_emote()
        id = await BenBotAsync.getEmoteId(joinedArguments)
        if id == None:
            await message.reply(f"Couldn't find an emote with the name: {joinedArguments}")
        else:
            await client.user.party.me.set_emote(asset=id)
            await message.reply('Emote set to ' + id)
            print(f" [PYBOT] [{getTime()}] Set Emote to: " + id)
    
    if "!pickaxe" in args[0].lower():
        id = await BenBotAsync.getPickaxeId(joinedArguments)
        if id == None:
            await message.reply(f"Couldn't find a pickaxe with the name: {joinedArguments}")
        else:
            await client.user.party.me.set_pickaxe(asset=id)
            await message.reply('Pickaxe set to ' + id)
            print(f" [PYBOT] [{getTime()}] Set Pickaxe to: " + id)

    if "!point" in args[0].lower():
        await client.user.party.me.clear_emote()
        id = await BenBotAsync.getPickaxeId(joinedArguments)
        if id == None:
            await message.reply(f"Couldn't find a pickaxe with the name: {joinedArguments}")
        else:
            await client.user.party.me.set_pickaxe(asset=id)
            await client.user.party.me.set_emote(asset="/Game/Athena/Items/Cosmetics/Dances/EID_IceKing.EID_IceKing")
            await message.reply('Pointing with ' + id)
            print(f" [PYBOT] [{getTime()}] Pointing a pickaxe with: " + id)

    if "!pet" in args[0].lower():
        id = await BenBotAsync.getPetId(joinedArguments)
        await client.user.party.me.set_backpack(
                asset="/Game/Athena/Items/Cosmetics/PetCarriers/" + id + "." + id
        )

        await message.reply('Pet set to ' + id)
        print(f" [PYBOT] [{getTime()}] Client's PetCarrier set to: " + id)

    if "!emoji" in args[0].lower():
        id = await fetch_cosmetic_id(' '.join(split), 'AthenaDance')
        await client.user.party.me.clear_emote()
        await client.user.party.me.set_emote(
                asset="/Game/Athena/Items/Cosmetics/Dances/Emoji/" + id + "." + id
        )

        await message.reply('Emoji set to ' + id)
        print(f" [PYBOT] [{getTime()}] Client's Emoji set to " + id)

    if "!purpleskull" in args[0].lower():
        variants = client.user.party.me.create_variants(
           clothing_color=1
        )

        await client.user.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Purple Skull Trooper!')
        print(f" [PYBOT] [{getTime()}] Client's Skin set to Purple Skull Trooper")

    if "!pinkghoul" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=3
        )

        await client.user.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Pink Ghoul Trooper!')
        print(f" [PYBOT] [{getTime()}] Client's Skin set to Pink Ghoul Trooper")

    if "!brainiacghoul" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Brainiac Ghoul Trooper!')
        print(f" [PYBOT] [{getTime()}] Client's Skin set to Brainiac Ghoul Trooper")

    if "!normalghoul" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=0
        )

        await client.user.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Brainiac Ghoul Trooper!')
        print(f" [PYBOT] [{getTime()}] Client's Skin set to Normal Ghoul Trooper")

    if "!purpleportal" in args[0].lower():
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
        print(f" [PYBOT] [{getTime()}] Client's Backpack set to Purple Ghost Portal")

    if "!banner" in args[0].lower():
        if len(args) == 1:
            await message.reply('You need to specify which banner, color & level you want to set the banner as.')
        if len(args) == 2:
            await client.user.party.me.set_banner(icon=args[1], color=data['banner_colour'], season_level=data['level'])
        if len(args) == 3:
            await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=data['level'])
        if len(args) == 4:
            await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=args[3])

        await message.reply(f'Banner set to; {args[1]} {args[2]} {args[3]}')
        print(f" [PYBOT] [{getTime()}] Banner set to; {args[1]} {args[2]} {args[3]}")

    if "CID_" in args[0]:
        await client.user.party.me.set_outfit(
            asset=args[0]
        )
        await message.reply(f'Skin set to {args[0]}')
        print(f' [PYBOT] [{getTime()}] Skin set to ' + args[0])

    if "!variants" in args[0]:
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
        print(f' [PYBOT] [{getTime()}] Set variants of {args[1]} to {args[2]} {args[3]}.')

    if "!checkeredrenegade" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
            variants=variants
        )

        await message.reply('Skin set to Checkered Renegade!')
        print(f" [PYBOT] [{getTime()}] Client's Skin set to Checkered Renegade")

    if "EID_" in args[0]:
        await client.user.party.me.clear_emote()
        await client.user.party.me.set_emote(
            asset=args[0]
        )
        await message.reply('Emote set to ' + args[0] + '!')
        
    if "!stop" in args[0].lower():
        await client.user.party.me.clear_emote()
        await message.reply('Stopped emoting.')

    if "BID_" in args[0]:
        await client.user.party.me.set_backpack(
            asset=args[0]
        )

        await message.reply('Backbling set to ' + message.content + '!')

    if "help" in args[0].lower():
        await message.reply('Commands: !cosmetics - Lists Cosmetic Commands  |  !party - Lists Party Commands | You can view a more detailed commands list in my discord server!')

    if "!cosmetics" in args[0].lower():
        await message.reply('Cosmetic Commands: !skin (skin name), !backpack (backpack name), !emote (emote name) | !stop-to stop the emote, !pickaxe (pickaxe name), !point (pickaxe name), !pet (pet name), !emoji (emoji name), !variants (CID) (style type) (integer), !purpleskull, !pinkghoul, !brainiacghoul, !purpleportal, !checkeredrenegade, !banner (icon) (colour) (level), CID_, BID_, PICKAXE_ID_, EID_')

    if "!party" in args[0].lower():
        await message.reply('Party Commands: !ready, !unready, !sitout, !sitin, !bp (tier), !level (level), !echo (message), !leave, !kick (username), Playlist_')

    if "Pickaxe_" in args[0]:
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

    if "!ready" in args[0].lower():
        await client.user.party.me.set_ready(True)
        await message.reply('Ready!')

    if ("!unready" in args[0].lower()) or ("!sitin" in args[0].lower()):
        await client.user.party.me.set_ready(False)
        await message.reply('Unready!')

    if "!sitout" in args[0].lower():
        await client.user.party.me.set_ready(None)
        await message.reply('Sitting Out!')

    if "!bp" in args[0].lower():
        await client.user.party.me.set_battlepass_info(has_purchased=True, level=args[1], self_boost_xp='0', friend_boost_xp='0')

    if "!level" in args[0].lower():
        await client.user.party.me.set_banner(icon=client.user.party.me.banner[0], color=client.user.party.me.banner[1], season_level=args[1])
    
    if "!reset" in args[0].lower():
        variants = client.user.party.me.create_variants(**{data['variants-type']: data['variants']})
        await client.user.party.me.set_outfit(asset=data['cid'], variants=variants)
        await client.user.party.me.set_backpack(asset=data['bid'])
        await client.user.party.me.set_banner(icon=data['banner'], color=data['banner_colour'], season_level=data['level'])
        await client.user.party.me.set_pickaxe(asset=data['pid'])
        await client.user.party.me.set_battlepass_info(has_purchased=True, level=data['bp_tier'], self_boost_xp='0', friend_boost_xp='0')
        await message.reply(f"Reset to default cosmetic loadout.")

    if "!echo" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            await client.user.party.send(joinedArguments)
            print(f' [PYBOT] [{getTime()}] ' + color.GREEN + 'Sent Message:' + color.END + f' {joinedArguments}')
        else:
            if message.author.display_name not in data['FullAccess']:
                await message.reply(f"You don't have access to this command!")

    if "!admin" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            if len(args) == 1:
                await message.reply('Please specify if you want to add or remove a user from the admin list')
                print(f' [PYBOT] [{getTime()}] Please specify if you want to add or remove a user from the admin list, using ' + color.GREEN + '!admin add ' + color.END + 'or ' + color.GREEN + '!admin remove' + color.END)
            if len(args) == 2:
                if args[1].lower() == 'add' or args[1].lower() == 'remove':
                    await message.reply('Please specify the name of the user you want to add/remove from the admin list')
                    print(f' [PYBOT] [{getTime()}] Please specify the name of the user you want to add/remove from the admin list')
                else:
                    await message.reply('Invalid usage, try !admin add <username> or !admin remove <username>')
                    print(f' [PYBOT] [{getTime()}] Invalid usage, try ' + color.GREEN + '!admin add <username> ' + color.END + 'or ' + color.GREEN + '!admin remove <username>' + color.END)
            if len(args) >= 3:
                joinedArgumentsAdmin = " ".join(args[2:])
                user = await client.fetch_profile(joinedArgumentsAdmin)
                try:
                    if args[1].lower() == 'add':
                        if user.display_name not in data['FullAccess']:
                            data['FullAccess'].append(f"{user.display_name}")
                            with open('config.json', 'w') as f:
                                json.dump(data, f, indent=4)
                                print(f" [PYBOT] [{getTime()}] Added " + color.GREEN + f"{user.display_name}" + color.END + " as an admin")
                        elif user.display_name in data['FullAccess']:
                            print(f" [PYBOT] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " is already an admin")
                    elif args[1].lower() == 'remove':
                        if user.display_name in data['FullAccess']:
                            data['FullAccess'].remove(user.display_name)
                            with open('config.json', 'w') as f:
                                json.dump(data, f, indent=4)
                                print(f" [PYBOT] [{getTime()}] Removed " + color.GREEN + f"{user.display_name}" + color.END + " as an admin")
                        elif user.display_name not in data['FullAccess']:
                            print(f" [PYBOT] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " is not an admin")
                except AttributeError:
                    pass
                    print(f" [PYBOT] [{getTime()}] Can't find user: " + color.GREEN + f"{joinedArgumentsAdmin}" + color.END)
                    await message.reply(f"I couldn't find an Epic account with the name: {joinedArgumentsAdmin}.")
        if message.author.display_name not in data['FullAccess']:
            if len(args) >= 3 and args[1].lower() == 'add':
                await message.reply(f"Password?")
                res = await client.wait_for('friend_message')
                content = res.content.lower()
                joinedArgumentsAdmin = " ".join(args[2:])
                user = await client.fetch_profile(joinedArgumentsAdmin)
                if content in data['AdminPassword']:
                    if user.display_name not in data['FullAccess']:
                        data['FullAccess'].append(f"{user.display_name}")
                        with open('config.json', 'w') as f:
                            json.dump(data, f, indent=4)
                            await message.reply(f"Correct. Added {user.display_name} as an admin.")
                            print(f" [PYBOT] [{getTime()}] Added " + color.GREEN + f"{user.display_name}" + color.END + " as an admin")
                    elif user.display_name in data['FullAccess']:
                        print(f" [PYBOT] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " is already an admin")
                        await message.reply(f"{user.display_name} is already an admin.")
            else:
                await message.reply(f"You don't have access to this command!")

    if "!status" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            await client.set_status(joinedArguments)
            await message.reply(f'Status set to {joinedArguments}')
            print(f' [PYBOT] [{getTime()}] Status set to {joinedArguments}.')
        else:
            if message.author.display_name not in data['FullAccess']:
                await message.reply(f"You don't have access to this command!")
            
    if "!leave" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            await client.user.party.me.set_emote('EID_Snap')
            delay.sleep(2)
            await client.user.party.me.leave()
            await message.reply('Bye!')
            print(Fore.GREEN + f' [PYBOT] [{getTime()}] Left the party as I was requested.')
        else:
            if message.author.display_name not in data['FullAccess']:
                await message.reply(f"You don't have access to this command!")

    if "!kick" in args[0].lower() and message.author.display_name in data['FullAccess']:
        user = await client.fetch_profile(joinedArguments)
        member = client.user.party.members.get(user.id)
        if member is None:
            await message.reply("Couldn't find that user, are you sure they're in the party?")
        else:
            try:
                await member.kick()
                await message.reply(f"Kicked user: {member.display_name}.")
                print(Fore.GREEN + f" [PYBOT] [{getTime()}] Kicked user: {member.display_name}")
            except Exception as e:
                pass
                await message.reply(f"Couldn't kick {member.display_name}, as I'm not party leader.")
                print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] Failed to kick member as I don't have the required permissions." + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            await message.reply(f"You don't have access to this command!")

    if "!join" in args[0] and message.author.display_name in data['FullAccess']:
        if len(args) != 1:
            user = await client.fetch_profile(joinedArguments)
            friend = client.get_friend(user.id)
        if len(args) == 1:
            user = await client.fetch_profile(message.author.id, cache=False, raw=False)
            friend = client.get_friend(user.id)
        if friend is None:
            await message.reply(f"Unable to invite that user, are you sure the bot has them added?")
            print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] Unable to join user: {joinedArguments}, are you sure the bot has them added?" + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            await message.reply(f"You don't have access to this command!")
        else:
            try:
                await friend.join_party()
                await message.reply(f"Joining {friend.display_name}'s party.")
            except Exception as e:
                await message.reply(f"Can not join user's party.")

    if "!invite" in args[0].lower():
        if len(args) != 1:
            user = await client.fetch_profile(joinedArguments)
            friend = client.get_friend(user.id)
        if len(args) == 1:
            user = await client.fetch_profile(message.author.id, cache=False, raw=False)
            friend = client.get_friend(user.id)
        if friend is None:
            await message.reply(f"Unable to invite that user, are you sure the bot has them added?")
            print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] Unable to invite user: {joinedArguments}, are you sure the bot has them added?" + Fore.WHITE)
        else:
            try:
                await friend.invite()
                await message.reply(f"Invited user: {friend.display_name}.")
                print(Fore.GREEN + f" [PYBOT] [{getTime()}] Invited user: {friend.display_name}")
            except Exception as e:
                pass
                await message.reply(f"Something went wrong trying to invite {friend.display_name}")
                print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] Something went wrong while trying to invite {friend.display_name}" + Fore.WHITE)           

    if "!add" in args[0].lower() and message.author.display_name in data['FullAccess']:
        user = await client.fetch_profile(joinedArguments)
        friends = client.friends
        if user is None:
            await message.reply(f"I can't find a player with the name of {joinedArguments}.")
            print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] Unable to find a player with the name {joinedArguments}")
        else:
            try:
                if (user.id in friends):
                    await message.reply(f"I already have {user.display_name} as a friend.")
                    print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] You already have {user.display_name} added as a friend.")
                else: 
                    await client.add_friend(user.id)
                    await message.reply(f"Sent a friend request to {user.display_name}")
                    print(Fore.GREEN + f" [PYBOT] [{getTime()}] {client.user.display_name} sent a friend request to {user.display_name}" + Fore.WHITE)
            except Exception as e:
                pass
                print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] Something went wrong adding {joinedArguments}" + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            await message.reply(f"You don't have access to this command!")

    if "!remove" in args[0].lower() and message.author.display_name in data['FullAccess']:
        user = await client.fetch_profile(joinedArguments)
        friends = client.friends
        if user is None:
            await message.reply(f"I can't find a player with the name of {joinedArguments}.")
            print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] Unable to find a player with the name {joinedArguments}")
        else:
            try:
                if (user.id in friends):
                    await client.remove_friend(user.id)
                    await message.reply(f"Sucessfully removed {user.display_name} as a friend.")
                    print(Fore.GREEN + f" [PYBOT] [{getTime()}] {client.user.display_name} removed {user.display_name} as a friend.")
                else: 
                    await message.reply(f"I don't have {user.display_name} as a friend.")
                    print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] {client.user.display_name} tried removing {user.display_name} as a friend, but the client doesn't have the friend added." + Fore.WHITE)
            except Exception as e:
                pass
                print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] Something went wrong removing {joinedArguments} as a friend." + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            await message.reply(f"You don't have access to this command!")

    if "!showfriends" in args[0].lower() and message.author.display_name in data['FullAccess']:
        friends = client.friends
        onlineFriends = []
        offlineFriends = []
        for f in friends:
            friend = client.get_friend(f)
            if friend.is_online:
                onlineFriends.append(friend.display_name)
            else:
                offlineFriends.append(friend.display_name)
        print(f" [PYBOT] [{getTime()}] " + Fore.WHITE + "Friends List: " + Fore.GREEN + f"{len(onlineFriends)} Online " + Fore.WHITE + "/" + Fore.LIGHTBLACK_EX + f" {len(offlineFriends)} Offline " + Fore.WHITE + "/" + Fore.LIGHTWHITE_EX + f" {len(onlineFriends) + len(offlineFriends)} Total")
        for x in onlineFriends:
            if x is not None:
                print(Fore.GREEN + " " + x + Fore.WHITE)
        for x in offlineFriends:
            if x is not None:
                print(Fore.LIGHTBLACK_EX + " " + x + Fore.WHITE)
        await message.reply("Check the command window for the list of my friends.")   
        if message.author.display_name not in data['FullAccess']:
            await message.reply(f"You don't have access to this command!")

    if "!members" in args[0].lower() and message.author.display_name in data['FullAccess']:
            members = client.user.party.members
            partyMembers = []
            for m in members:
                member = client.get_user(m)
                partyMembers.append(member.display_name)
            print(f" [PYBOT] [{getTime()}] " + Fore.WHITE + "There are " + Fore.LIGHTWHITE_EX + f"{len(partyMembers)} members in client's party:")
            await message.reply(f"There are {len(partyMembers)} members in {client.user.display_name}'s party:")
            for x in partyMembers:
                if x is not None:
                    print(Fore.GREEN + " " + x + Fore.WHITE)
                    await message.reply(x)

    if "!promote" in args[0].lower() and message.author.display_name in data['FullAccess']:
        if len(args) != 1:
            user = await client.fetch_profile(joinedArguments)
            member = client.user.party.members.get(user.id)
        if len(args) == 1:
            user = await client.fetch_profile(message.author.display_name)
            member = client.user.party.members.get(user.id)
        if member is None:
            await message.reply("Couldn't find that user, are you sure they're in the party?")
        else:
            try:
                await member.promote()
                await message.reply(f"Promoted user: {member.display_name}.")
                print(Fore.GREEN + f" [PYBOT] [{getTime()}] Promoted user: {member.display_name}")
            except Exception as e:
                pass
                await message.reply(f"Couldn't promote {member.display_name}, as I'm not party leader.")
                print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] Failed to promote member as I don't have the required permissions." + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            await message.reply(f"You don't have access to this command!")

    if "Playlist_" in args[0]:
        try:
            await client.user.party.set_playlist(playlist=args[0])
        except Exception as e:
            pass
            await message.reply(f"Couldn't set gamemode to {args[0]}, as I'm not party leader.")
            print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] Failed to set gamemode as I don't have the required permissions." + Fore.WHITE)

    if "!platform" in args[0] and message.author.display_name in data['FullAccess']:
        await message.reply('Setting platform to ' + args[1] + '.')
        party_id = client.user.party.id
        await client.user.party.me.leave()
        client.platform = fortnitepy.Platform(args[1])
        await message.reply('Platform set to ' + str(client.platform) + '.')
        try:
            await client.join_to_party(party_id, check_private=True)
        except Exception as e:
            pass
            await message.reply('Failed to join back as party is set to private.')
        else:
            if message.author.display_name not in data['FullAccess']:
                await message.reply(f"You don't have access to this command!")

    if args[0] == "!id":
        user = await client.fetch_profile(joinedArguments, cache=False, raw=False)
        try:
            await message.reply(f"{joinedArguments}'s Epic ID is: {user.id}")
            print(Fore.GREEN + f" [PYBOT] [{getTime()}] {joinedArguments}'s Epic ID is: {user.id}")
        except AttributeError:
            await message.reply(f"I couldn't find an Epic account with the name: {joinedArguments}.")
            print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] I couldn't find an Epic account with the name: {joinedArguments}.")

try:
    client.run()
except fortnitepy.AuthException:
    print(Fore.RED + f" [PYBOT] [{getTime()}] [ERROR] Couldn't log into the account, is config.json filled out?")
