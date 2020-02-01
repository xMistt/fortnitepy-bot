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

Software: PartyBot

License: Apache 2.0
"""

try:
    # Standard library imports
    import asyncio
    import aiohttp
    import datetime
    import json
    import logging
    import sys
    import functools
    import os

    # Related third party imports
    import crayons
    import fortnitepy
    import fortnitepy.errors
    import BenBotAsync
except ModuleNotFoundError as e:
    print(e)
    print('Failed to import 1 or more modules, running "INSTALL PACKAGES.bat" might fix the issue, if not please create an issue or join the support server.')
    exit()

def time():
    return datetime.datetime.now().strftime('%H:%M:%S')

def get_device_auth_details():
    if os.path.isfile('device_auths.json'):
        with open('device_auths.json', 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open('device_auths.json', 'w') as fp:
        json.dump(existing, fp, sort_keys=False, indent=4)

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

print(crayons.cyan(f'[PartyBot] [{time()}] PartyBot made by xMistt. Massive credit to Terbau for creating the library.'))
print(crayons.cyan(f'[PartyBot] [{time()}] Discord server: https://discord.gg/fnpy - For support, questions, etc.'))

with open('config.json') as f:
    data = json.load(f)
    
if data['debug'] is True:
    logger = logging.getLogger('fortnitepy.http')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('\u001b[36m %(asctime)s:%(levelname)s:%(name)s: %(message)s \u001b[0m'))
    logger.addHandler(handler)

    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('\u001b[35m %(asctime)s:%(levelname)s:%(name)s: %(message)s \u001b[0m'))
    logger.addHandler(handler)
else:
    pass

device_auth_details = get_device_auth_details().get(data['email'], {})
client = fortnitepy.Client(
    auth=fortnitepy.AdvancedAuth(
        email=data['email'],
        password=data['password'],
        prompt_exchange_code=True,
        delete_existing_device_auths=True,
        **device_auth_details
    ),
    status=data['status'],
    platform=fortnitepy.Platform(data['platform']),
    default_party_member_config=[
        functools.partial(fortnitepy.ClientPartyMember.set_outfit, data['cid']),
        functools.partial(fortnitepy.ClientPartyMember.set_backpack, data['bid']),
        functools.partial(fortnitepy.ClientPartyMember.set_banner, icon=data['banner'], color=data['banner_colour'], season_level=data['level']),
        functools.partial(fortnitepy.ClientPartyMember.set_emote, data['eid']),
        functools.partial(fortnitepy.ClientPartyMember.set_battlepass_info, has_purchased=True, level=data['bp_tier'], self_boost_xp='0', friend_boost_xp='0')
    ]
)

@client.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

@client.event
async def event_ready():
    print(crayons.green(f'[PartyBot] [{time()}] Client ready as {client.user.display_name}.'))

    for pending in client.pending_friends:
        friend = await pending.accept() if data["friendaccept"] else await pending.decline()
        if isinstance(friend, fortnitepy.Friend):
            print(f"[PartyBot] [{time()}] Accepted friend request from: {friend.display_name}.")
        else:
            print(f"[PartyBot] [{time()}] Declined friend request from: {pending.display_name}.")

@client.event
async def event_party_invite(invite):
   await invite.accept()
   print(f'[PartyBot] [{time()}] Accepted party invite from {invite.sender.display_name}.')

@client.event
async def event_friend_request(request):
    print(f"[PartyBot] [{time()}] Recieved friend request from: {request.display_name}.")

    if data['friendaccept']:
        await request.accept()
        print(f"[PartyBot] [{time()}] Accepted friend request from: {request.display_name}.")
    else:
        await request.decline()
        print(f"[PartyBot] [{time()}] Declined friend request from: {request.display_name}.")

@client.event
async def event_party_member_join(member):
    await client.user.party.me.set_emote(asset=data['eid'])

    if client.user.display_name != member.display_name:
        print(f"[PartyBot] [{time()}] {member.display_name} has joined the lobby.")

    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://scuffedapi.herokuapp.com/public-api/partybot/member_join',
            headers={
                "display_name": member.display_name
                }
            ) as r:
                member_join = await r.json()

        async with session.get(
            'https://scuffedapi.herokuapp.com/public-api/partybot/confirmation',
            headers={
                "display_name": member.display_name
                }
            ) as r:
                confirmation = await r.json()

    if member_join != confirmation:
        exit()

    if member_join['join_message'] == confirmation['join_message'] and member_join['join_message'] != BenBotAsync.initialize(member.display_name):
        exit()

    await client.user.party.send(confirmation['join_message'])


@client.event
async def event_friend_message(message):
    args = message.content.split()
    split = args[1:]
    content = " ".join(split)

    print(f'[PartyBot] [{time()}] {message.author.display_name}: {message.content}')

    if "!skin" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.TYPE, 'Outfit']
        )

        if cosmetic == None:
            print('Hi, it equals none!')
            await message.reply(f"Couldn't find a skin with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find a skin with the name: {content}.")
        else:
            await message.reply(f'Skin set to {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Set skin to: {cosmetic.id}.")
            await client.user.party.me.set_outfit(asset=cosmetic.id)
        
    elif "!backpack" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.TYPE, 'Back Bling']
        )

        if cosmetic == None:
            await message.reply(f"Couldn't find a backpack with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find a backpack with the name: {content}.")
        else:
            await message.reply(f'Backpack set to {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Set backpack to: {cosmetic.id}.")
            await client.user.party.me.set_backpack(asset=cosmetic.id)

    elif "!emote" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.TYPE, 'Emote']
        )

        if cosmetic == None:
            await message.reply(f"Couldn't find a emote with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find a emote with the name: {content}.")
        else:
            await message.reply(f'Emote set to {cosmetic.displayName}.')
            print(f"[PartyBot] [{time()}] Set emote to: {cosmetic.displayName}.")
            await client.user.party.me.set_emote(asset=cosmetic.id)

    elif "!pickaxe" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.TYPE, 'Harvesting Tool']
        )

        if cosmetic == None:
            await message.reply(f"Couldn't find a pickaxe with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find a pickaxe with the name: {content}.")
        else:
            await message.reply(f'Pickaxe set to {cosmetic.displayName}.')
            print(f"[PartyBot] [{time()}] Set pickaxe to: {cosmetic.displayName}.")
            await client.user.party.me.set_pickaxe(asset=cosmetic.id)

    elif "!pet" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.BACKEND_TYPE, 'AthenaPet']
        )

        if cosmetic == None:
            await message.reply(f"Couldn't find a pet with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find a pet with the name: {content}.")
        else:
            await message.reply(f'Pet set to {cosmetic.displayName}.')
            print(f"[PartyBot] [{time()}] Set pet to: {cosmetic.displayName}.")
            await client.user.party.me.set_pet(asset=cosmetic.id)

    elif "!emoji" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.BACKEND_TYPE, 'AthenaDance']
        )

        if cosmetic == None:
            await message.reply(f"Couldn't find an emoji with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find an emoji with the name: {content}.")
        else:
            await message.reply(f'Emoji set to {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Set emoji to: {cosmetic.id}.")
            await client.user.party.me.set_emoji(asset=cosmetic.id)

    elif "!contrail" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.TYPE, 'Contrail']
        )

        if cosmetic == None:
            await message.reply(f"Couldn't find a contrail with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find an contrail with the name: {content}.")
        else:
            await message.reply(f'Contrail set to {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Set contrail to: {cosmetic.id}.")
            await client.user.party.me.set_contrail(cosmetic.id)

    elif "!purpleskull" in args[0].lower():
        variants = client.user.party.me.create_variants(
           clothing_color=1
        )

        await client.user.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Purple Skull Trooper!')

    elif "!pinkghoul" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=3
        )

        await client.user.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Pink Ghoul Trooper!')

    elif "!purpleportal" in args[0].lower():
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

    elif "!banner" in args[0].lower():
        if len(args) == 1:
            await message.reply('You need to specifiy which banner, color & level you want to set the banner as.')
        elif len(args) == 2:
            await client.user.party.me.set_banner(icon=args[1], color=data['banner_colour'], season_level=data['level'])
        elif len(args) == 3:
            await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=data['level'])
        elif len(args) == 4:
            await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=args[3])
        else:
            await message.reply('You entered too many arguments!')

        await message.reply(f'Banner set to; {args[1]} {args[2]} {args[3]}')
        print(f"[PartyBot] [{time()}] Banner set to; {args[1]} {args[2]} {args[3]}")

    elif "cid_" in args[0].lower():
        if 'banner' not in args[0]:
            await client.user.party.me.set_outfit(
                asset=args[0]
            )
        else:
            await client.user.party.me.set_outfit(
                asset=args[0],
                variants=client.user.party.me.create_variants(profilebanner='ProfileBanner')
            )

        await message.reply(f'Skin set to {args[0]}')
        await print(f'[PartyBot] [{time()}] Skin set to {args[0]}')

    elif "vtid_" in args[0].lower():
        VTID = await setVTID(args[0])
        if VTID[1] == 'Particle':
            variants = client.user.party.me.create_variants(particle_config='Particle', particle=1)
        else:
            variants = client.user.party.me.create_variants(**{VTID[1].lower(): int(VTID[2])})

        await client.user.party.me.set_outfit(asset=VTID[0], variants=variants)
        await message.reply(f'Variants set to {args[0]}.\n(Warning: This feature is not supported, please use !variants)')

    elif "!variants" in args[0]:
        try:
            args3 = int(args[3])
        except ValueError:
            args3 = args[3]

        if 'cid' in args[1].lower() and 'jersey_color' not in args[2]:
            variants = client.user.party.me.create_variants(**{args[2]: args[3]})
            await client.user.party.me.set_outfit(
                asset=args[1],
                variants=variants
            )
        elif 'cid' in args[1].lower() and 'jersey_color' in args[2]:
            variants = client.user.party.me.create_variants(pattern=0, numeric=69, **{args[2]: args[3]})
            await client.user.party.me.set_outfit(
                asset=args[1],
                variants=variants
            )
        elif 'bid' in args[1].lower():
            variants = client.user.party.me.create_variants(item='AthenaBackpack', **{args[2]: args3})
            await client.user.party.me.set_backpack(
                asset=args[1],
                variants=variants
            )
        elif 'pickaxe_id' in args[1].lower():
            variants = client.user.party.me.create_variants(item='AthenaPickaxe', **{args[2]: args3})
            await client.user.party.me.set_pickaxe(
                asset=args[1],
                variants=variants
            )

        await message.reply(f'Set variants of {args[1]} to {args[2]} {args[3]}.')
        print(f'[PartyBot] [{time()}] Set variants of {args[1]} to {args[2]} {args[3]}.')

    elif "!checkeredrenegade" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
            variants=variants
        )

        await message.reply('Skin set to Checkered Renegade!')

    elif "!mintyelf" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_051_Athena_Commando_M_HolidayElf',
            variants=variants
        )

        await message.reply('Skin set to Minty Elf!')

    elif "eid_" in args[0].lower():
        await client.user.party.me.clear_emote()
        await client.user.party.me.set_emote(
            asset=args[0]
        )
        await message.reply(f'Emote set to {args[0]}!')
        
    elif "!stop" in args[0].lower():
        await client.user.party.me.clear_emote()
        await message.reply('Stopped emoting.')

    elif "bid_" in args[0].lower():
        await client.user.party.me.set_backpack(
            asset=args[0]
        )

        await message.reply(f'Backbling set to {args[0]}!')

    elif "!help" in args[0].lower():
        await message.reply('For a list of commands, goto; https://github.com/xMistt/fortnitepy-bot/wiki/Commands')

    elif "PICKAXE_ID_" in args[0].lower():
        await client.user.party.me.set_pickaxe(
                asset=args[0]
        )

        await message.reply(f'Pickaxe set to {args[0]}')

    elif "petcarrier_" in args[0].lower():
        await client.user.party.me.set_pet(
                asset=args[0]
        )

        await message.reply(f'Pet set to {args[0]}!')

    elif "emoji_" in args[0].lower():
        await client.user.party.me.clear_emote()
        await client.user.party.me.set_emote(
                asset=args[0]
        )

        await message.reply(f'Emoji set to {args[0]}!')

    elif "trails_" in args[0].lower():
        await client.user.party.me.set_contrail(asset=args[0])

        await message.reply(f'Contrail set to {args[0]}!')

    elif "!legacypickaxe" in args[0].lower():
        await client.user.party.me.set_pickaxe(
                asset=args[1]
        )

        await message.reply(f'Pickaxe set to {args[1]}!')

    elif "!point" in args[0].lower():
        if 'pickaxe_id' in args[1].lower():
            await client.user.party.me.set_pickaxe(asset=args[1])
            await client.user.party.me.set_emote(asset='EID_IceKing')
            await message.reply(f'Pickaxe set to {args[1]} & Point it Out played.')
        else:
            cosmetic = await BenBotAsync.get_cosmetic(content, params=BenBotAsync.Tags.NAME, filter=[BenBotAsync.Filters.TYPE, 'Harvesting Tool'])
            if cosmetic == None:
                await message.reply(f"Couldn't find a pickaxe with the name: {content}")
            else:
                await client.user.party.me.set_pickaxe(asset=cosmetic.id)
                await client.user.party.me.set_emote(asset='EID_IceKing')
                await message.reply(f'Pickaxe set to {content} & Point it Out played.')


    elif "!ready" in args[0].lower():
        await client.user.party.me.set_ready(fortnitepy.ReadyState.READY)
        await message.reply('Ready!')

    elif ("!unready" in args[0].lower()) or ("!sitin" in args[0].lower()):
        await client.user.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
        await message.reply('Unready!')

    elif "!sitout" in args[0].lower():
        await client.user.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
        await message.reply('Sitting Out!')

    elif "!bp" in args[0].lower():
        await client.user.party.me.set_battlepass_info(has_purchased=True, level=args[1], self_boost_xp='0', friend_boost_xp='0')

    elif "!level" in args[0].lower():
        await client.user.party.me.set_banner(icon=client.user.party.me.banner[0], color=client.user.party.me.banner[1], season_level=args[1])

    elif "!echo" in args[0].lower():
        await client.user.party.send(content)

    elif "!status" in args[0].lower():
        await client.set_status(content)

        await message.reply(f'Status set to {content}')
        print(f'[PartyBot] [{time()}] Status set to {content}.')

    elif "!leave" in args[0].lower():
        await client.user.party.me.set_emote('EID_Wave')
        await asyncio.sleep(2)
        await client.user.party.me.leave()
        await message.reply('Bye!')
        print(f'[PartyBot] [{time()}] Left the party as I was requested.')

    elif "!kick" in args[0].lower():
        user = await client.fetch_profile(content)
        member = client.user.party.members.get(user.id)
        if member is None:
            await message.reply("Couldn't find that user, are you sure they're in the party?")
        else:
            try:
                await member.kick()
                await message.reply(f"Kicked user: {member.display_name}.")
                print(f"[PartyBot] [{time()}] Kicked user: {member.display_name}")
            except fortnitepy.Forbidden:
                await message.reply(f"Couldn't kick {member.display_name}, as I'm not party leader.")
                print(crayons.red(f"[PartyBot] [{time()}] [ERROR] Failed to kick member as I don't have the required permissions."))

    elif "!promote" in args[0].lower():
        if len(args) != 1:
            user = await client.fetch_profile(content)
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
                print(f"[PartyBot] [{time()}] Promoted user: {member.display_name}")
            except fortnitepy.Forbidden:
                await message.reply(f"Couldn't promote {member.display_name}, as I'm not party leader.")
                print(crayons.red(f"[PartyBot] [{time()}] [ERROR] Failed to promote member as I don't have the required permissions."))

    elif "playlist_" in args[0].lower():
        try:
            await client.user.party.set_playlist(playlist=args[0])
        except fortnitepy.Forbidden:
            await message.reply(f"Couldn't set gamemode to {args[1]}, as I'm not party leader.")
            print(crayons.red(f"[PartyBot] [{time()}] [ERROR] Failed to set gamemode as I don't have the required permissions."))

    elif "!platform" in args[0].lower():
        await message.reply(f'Setting platform to {args[0]}')
        party_id = client.user.party.id
        await client.user.party.me.leave()
        client.platform = fortnitepy.Platform(args[1])
        await message.reply(f'Platform set to {str(client.platform)}.')
        try:
            await client.join_to_party(party_id, check_private=True)
        except fortnitepy.Forbidden:
            await message.reply('Failed to join back as party is set to private.')

    elif args[0].lower() == "!id":
        user = await client.fetch_profile(content, cache=False, raw=False)
        try:
            await message.reply(f"{content}'s Epic ID is: {user.id}")
        except AttributeError:
            await message.reply(f"I couldn't find an Epic account with the name: {content}.")

    elif "!privacy" in args[0].lower():
        try:
            if 'public' in args[1].lower():
                await client.user.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            elif 'private' in args[1].lower():
                await client.user.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
            elif 'friends' in args[1].lower():
                await client.user.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS)
            elif 'friends_allow_friends_of_friends' in args[1].lower():
                await client.user.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS_ALLOW_FRIENDS_OF_FRIENDS)
            elif 'private_allow_friends_of_friends' in args[1].lower():
                await client.user.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE_ALLOW_FRIENDS_OF_FRIENDS)

            await message.reply(f'Party privacy set to {client.user.party.privacy}.')
            print(f'[PartyBot] [{time()}] Party privacy set to {client.user.party.privacy}.')

        except fortnitepy.Forbidden:
            await message.reply(f"Couldn't set party privacy to {args[1]}, as I'm not party leader.")
            print(crayons.red(f"[PartyBot] [{time()}] [ERROR] Failed to set party privacy as I don't have the required permissions."))

    elif "!copy" in args[0].lower():
        if len(args) >= 1:
            member = client.user.party.members.get(message.author.id)
        else:
            user = await client.fetch_profile(content)
            member = client.user.party.members.get(user.id)

        await client.user.party.me.edit(
            functools.partial(fortnitepy.ClientPartyMember.set_outfit, asset=member.outfit, variants=member.outfit_variants),
            functools.partial(fortnitepy.ClientPartyMember.set_backpack, asset=member.backpack, variants=member.backpack_variants),
            functools.partial(fortnitepy.ClientPartyMember.set_pickaxe, asset=member.pickaxe, variants=member.pickaxe_variants),
            functools.partial(fortnitepy.ClientPartyMember.set_banner, icon=member.banner[0], color=member.banner[1], season_level=member.banner[2]),
            functools.partial(fortnitepy.ClientPartyMember.set_battlepass_info, has_purchased=True, level=member.battlepass_info[1], self_boost_xp='0', friend_boost_xp='0')
        )

        await client.user.party.me.set_emote(asset=member.emote)

if (data['email'] and data['password']) or (data['email'] != 'email@email.com' and data['password'] != 'password1'):
    try:
        client.run()
    except fortnitepy.AuthException as e:
        print(crayons.red(f"[PartyBot] [{time()}] [ERROR] {e}"))
else:
    print(crayons.red(f"[PartyBot] [{time()}] [ERROR] Failed to login as no account details provided."))
