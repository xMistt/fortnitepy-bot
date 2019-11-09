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

try:
    import fortnitepy, fortnitepy.errors, BenBotAsync, asyncio
    import aiohttp
    import getpass
    import time as delay
    import datetime
    import json
    import logging
    import sys
    from colorama import init
    init(autoreset=True)
    from colorama import Fore, Back, Style
except ModuleNotFoundError:
    print('\u001b[31m' + f'[FORTNITEPY] [N/A] [ERROR] Failed to import 1 or more modules, run "INSTALL PACKAGES.bat".')
    exit()

time = datetime.datetime.now().strftime('%H:%M:%S')
print(f'[FORTNITEPY] [{time}] fortnitepy-bot made by xMistt. credit to Terbau for creating the library.')
print(f"[FORTNITEPY] [{time}] If you have paid for this program, you have been scammed. I'd advise you try and get a refund. This is an open-source free program.")

def debugOn():
    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

with open('config.json') as f:
    print(f'[FORTNITEPY] [{time}] Loading config.')
    data = json.load(f)
    print(f'[FORTNITEPY] [{time}] Config loaded.')
    
if data['debug'] == 'True':
    print(f'[FORTNITEPY] [{time}] Debug logging is on, prepare for a shitstorm.')
    debugOn()
else:
    print(f'[FORTNITEPY] [{time}] Debug logging is off.')

client = fortnitepy.Client(
    email=data['email'],
    password=data['password'],
    status=data['status'],
    platform=fortnitepy.Platform(data['platform'])
)

async def setVTID(VTID):
    url = f'http://benbotfn.tk:8080/api/assetProperties?file=FortniteGame/Content/Athena/Items/CosmeticVariantTokens/{VTID}.uasset'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            fileLocation = await r.json()

            SkinCID = fileLocation['export_properties'][0]['cosmetic_item']
            VariantChanelTag = fileLocation['export_properties'][0]['VariantChanelTag']['TagName']
            VariantNameTag = fileLocation['export_properties'][0]['VariantNameTag']['TagName']

            VariantType = VariantChanelTag.split('Cosmetics.Variant.Channel.')[1].split('.')[0]

            VariantInt = int("".join(filter(lambda x: x.isnumeric(), VariantNameTag)))

            if VariantType == 'ClothingColor':
                return SkinCID, 'clothing_color', VariantInt
            else:
                return SkinCID, VariantType, VariantInt


@client.event
async def event_ready():
    print(Fore.GREEN + '[FORTNITEPY] [' + time + '] Client ready as {0.user.display_name}.'.format(client))

@client.event
async def event_party_invite(invite):
    await invite.accept()
    print(f'[FORTNITEPY] [{time}] Accepted party invite.')

@client.event
async def event_friend_request(request):
    print(f"[FORTNITEPY] [{time}] Recieved friend request from: {request.display_name}.")

    if data['friendaccept'].lower() == 'true':
        await request.accept()
        print(f"[FORTNITEPY] [{time}] Accepted friend request from: {request.display_name}.")
    if data['freindaccept'].lower() == 'false':
        await request.decline()
        print(f"[FORTNITEPY] [{time}] Declined friend request from: {request.display_name}.")

@client.event
async def event_party_member_join(member):
    await client.user.party.me.set_outfit(asset=data['cid'])
    await client.user.party.me.set_backpack(asset=data['bid'])
    await client.user.party.me.set_banner(icon=data['banner'], color=data['banner_colour'], season_level=data['level'])
    delay.sleep(2)
    await client.user.party.me.set_emote(asset=data['eid'])
    await client.user.party.me.set_battlepass_info(has_purchased=True, level=data['bp_tier'], self_boost_xp='0', friend_boost_xp='0')
    
    if client.user.display_name != member.display_name:
        print(f"[FORTNITEPY] [{time}] {member.display_name} has joined the lobby.")

