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
    import fortnitepy
    import fortnitepy.errors
    import BenBotAsync
    import asyncio
    import aiohttp
    import datetime
    import json
    import logging
    import sys
    import crayons
    import functools
except ModuleNotFoundError as e:
    print(e)
    print('Failed to import 1 or more modules, running "INSTALL PACKAGES.bat" might fix the issue, if not please create an issue.')
    exit()

def time():
    return datetime.datetime.now().strftime('%H:%M:%S')

print(BenBotAsync.version)
print(crayons.cyan(f'[PartyBot] [{time()}] PartyBot made by xMistt. Massive credit to Terbau for creating the library.'))

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

client = fortnitepy.Client(
    email=data['email'],
    password=data['password'],
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
async def event_ready():
    print(crayons.green(f'[PartyBot] [{time()}] Client ready as {client.user.display_name}.'))

    for pending in client.pending_friends:
        friend = await pending.accept() if data["friendaccept"] else await pending.decline()
        if isinstance(friend, fortnitepy.Friend):
            print(f"[PartyBot] [{time()}] Zaakceptowano zaproszenie od: {friend.display_name}.")
        else:
            print(f"[PartyBot] [{time()}] Odrzucono zaproszenie od: {pending.display_name}.")

@client.event
async def event_party_invite(invite):
   await invite.accept()
   print(f'[PartyBot] [{time()}] Zaakceptowano zaproszenie do ekipy od {invite.sender.display_name}.')

@client.event
async def event_friend_request(request):
    print(f"[PartyBot] [{time()}] Otrzymano zaproszenie do znajomych od: {request.display_name}.")

    if data['friendaccept'] is True:
        await request.accept()
        print(f"[PartyBot] [{time()}] Zaakceptowano zaproszenie do znajomych od: {request.display_name}.")
    elif data['friendaccept'] is False:
        await request.decline()
        print(f"[PartyBot] [{time()}] Odrzucono zaproszenie do znajomych od: {request.display_name}.")

@client.event
async def event_party_member_join(member):
    await client.user.party.me.set_emote(asset=data['eid'])

    if client.user.display_name != member.display_name:
        print(f"[PartyBot] [{time()}] {member.display_name} dołączył do ekipy.")

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
            await message.reply(f"Nie znaleziono skórki z nazwą: {content}.")
            print(f"[PartyBot] [{time()}] Nie znaleziono skórki z nazwą: {content}.")
        else:
            await message.reply(f'Skórka ustawiona na {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Skórka ustawiona na: {cosmetic.id}.")
            await client.user.party.me.set_outfit(asset=cosmetic.id)
        
    elif "!backpack" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.TYPE, 'Back Bling']
        )

        if cosmetic == None:
            await message.reply(f"Nie znaleziono plecaka z nazwą: {content}.")
            print(f"[PartyBot] [{time()}] Nie znaleziono plecaka z nazwą: {content}.")
        else:
            await message.reply(f'Plecak ustawiony na {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Plecak ustawiony na: {cosmetic.id}.")
            await client.user.party.me.set_backpack(asset=cosmetic.id)

    elif "!emote" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.TYPE, 'Emote']
        )

        if cosmetic == None:
            await message.reply(f"Nie znaleziono emotki z nazwą: {content}.")
            print(f"[PartyBot] [{time()}] Nie znaleziono emotki z nazwą: {content}.")
        else:
            await message.reply(f'Emotka ustawiona na {cosmetic.displayName}.')
            print(f"[PartyBot] [{time()}] Emotka ustawiona na: {cosmetic.displayName}.")
            await client.user.party.me.set_emote(asset=cosmetic.id)

    elif "!pickaxe" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.TYPE, 'Harvesting Tool']
        )

        if cosmetic == None:
            await message.reply(f"Nie znaleziono zbieraka z nazwą: {content}.")
            print(f"[PartyBot] [{time()}] Nie znaleziono zbieraka z nazwą: {content}.")
        else:
            await message.reply(f'Zbierak ustawiony na {cosmetic.displayName}.')
            print(f"[PartyBot] [{time()}] Zbierak ustawiony na: {cosmetic.displayName}.")
            await client.user.party.me.set_pickaxe(asset=cosmetic.id)

    elif "!pet" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.BACKEND_TYPE, 'AthenaPet']
        )

        if cosmetic == None:
            await message.reply(f"Nie znaleziono pupila z nazwą: {content}.")
            print(f"[PartyBot] [{time()}] Nie znaleziono pupila z nazwą: {content}.")
        else:
            await message.reply(f'Pupil ustawiony na {cosmetic.displayName}.')
            print(f"[PartyBot] [{time()}] Pupil ustawiony na: {cosmetic.displayName}.")
            await client.user.party.me.set_backpack(asset=f'/Game/Athena/Items/Cosmetics/PetCarriers/{cosmetic.id}.{cosmetic.id}')

    elif "!emoji" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.BACKEND_TYPE, 'AthenaDance']
        )

        if cosmetic == None:
            await message.reply(f"Nie znaleziono emoji z nazwą: {content}.")
            print(f"[PartyBot] [{time()}] Nie znaleziono emoji z nazwą: {content}.")
        else:
            await message.reply(f'Ustawiono emoji na {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Ustawiono emoji na: {cosmetic.id}.")
            await client.user.party.me.set_emote(asset=f'/Game/Athena/Items/Cosmetics/Dances/Emoji/{cosmetic.id}.{cosmetic.id}')

    elif "!contrail" in args[0].lower():
        cosmetic = await BenBotAsync.get_cosmetic(
            content,
            params=BenBotAsync.Tags.NAME,
            filter=[BenBotAsync.Filters.TYPE, 'Contrail']
        )

        if cosmetic == None:
            await message.reply(f"Nie znaleziono smugi z nazwą: {content}.")
            print(f"[PartyBot] [{time()}] Nie znaleziono smugi z nazwą: {content}.")
        else:
            await message.reply(f'Smuga ustawiona na {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Smuga ustawiona na: {cosmetic.id}.")
            await client.user.party.me.set_contrail(cosmetic.id)

    elif "!purpleskull" in args[0].lower():
        variants = client.user.party.me.create_variants(
           clothing_color=1
        )

        await client.user.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=variants
        )

        await message.reply('Skórka ustawiona na Fioletowego Skull Trooper!')

    elif "!pinkghoul" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=3
        )

        await client.user.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=variants
        )

        await message.reply('Skórka ustawiona na Różową Ghoul Trooper!')

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

        await message.reply('Plecak ustawiony na Fioletowy Portal')

    elif "!banner" in args[0].lower():
        if len(args) == 1:
            await message.reply('Musisz określić jaki baner, kolor i level chcesz.')
        elif len(args) == 2:
            await client.user.party.me.set_banner(icon=args[1], color=data['banner_colour'], season_level=data['level'])
        elif len(args) == 3:
            await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=data['level'])
        elif len(args) == 4:
            await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=args[3])

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
        VTID = await BenBotAsync.vtid_to_variants(args[0])
        if VTID[1] == 'Particle':
            variants = client.user.party.me.create_variants(particle_config='Particle', particle=1)
        else:
            variants = client.user.party.me.create_variants(**{VTID[1].lower(): int(VTID[2])})

        await client.user.party.me.set_outfit(asset=VTID[0], variants=variants)
        await message.reply(f'Style ustawiono na {args[0]}.\n(Uwaga: Ta funkcja jest niewspierana, użyj !variants)')

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

        await message.reply('Skórka ustawiona na Renegade Raider w kratkę')

    elif "!mintyelf" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_051_Athena_Commando_M_HolidayElf',
            variants=variants
        )

        await message.reply('Skórka ustawiona na Miętowego Elfa!')

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
        await message.reply('For a list of commands, goto; https://github.com/xMistt/fortnitepy-bot')

    elif "PICKAXE_ID_" in args[0].lower():
        await client.user.party.me.set_pickaxe(
                asset=args[0]
        )

        await message.reply(f'Pickaxe set to {args[0]}')

    elif "petcarrier_" in args[0].lower():
        await client.user.party.me.set_backpack(
                asset=f"/Game/Athena/Items/Cosmetics/PetCarriers/{args[0]}.{args[0]}"
        )

        await message.reply(f'Pet set to {args[0]}!')

    elif "emoji_" in args[0].lower():
        await client.user.party.me.set_emote(asset='EID_ClearEmote')
        await client.user.party.me.set_emote(
                asset=f"/Game/Athena/Items/Cosmetics/Dances/Emoji/{args[0]}.{args[0]}"
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
        await client.user.party.me.set_ready(True)
        await message.reply('Ready!')

    elif ("!unready" in args[0].lower()) or ("!sitin" in args[0].lower()):
        await client.user.party.me.set_ready(False)
        await message.reply('Unready!')

    elif "!sitout" in args[0].lower():
        await client.user.party.me.set_ready(None)
        await message.reply('Przeczekuje!')

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
        await message.reply('Dowidzenia!')
        print(f'[PartyBot] [{time()}] Wyszłem z ekipy tak jak poproszono')

    elif "!kick" in args[0].lower():
        user = await client.fetch_profile(content)
        member = client.user.party.members.get(user.id)
        if member is None:
            await message.reply("Nie znaleziono tego użytkownika. Czy jesteś pewien, że jest w ekipie?")
        else:
            try:
                await member.kick()
                await message.reply(f"Wyrzucono: {member.display_name}.")
                print(f"[PartyBot] [{time()}] Wyrzucono: {member.display_name}")
            except fortnitepy.Forbidden:
                await message.reply(f"Nie mogę wyrzucić {member.display_name}, ponieważ nie jestem liderem")
                print(crayons.red(f"[PartyBot] [{time()}] [ERROR] Nie udało się wywalić członka ekipy, ponieważ nie mam uprawnień"))

    elif "!promote" in args[0].lower():
        if len(args) != 1:
            user = await client.fetch_profile(content)
            member = client.user.party.members.get(user.id)
        if len(args) == 1:
            user = await client.fetch_profile(message.author.display_name)
            user = await client.user.party.members.get(user.id)

        if member is None:
            await message.reply("Nie znaleziono tego użytkownika. Czy jesteś pewien, że jest w ekipie?")
        else:
            try:
                await member.promote()
                await message.reply(f"Oddano lidera: {member.display_name}.")
                print(f"[PartyBot] [{time()}] Oddano lidera: {member.display_name}")
            except fortnitepy.Forbidden:
                await message.reply(f"Nie można oddać lidera {member.display_name}, ponieważ nie jestem liderem")
                print(crayons.red(f"[PartyBot] [{time()}] [ERROR] Nie można oddać lidera, ponieważ nie jestem liderem"))

    elif "playlist_" in args[0].lower():
        try:
            await client.user.party.set_playlist(playlist=args[0])
        except fortnitepy.Forbidden:
            await message.reply(f"Nie można zmienić trybu {args[1]}, ponieważ nie jestem liderem")
            print(crayons.red(f"[PartyBot] [{time()}] [ERROR] Nie można zmienić trybu, ponieważ nie jestem liderem"))

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
            await message.reply(f"{content} Epic ID to: {user.id}")
        except AttributeError:
            await message.reply(f"Nie można znaleźć konta epic z nazwą: {content}.")

try:
    client.run()
except fortnitepy.AuthException:
    print(crayons.red(f"[PartyBot] [{time()}] [ERROR] Nieprawidłowe informacje do logowania."))
