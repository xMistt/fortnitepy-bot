# -*- coding: utf-8 -*-

"""
“Commons Clause” License Condition v1.0
Copyright Oli 2019-2020

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
    from typing import Tuple
    import random

    # Related third party imports
    import crayons
    import fortnitepy
    import fortnitepy.errors
    import BenBotAsync

except ModuleNotFoundError as e:
    print(e)
    print('Failed to import 1 or more modules, running "INSTALL PACKAGES.bat"'
          'might fix the issue, if not please create an issue or join'
          'the support server.')
    sys.exit()

# Imports uvloop and uses it if installed (Unix only).
try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def time() -> str:
    return datetime.datetime.now().strftime('%H:%M:%S')


def get_device_auth_details() -> dict:
    if os.path.isfile('device_auths.json'):
        with open('device_auths.json', 'r') as fp:
            return json.load(fp)
    else:
        with open('device_auths.json', 'w+') as fp:
            fp.write('{}')
            
    return {}


def store_device_auth_details(email: str, details: dict) -> None:
    existing = get_device_auth_details()
    existing[email] = details

    with open('device_auths.json', 'w') as fp:
        json.dump(existing, fp, sort_keys=False, indent=4)


async def set_vtid(vtid: str) -> Tuple[str, str, int]:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='https://benbotfn.tk/api/v1/assetProperties',
            params={
                'path': 'FortniteGame/Content/Athena/'
                        f'Items/CosmeticVariantTokens/{vtid}.uasset'
            })

        response = await request.json()

    file_location = response['export_properties'][0]

    skin_cid = file_location['cosmetic_item']
    variant_channel_tag = file_location['VariantChanelTag']['TagName']
    variant_name_tag = file_location['VariantNameTag']['TagName']

    variant_type = variant_channel_tag.split(
        'Cosmetics.Variant.Channel.'
    )[1].split('.')[0]

    variant_int = int("".join(filter(
        lambda x: x.isnumeric(), variant_name_tag
    )))

    if variant_type == 'ClothingColor':
        return skin_cid, 'clothing_color', variant_int
    else:
        return skin_cid, variant_type, variant_int


print(crayons.cyan(f'[PartyBot] [{time()}] PartyBot made by xMistt. '
                   'Massive credit to Terbau for creating the library.'))
print(crayons.cyan(f'[PartyBot] [{time()}] Discord server: https://discord.gg/fnpy - For support, questions, etc.'))

with open('config.json') as f:
    data = json.load(f)

if data['debug']:
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
    platform=fortnitepy.Platform(data['platform'])
)


@client.event
async def event_device_auth_generate(details: dict, email: str) -> None:
    store_device_auth_details(email, details)


@client.event
async def event_ready() -> None:
    print(crayons.green(f'[PartyBot] [{time()}] Client ready as {client.user.display_name}.'))

    for pending in list(client.pending_friends.values()):
        if pending.direction == 'INBOUND':
            friend = await pending.accept() if data["friendaccept"] else await pending.decline()
            if isinstance(friend, fortnitepy.Friend):
                print(f"[PartyBot] [{time()}] Accepted friend request from: {friend.display_name}.")
            else:
                print(f"[PartyBot] [{time()}] Declined friend request from: {pending.display_name}.")


@client.event
async def event_party_invite(invite: fortnitepy.PartyInvitation) -> None:
    await invite.accept()
    print(f'[PartyBot] [{time()}] Accepted party invite from {invite.sender.display_name}.')


@client.event
async def event_friend_request(request: fortnitepy.PendingFriend) -> None:
    print(f"[PartyBot] [{time()}] Received friend request from: {request.display_name}.")

    if data['friendaccept']:
        await request.accept()
        print(f"[PartyBot] [{time()}] Accepted friend request from: {request.display_name}.")
    else:
        await request.decline()
        print(f"[PartyBot] [{time()}] Declined friend request from: {request.display_name}.")


@client.event
async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
    await BenBotAsync.set_default_loadout(client, data, member)


@client.event
async def event_friend_message(message: fortnitepy.FriendMessage) -> None:
    args = message.content.split()
    split = args[1:]
    content = " ".join(split)

    print(f'[PartyBot] [{time()}] {message.author.display_name}: {message.content}')

    if "!skin" in args[0].lower():
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaCharacter"
            )

            await message.reply(f'Skin set to {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Set skin to: {cosmetic.id}.")
            await client.user.party.me.set_outfit(asset=cosmetic.id)

        except BenBotAsync.exceptions.NotFound:
            await message.reply(f"Couldn't find a skin with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find a skin with the name: {content}.")

    elif "!backpack" in args[0].lower():
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )

            await message.reply(f'Backpack set to {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Set backpack to: {cosmetic.id}.")
            await client.user.party.me.set_backpack(asset=cosmetic.id)

        except BenBotAsync.exceptions.NotFound:
            await message.reply(f"Couldn't find a backpack with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find a backpack with the name: {content}.")

    elif "!emote" in args[0].lower():
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )

            await message.reply(f'Emote set to {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Set emote to: {cosmetic.id}.")
            await client.user.party.me.clear_emote()
            await client.user.party.me.set_emote(asset=cosmetic.id)

        except BenBotAsync.exceptions.NotFound:
            await message.reply(f"Couldn't find an emote with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find an emote with the name: {content}.")

    elif "!pickaxe" in args[0].lower():
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )

            await message.reply(f'Pickaxe set to {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Set pickaxe to: {cosmetic.id}.")
            await client.user.party.me.set_pickaxe(asset=cosmetic.id)

        except BenBotAsync.exceptions.NotFound:
            await message.reply(f"Couldn't find a pickaxe with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find a pickaxe with the name: {content}.")

    elif "!pet" in args[0].lower():
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPet"
            )

            await message.reply(f'Pet set to {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Set pet to: {cosmetic.id}.")
            await client.user.party.me.set_pet(asset=cosmetic.id)

        except BenBotAsync.exceptions.NotFound:
            await message.reply(f"Couldn't find a pet with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find a pet with the name: {content}.")

    elif "!emoji" in args[0].lower():
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaEmoji"
            )

            await message.reply(f'Pet set to {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Set pet to: {cosmetic.id}.")
            await client.user.party.me.set_emoji(asset=cosmetic.id)

        except BenBotAsync.exceptions.NotFound:
            await message.reply(f"Couldn't find an emoji with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find an emoji with the name: {content}.")

    elif "!contrail" in args[0].lower():
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaSkyDiveContrail"
            )

            await message.reply(f'Contrail set to {cosmetic.id}.')
            print(f"[PartyBot] [{time()}] Set contrail to: {cosmetic.id}.")
            await client.user.party.me.set_contrail(asset=cosmetic.id)

        except BenBotAsync.exceptions.NotFound:
            await message.reply(f"Couldn't find a contrail with the name: {content}.")
            print(f"[PartyBot] [{time()}] Couldn't find an contrail with the name: {content}.")

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
        await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=args[3])

        await message.reply(f'Banner set to: {args[1]}, {args[2]}, {args[3]}.')
        print(f"[PartyBot] [{time()}] Banner set to: {args[1]}, {args[2]}, {args[3]}.")

    elif "cid_" in args[0].lower():
        if 'banner' not in args[0].lower():
            await client.user.party.me.set_outfit(
                asset=args[0]
            )
        else:
            await client.user.party.me.set_outfit(
                asset=args[0],
                variants=client.user.party.me.create_variants(profile_banner='ProfileBanner')
            )

        await message.reply(f'Skin set to {args[0]}')
        print(f'[PartyBot] [{time()}] Skin set to {args[0]}')

    elif "vtid_" in args[0].lower():
        vtid = await set_vtid(args[0])
        if vtid[1] == 'Particle':
            variants = client.user.party.me.create_variants(particle_config='Particle', particle=1)
        else:
            variants = client.user.party.me.create_variants(**{vtid[1].lower(): int(vtid[2])})

        await client.user.party.me.set_outfit(asset=vtid[0], variants=variants)
        await message.reply(f'Variants set to {args[0]}.\n'
                            '(Warning: This feature is not supported, please use !variants)')

    elif "!variants" in args[0].lower():
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
        await client.user.party.me.set_emoji(
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
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=content,
                    backendType="AthenaPickaxe"
                )

                await client.user.party.me.set_pickaxe(asset=cosmetic.id)
                await client.user.party.me.clear_emote()
                await client.user.party.me.set_emote(asset='EID_IceKing')
                await message.reply(f'Pickaxe set to {content} & Point it Out played.')
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f"Couldn't find a pickaxe with the name: {content}")

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
        await client.user.party.me.set_battlepass_info(
            has_purchased=True,
            level=args[1],
        )

        await message.reply(f'Set battle pass tier to {args[1]}.')

    elif "!level" in args[0].lower():
        await client.user.party.me.set_banner(
            icon=client.user.party.me.banner[0],
            color=client.user.party.me.banner[1],
            season_level=args[1]
        )

        await message.reply(f'Set level to {args[1]}.')

    elif "!echo" in args[0].lower():
        await client.user.party.send(content)
        await message.reply('Sent message to party chat.')

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
                print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                                  "Failed to kick member as I don't have the required permissions."))

    elif "!promote" in args[0].lower():
        if len(args) == 1:
            user = await client.fetch_profile(message.author.display_name)
            member = await client.user.party.members.get(user.id)
        else:
            user = await client.fetch_profile(content)
            member = client.user.party.members.get(user.id)

        if member is None:
            await message.reply("Couldn't find that user, are you sure they're in the party?")
        else:
            try:
                await member.promote()
                await message.reply(f"Promoted user: {member.display_name}.")
                print(f"[PartyBot] [{time()}] Promoted user: {member.display_name}")
            except fortnitepy.Forbidden:
                await message.reply(f"Couldn't promote {member.display_name}, as I'm not party leader.")
                print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                                  "Failed to kick member as I don't have the required permissions."))

    elif "playlist_" in args[0].lower():
        try:
            await client.user.party.set_playlist(playlist=args[0])
            await message.reply(f'Gamemode set to {args[0]}')
        except fortnitepy.Forbidden:
            await message.reply(f"Couldn't set gamemode to {args[1]}, as I'm not party leader.")
            print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                              "Failed to set gamemode as I don't have the required permissions."))

    elif "!platform" in args[0].lower():
        await message.reply(f'Setting platform to {args[0]}')
        party_id = client.user.party.id
        await client.user.party.me.leave()
        client.platform = fortnitepy.Platform(args[1])
        await message.reply(f'Platform set to {str(client.platform)}.')
        try:
            await client.join_to_party(party_id)
        except fortnitepy.Forbidden:
            await message.reply('Failed to join back as party is set to private.')

    elif "!id" in args[0].lower():
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
            print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                              "Failed to set party privacy as I don't have the required permissions."))

    elif "!copy" in args[0].lower():
        if len(args) == 1:
            member = client.user.party.members.get(message.author.id)
        else:
            user = await client.fetch_profile(content)
            member = client.user.party.members.get(user.id)

        await client.user.party.me.edit(
            functools.partial(
                fortnitepy.ClientPartyMember.set_outfit,
                asset=member.outfit,
                variants=member.outfit_variants
            ),
            functools.partial(
                fortnitepy.ClientPartyMember.set_backpack,
                asset=member.backpack,
                variants=member.backpack_variants
            ),
            functools.partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                asset=member.pickaxe,
                variants=member.pickaxe_variants
            ),
            functools.partial(
                fortnitepy.ClientPartyMember.set_banner,
                icon=member.banner[0],
                color=member.banner[1],
                season_level=member.banner[2]
            ),
            functools.partial(
                fortnitepy.ClientPartyMember.set_battlepass_info,
                has_purchased=True,
                level=member.battlepass_info[1]
            )
        )

        await client.user.party.me.set_emote(asset=member.emote)
        await message.reply(f'Copied the loadout of {member.display_name}.')

    elif "!hologram" in args[0].lower():
        await client.user.party.me.set_outfit(
            asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
        )

        await message.reply('Skin set to Star Wars Hologram!')

    elif "!gift" in args[0].lower():
        await client.user.party.me.clear_emote()

        await client.user.party.me.set_emote(
            asset='EID_NeverGonna'
        )

        await message.reply('What did you think would happen?')

    elif "!matchmakingcode" in args[0].lower():
        await client.user.party.set_custom_key(
            key=content
        )

        await message.reply(f'Custom matchmaking code set to: {content}')

    elif "!ninja" in args[0].lower():
        await client.user.party.me.set_outfit(
            asset='CID_605_Athena_Commando_M_TourBus'
        )

        await message.reply('Skin set to Ninja!')

    elif "!ponpon" in args[0].lower():
        await client.user.party.me.set_emote(
            asset='EID_TourBus'
        )

        await message.reply('Emote set to Ninja Style!')

    elif "!enlightened" in args[0].lower():
        await client.user.party.me.set_outfit(
            asset=args[1],
            variants=client.user.party.me.create_variants(progressive=4),
            enlightenment=(args[2], args[3])
        )

        await message.reply(f'Skin set to {args[1]} at level {args[3]} (for Season 1{args[2]}).')

    elif "!rareskins" in args[0].lower():
        await message.reply('Showing all rare skins now.')

        await client.user.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=client.user.party.me.create_variants(clothing_color=1)
        )

        await message.reply('Skin set to Purple Skull Trooper!')
        await asyncio.sleep(2)

        await client.user.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=client.user.party.me.create_variants(material=3)
        )

        await message.reply('Skin set to Pink Ghoul Trooper!')
        await asyncio.sleep(2)

        for skin in ('CID_028_Athena_Commando_F', 'CID_017_Athena_Commando_M', 'CID_022_Athena_Commando_F'):
            await client.user.party.me.set_outfit(
                asset=skin
            )

            await message.reply(f'Skin set to {skin}!')
            await asyncio.sleep(2)

    elif "!goldenpeely" in args[0].lower():
        await client.user.party.me.set_outfit(
            asset='CID_701_Athena_Commando_M_BananaAgent',
            variants=client.user.party.me.create_variants(progressive=4),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin set to Golden Peely.')

    elif "!random" in args[0].lower():
        outfits = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaCharacter"
        )

        skin = random.choice(outfits).id

        await client.user.party.me.set_outfit(
            asset=skin,
            variants=client.user.party.me.create_variants(profile_banner='ProfileBanner')
        )

        await message.reply(f'Skin randomly set to {skin}.')

    elif "!nobackpack" in args[0].lower():
        await client.user.party.me.clear_backpack()
        await message.reply('Removed backpack.')

    elif "!nopet" in args[0].lower():
        await client.user.party.me.clear_pet()
        await message.reply('Removed pet.')

    elif "!nocontrail" in args[0].lower():
        await client.user.party.me.clear_contrail()
        await message.reply('Removed contrail.')

    elif "!match" in args[0].lower():
        async def _set_prop(schema_key: str, new_value: str) -> None:
            prop = {schema_key: client.user.party.me.meta.set_prop(schema_key, new_value)}

            await client.user.party.me.patch(updated=prop)

        await _set_prop('Location_s', 'InGame')
        await _set_prop('NumAthenaPlayersLeft_U', args[1] if len(args) >= 2 else 0)
        await _set_prop('HasPreloadedAthena_b', True)
        await _set_prop('SpectateAPartyMemberAvailable_b', 'true')

        match_time = str(fortnitepy.Client.to_iso(
            datetime.datetime.utcnow() - datetime.timedelta(minutes=int(args[2]) if len(args) >= 3 else 0)
        ))[slice(23)]

        await _set_prop('UtcTimeStartedMatchAthena_s', f'{str(match_time)}Z')

        await message.reply(f'Set state to in-game in a match with {args[1] if len(args) >= 2 else 0} players.'
                            '\nUse the command: !lobby to revert back to normal.')

    elif "!lobby" in args[0].lower():
        async def _set_prop(schema_key: str, new_value: str) -> None:
            prop = {schema_key: client.user.party.me.meta.set_prop(schema_key, new_value)}

            await client.user.party.me.patch(updated=prop)

        await _set_prop('Location_s', 'PreLobby')
        await _set_prop('NumAthenaPlayersLeft_U', '0')
        await _set_prop('HasPreloadedAthena_b', False)
        await _set_prop('SpectateAPartyMemberAvailable_b', 'false')
        await _set_prop('UtcTimeStartedMatchAthena_s', '0001-01-01T00:00:00.000Z')

        await message.reply('Set state to the pre-game lobby.')

    elif "!join" in args[0].lower():
        if len(args) == 1:
            friend = client.get_friend(message.author.id)
        else:
            user = await client.fetch_profile(content)

            if user is not None:
                friend = client.get_friend(user.id)
            else:
                friend = None
                await message.reply(f'Failed to find user with the name: {content}.')

        if isinstance(friend, fortnitepy.Friend):
            try:
                await friend.join_party()
                await message.reply(f'Joined the party of {friend.display_name}.')
            except fortnitepy.Forbidden:
                await message.reply('Failed to join party since it is private.')
            except fortnitepy.PartyError:
                await message.reply('Party not found, are you sure Fortnite is open?')
        else:
            await message.reply('Cannot join party as the friend is not found.')

if (data['email'] and data['password']) and (data['email'] != 'email@email.com' and data['password'] != 'password1'):
    try:
        client.run()
    except fortnitepy.AuthException as e:
        print(crayons.red(f"[PartyBot] [{time()}] [ERROR] {e}"))
else:
    print(crayons.red(f"[PartyBot] [{time()}] [ERROR] Failed to login as no (or default) account details provided."))