@client.event
async def event_friend_message(message):
    args = message.content.split()
    split = args[1:]
    joinedArguments = " ".join(split)
    print('[FORTNITEPY] [' + time + '] {0.author.display_name}: {0.content}'.format(message))

    if "!skin" in args[0].lower():
        id = await BenBotAsync.getSkinId(joinedArguments)
        if id == None:
            await message.reply(f"Couldn't find a skin with the name: {joinedArguments}")
        else:
            await client.user.party.me.set_outfit(asset=id)
            await message.reply('Skin set to ' + id)
            print(f"[FORTNITEPY] [{time}] Set Skin to: " + id)
        
    if "!backpack" in args[0].lower():
        id = await BenBotAsync.getBackpackId(joinedArguments)
        if id == None:
            await message.reply(f"Couldn't find a backpack with the name: {joinedArguments}")
        else:
            await client.user.party.me.set_backpack(asset=id)
            await message.reply('Backpack set to ' + id)
            print(f"[FORTNITEPY] [{time}] Set Backpack to: " + id)

    if "!emote" in args[0].lower():
        await client.user.party.me.clear_emote()
        id = await BenBotAsync.getEmoteId(joinedArguments)
        if id == None:
            await message.reply(f"Couldn't find a skin with the name: {joinedArguments}")
        else:
            await client.user.party.me.set_emote(asset=id)
            await message.reply('Skin set to ' + id)
            print(f"[FORTNITEPY] [{time}] Set Skin to: " + id)

    if "!pickaxe" in args[0].lower():
        id = await BenBotAsync.getPickaxeId(joinedArguments)
        if id == None:
            await message.reply(f"Couldn't find a pickaxe with the name: {joinedArguments}")
        else:
            await client.user.party.me.set_pickaxe(asset=id)
            await message.reply('Pickaxe set to ' + id)
            print(f"[FORTNITEPY] [{time}] Set Pickaxe to: " + id)

    if "!pet" in args[0].lower():
        id = await BenBotAsync.getPetId(joinedArguments)
        await client.user.party.me.set_backpack(
                asset="/Game/Athena/Items/Cosmetics/PetCarriers/" + id + "." + id
        )

        await message.reply('Pet set to ' + id)
        print(f"[FORTNITEPY] [{time}] Client's PetCarrier set to: " + id)

    if "!emoji" in args[0].lower():
        id = await fetch_cosmetic_id(' '.join(split), 'AthenaDance')
        await client.user.party.me.clear_emote()
        await client.user.party.me.set_emote(
                asset="/Game/Athena/Items/Cosmetics/Dances/Emoji/" + id + "." + id
        )

        await message.reply('Emoji set to ' + id)
        print(f"[FORTNITEPY] [{time}] Client's Emoji set to " + id)

    if "!purpleskull" in args[0].lower():
        variants = client.user.party.me.create_variants(
           clothing_color=1
        )

        await client.user.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Purple Skull Trooper!')

    if "!pinkghoul" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=3
        )

        await client.user.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Pink Ghoul Trooper!')

    if "!brainiacghoul" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Brainiac Ghoul Trooper!')

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
        print(f"[FORTNITEPY] [{time}] Banner set to; {args[1]} {args[2]} {args[3]}")

    if "CID_" in args[0]:
        await client.user.party.me.set_outfit(
            asset=args[0]
        )

        await message.reply(f'Skin set to {args[0]}')
        await print(f'[FORTNITEPY] [{time}] Skin set to ' + args[0])

    if "VTID_" in args[0]:
        VTID = await setVTID(args[0])
        if VTID[1] == 'Particle':
            variants = client.user.party.me.create_variants(particle_config='Particle', particle=1)
        else:
            variants = client.user.party.me.create_variants(**{VTID[1].lower(): int(VTID[2])})

        await client.user.party.me.set_outfit(asset=VTID[0], variants=variants)
        await message.reply(f'Variants set to {args[0]}.\n(Warning: This feature is not supported, please use !variants)')

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
        print(f'[FORTNITEPY] [{time}] Set variants of {args[1]} to {args[2]} {args[3]}.')

    if "!checkeredrenegade" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
            variants=variants
        )

        await message.reply('Skin set to Checkered Renegade!')

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

    if "!help" in args[0].lower():
        await message.reply('For a list of commands, goto; https://github.com/xMistt/fortnitepy-bot')

    if "PICKAXE_ID_" in args[0].lower():
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
        await client.user.party.me.set_ready(None)
        await message.reply('Sitting Out!')

    if "!bp" in args[0].lower():
        await client.user.party.me.set_battlepass_info(has_purchased=True, level=args[1], self_boost_xp='0', friend_boost_xp='0')

    if "!level" in args[0].lower():
        await client.user.party.me.set_banner(icon=client.user.party.me.banner[0], color=client.user.party.me.banner[1], season_level=args[1])

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
        if len(args) != 1:
            user = await client.fetch_profile(joinedArguments)
            member = client.user.party.members.get(user.id)
        if len(args) == 1:
            user = await client.fetch_profile(message.author.display_name)
            user = await client.user.party.members.get(user.id)

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

    if "!platform" in args[0]:
        await message.reply('Setting platform to ' + args[1] + '.')
        party_id = client.user.party.id
        await client.user.party.me.leave()
        client.platform = fortnitepy.Platform(args[1])
        await message.reply('Platform set to ' + str(client.platform) + '.')
        try:
            await client.join_to_party(party_id, check_private=True)
        except fortnitepy.Forbidden:
            await message.reply('Failed to join back as party is set to private.')

    if args[0] == "!id":
        user = await client.fetch_profile(joinedArguments, cache=False, raw=False)
        try:
            await message.reply(f"{joinedArguments}'s Epic ID is: {user.id}")
        except AttributeError:
            await message.reply(f"I couldn't find an Epic account with the name: {joinedArguments}.")

if bool(data['email']) == False or bool(data['password']) == False:
    with open('config.json', 'w') as file:
        data['email'] = input('Email: ')
        data['password'] = getpass.getpass()
        json.dump(data, file, sort_keys=False, indent=4)
    exit()

try:
    client.run()
except fortnitepy.AuthException:
    print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Invalid account credentials.")
    
