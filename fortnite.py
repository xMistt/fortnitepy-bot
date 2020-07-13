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

Software: PartyBot (fortnitepy-bot)

License: Apache 2.0
"""

try:
    # System imports.
    from typing import Tuple, Any, Union

    import asyncio
    import sys
    import datetime
    import json
    import functools
    import os
    import random as py_random
    import logging
    import uuid
    import json

    # Third party imports.
    from fortnitepy.ext import commands

    import crayons
    import fortnitepy
    import BenBotAsync
    import aiohttp
    import pypresence
    import psutil

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

if sys.platform == 'win32':
    asyncio.set_event_loop(asyncio.ProactorEventLoop())


def time() -> str:
    return datetime.datetime.now().strftime('%H:%M:%S')


def get_device_auth_details() -> dict:
    if os.path.isfile('device_auths.json'):
        with open('device_auths.json', 'r') as fp:
            return json.load(fp)
    else:
        with open('device_auths.json', 'w+') as fp:
            json.dump({}, fp, sort_keys=False, indent=4)

    return {}


def store_device_auth_details(email: str, details: dict) -> None:
    existing = get_device_auth_details()
    existing[email] = details

    with open('device_auths.json', 'w') as fp:
        json.dump(existing, fp, sort_keys=False, indent=4)


def check_if_process_running(name: str) -> bool:
    for process in psutil.process_iter():
        try:
            if name.lower() in process.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False


async def set_vtid(variant_token: str) -> Tuple[str, str, int]:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='https://benbotfn.tk/api/v1/assetProperties',
            params={
                'path': 'FortniteGame/Content/Athena/'
                        f'Items/CosmeticVariantTokens/{variant_token}.uasset'
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

    return skin_cid, variant_type if variant_type != 'ClothingColor' else 'clothing_color', variant_int


async def get_playlist(display_name: str) -> str:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='http://scuffedapi.xyz/api/playlists/search',
            params={
                'displayName': display_name
            })

        response = await request.json()

    return response['id'] if 'error' not in response else None


async def set_and_update_member_prop(schema_key: str, new_value: Any) -> None:
    prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}

    await client.party.me.patch(updated=prop)


async def set_and_update_party_prop(schema_key: str, new_value: Any) -> None:
    prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}

    await client.party.patch(updated=prop)


async def start_discord_rich_presence() -> None:
    rpc = pypresence.AioPresence(
        client_id='717610574837710919',
        loop=client.loop
    )

    try:
        await rpc.connect()
    except Exception as discord_error:
        print(f'There was an error: {discord_error}.')

    start_time = datetime.datetime.now().timestamp()

    while True:
        try:
            outfit = (await BenBotAsync.get_cosmetic_from_id(
                cosmetic_id=client.party.me.outfit
            )).name

        except BenBotAsync.exceptions.NotFound:
            outfit = client.party.me.outfit

        await rpc.update(
            details=f"Logged in as {client.user.display_name}.",
            state=f"{client.party.leader.display_name}'s party.",
            large_image="skull_trooper",
            large_text="discord.gg/fnpy",
            small_image="outfit",
            small_text=outfit,
            start=int(start_time),
            party_id=client.party.id,
            party_size=[client.party.member_count, 16],
            join=uuid.uuid4().hex
        )

        await asyncio.sleep(20)


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
client = commands.Bot(
    command_prefix='!',
    auth=fortnitepy.AdvancedAuth(
        email=data['email'],
        password=data['password'],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auth_details
    ),
    status=data['status'],
    platform=fortnitepy.Platform(data['platform']),
    avatar=fortnitepy.Avatar(
        asset="cid_028_ff2b06cf446376144ba408d3482f5c982bf2584cf0f508ee3e4ba4a0fd461a38",
        background_colors=fortnitepy.KairosBackgroundColorPreset.PINK.value
    )
)


@client.event
async def event_device_auth_generate(details: dict, email: str) -> None:
    store_device_auth_details(email, details)


@client.event
async def event_ready() -> None:
    print(crayons.green(f'[PartyBot] [{time()}] Client ready as {client.user.display_name}.'))

    discord_exists = await client.loop.run_in_executor(None, check_if_process_running, 'Discord')

    if discord_exists:
        client.loop.create_task(start_discord_rich_presence())

    for pending in list(client.pending_friends.values()):
        if type(pending) == fortnitepy.IncomingPendingFriend:
            try:
                epic_friend = await pending.accept() if data["friend_accept"] else await pending.decline()
                if isinstance(epic_friend, fortnitepy.Friend):
                    print(f"[PartyBot] [{time()}] Accepted friend request from: {epic_friend.display_name}.")
                else:
                    print(f"[PartyBot] [{time()}] Declined friend request from: {pending.display_name}.")
            except fortnitepy.HTTPException as epic_error:
                if epic_error.message_code != 'errors.com.epicgames.common.throttled':
                    raise

                await asyncio.sleep(int(epic_error.message_vars[0] + 1))
                await pending.accept() if data["friend_accept"] else await pending.decline()


@client.event
async def event_party_invite(invite: fortnitepy.ReceivedPartyInvitation) -> None:
    await invite.accept()
    print(f'[PartyBot] [{time()}] Accepted party invite from {invite.sender.display_name}.')


@client.event
async def event_friend_request(request: fortnitepy.IncomingPendingFriend) -> None:
    print(f"[PartyBot] [{time()}] Received friend request from: {request.display_name}.")

    if data['friend_accept']:
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
    print(crayons.magenta(f'[PartyBot] [{time()}] {message.author.display_name}: {message.content}'))


@client.event
async def event_party_message(message: fortnitepy.FriendMessage) -> None:
    print(crayons.green(f'[PartyBot] [{time()}] {message.author.display_name}: {message.content}'))


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client using the outfits name.",
    help="Sets the outfit of the client using the outfits name.\n"
    "Example: !skin Nog Ops"
)
async def skin(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaCharacter"
        )

        await ctx.send(f'Skin set to {cosmetic.id}.')
        print(f"[PartyBot] [{time()}] Set skin to: {cosmetic.id}.")
        await client.party.me.set_outfit(asset=cosmetic.id)

    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a skin with the name: {content}.")
        print(f"[PartyBot] [{time()}] Failed to find a skin with the name: {content}.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the backpack of the client using the backpacks name.",
    help="Sets the backpack of the client using the backpacks name.\n"
    "Example: !backpack Black Shield"
)
async def backpack(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaBackpack"
        )

        await ctx.send(f'Backpack set to {cosmetic.id}.')
        print(f"[PartyBot] [{time()}] Set backpack to: {cosmetic.id}.")
        await client.party.me.set_backpack(asset=cosmetic.id)

    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a backpack with the name: {content}.")
        print(f"[PartyBot] [{time()}] Failed to find a backpack with the name: {content}.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the emote of the client using the emotes name.",
    help="Sets the emote of the client using the emotes name.\n"
    "Example: !emote Windmill Floss"
)
async def emote(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaDance"
        )

        await ctx.send(f'Emote set to {cosmetic.id}.')
        print(f"[PartyBot] [{time()}] Set emote to: {cosmetic.id}.")
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset=cosmetic.id)

    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find an emote with the name: {content}.")
        print(f"[PartyBot] [{time()}] Failed to find an emote with the name: {content}.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the pickaxe of the client using the pickaxe name.",
    help="Sets the pickaxe of the client using the pickaxe name.\n"
    "Example: !pickaxe Raider's Revenge"
)
async def pickaxe(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaPickaxe"
        )

        await ctx.send(f'Pickaxe set to {cosmetic.id}.')
        print(f"[PartyBot] [{time()}] Set pickaxe to: {cosmetic.id}.")
        await client.party.me.set_pickaxe(asset=cosmetic.id)

    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a pickaxe with the name: {content}.")
        print(f"[PartyBot] [{time()}] Failed to find a pickaxe with the name: {content}.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the pet (backpack) of the client using the pets name.",
    help="Sets the pet (backpack) of the client using the pets name.\n"
    "Example: !pet Bonesy"
)
async def pet(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaPetCarrier"
        )

        await ctx.send(f'Pet set to {cosmetic.id}.')
        print(f"[PartyBot] [{time()}] Set pet to: {cosmetic.id}.")
        await client.party.me.set_pet(asset=cosmetic.id)

    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a pet with the name: {content}.")
        print(f"[PartyBot] [{time()}] Failed to find a pet with the name: {content}.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the emoji of the client using the emojis name.",
    help="Sets the emoji of the client using the emojis name.\n"
    "Example: !emoji Snowball"
)
async def emoji(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaEmoji"
        )

        await ctx.send(f'Emoji set to {cosmetic.id}.')
        print(f"[PartyBot] [{time()}] Set emoji to: {cosmetic.id}.")
        await client.party.me.set_emoji(asset=cosmetic.id)

    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find an emoji with the name: {content}.")
        print(f"[PartyBot] [{time()}] Failed to find an emoji with the name: {content}.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the contrail of the client using the contrail name.",
    help="Sets the contrail of the client using the contrail name.\n"
    "Example: !contrail Holly And Divey"
)
async def contrail(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaSkyDiveContrail"
        )

        await ctx.send(f'Contrail set to {cosmetic.id}.')
        print(f"[PartyBot] [{time()}] Set contrail to: {cosmetic.id}.")
        await client.party.me.set_contrail(asset=cosmetic.id)

    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a contrail with the name: {content}.")
        print(f"[PartyBot] [{time()}] Failed to find an contrail with the name: {content}.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to Purple Skull Trooper.",
    help="Sets the outfit of the client to Purple Skull Trooper.\n"
    "Example: !purpleskull"
)
async def purpleskull(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        clothing_color=1
    )

    await client.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants=skin_variants
    )

    await ctx.send('Skin set to Purple Skull Trooper!')
    print(f"[PartyBot] [{time()}] Skin set to Purple Skull Trooper.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to Pink Ghoul Trooper.",
    help="Sets the outfit of the client to Pink Ghoul Trooper.\n"
    "Example: !pinkghoul"
)
async def pinkghoul(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        material=3
    )

    await client.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=skin_variants
    )

    await ctx.send('Skin set to Pink Ghoul Trooper!')
    print(f"[PartyBot] [{time()}] Skin set to Pink Ghoul Trooper.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the backpack of the client to Purple Ghost Portal.",
    help="Sets the backpack of the client to Purple Ghost Portal.\n"
    "Example: !purpleportal"
)
async def purpleportal(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        item='AthenaBackpack',
        particle_config='Particle',
        particle=1
    )

    await client.party.me.set_backpack(
        asset='BID_105_GhostPortal',
        variants=skin_variants
    )

    await ctx.send('Backpack set to Purple Ghost Portal!')
    print(f"[PartyBot] [{time()}] Backpack set to Purple Ghost Portal.")


@commands.dm_only()
@client.command(
    description="[Party] Sets the banner of the client.",
    help="Sets the banner of the client.\n"
    "Example: !banner BRSeason01 defaultcolor15 100"
)
async def banner(ctx: fortnitepy.ext.commands.Context, icon: str, colour: str, banner_level: int) -> None:
    await client.party.me.set_banner(icon=icon, color=colour, season_level=banner_level)

    await ctx.send(f'Banner set to: {icon}, {colour}, {banner_level}.')
    print(f"[PartyBot] [{time()}] Banner set to: {icon}, {colour}, {banner_level}.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client using CID.",
    help="Sets the outfit of the client using CID.\n"
    "Example: !cid CID_047_Athena_Commando_F_HolidayReindeer"
)
async def cid(ctx: fortnitepy.ext.commands.Context, character_id: str) -> None:
    await client.party.me.set_outfit(
        asset=character_id,
        variants=client.party.me.create_variants(profile_banner='ProfileBanner')
    )

    await ctx.send(f'Skin set to {character_id}')
    print(f'[PartyBot] [{time()}] Skin set to {character_id}')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Creates the variants list by the variants you set using VTID.",
    help="Creates the variants list by the variants you set using VTID.\n"
    "Example: !vtid VTID_052_Skull_Trooper_RedFlames"
)
async def vtid(ctx: fortnitepy.ext.commands.Context, variant_token: str) -> None:
    variant_id = await set_vtid(variant_token)

    if variant_id[1].lower() == 'particle':
        skin_variants = client.party.me.create_variants(particle_config='Particle', particle=1)
    else:
        skin_variants = client.party.me.create_variants(**{vtid[1].lower(): int(vtid[2])})

    await client.party.me.set_outfit(asset=vtid[0], variants=skin_variants)
    print(f'[PartyBot] [{time()}] Set variants of {vtid[0]} to {vtid[1]} {vtid[2]}.')
    await ctx.send(f'Variants set to {variant_token}.\n'
                   '(Warning: This feature is not supported, please use !variants)')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Creates the variants list by the variants you set.",
    help="Creates the variants list by the variants you set.\n"
    "Example: !variants CID_030_Athena_Commando_M_Halloween clothing_color 1"
)
async def variants(ctx: fortnitepy.ext.commands.Context, cosmetic_id: str, variant_type: str, variant_int: str) -> None:
    if 'cid' in cosmetic_id.lower() and 'jersey_color' not in variant_type.lower():
        skin_variants = client.party.me.create_variants(
            **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
        )

        await client.party.me.set_outfit(
            asset=cosmetic_id,
            variants=skin_variants
        )

    elif 'cid' in cosmetic_id.lower() and 'jersey_color' in variant_type.lower():
        cosmetic_variants = client.party.me.create_variants(
            pattern=0,
            numeric=69,
            **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
        )

        await client.party.me.set_outfit(
            asset=cosmetic_id,
            variants=cosmetic_variants
        )

    elif 'bid' in cosmetic_id.lower():
        cosmetic_variants = client.party.me.create_variants(
            item='AthenaBackpack',
            **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
        )

        await client.party.me.set_backpack(
            asset=cosmetic_id,
            variants=cosmetic_variants
        )
    elif 'pickaxe_id' in cosmetic_id.lower():
        cosmetic_variants = client.party.me.create_variants(
            item='AthenaPickaxe',
            **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
        )

        await client.party.me.set_pickaxe(
            asset=cosmetic_id,
            variants=cosmetic_variants
        )

    await ctx.send(f'Set variants of {cosmetic_id} to {variant_type} {variant_int}.')
    print(f'[PartyBot] [{time()}] Set variants of {cosmetic_id} to {variant_type} {variant_int}.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to Checkered Renegade.",
    help="Sets the outfit of the client to Checkered Renegade.\n"
    "Example: !checkeredrenegade"
)
async def checkeredrenegade(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        material=2
    )

    await client.party.me.set_outfit(
        asset='CID_028_Athena_Commando_F',
        variants=skin_variants
    )

    await ctx.send('Skin set to Checkered Renegade!')
    print(f'[PartyBot] [{time()}] Skin set to Checkered Renegade.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to Minty Elf.",
    help="Sets the outfit of the client to Minty Elf.\n"
    "Example: !mintyelf"
)
async def mintyelf(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        material=2
    )

    await client.party.me.set_outfit(
        asset='CID_051_Athena_Commando_M_HolidayElf',
        variants=skin_variants
    )

    await ctx.send('Skin set to Minty Elf!')
    print(f'[PartyBot] [{time()}] Skin set to Minty Elf.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the emote of the client using EID.",
    help="Sets the emote of the client using EID.\n"
    "Example: !eid EID_Floss"
)
async def eid(ctx: fortnitepy.ext.commands.Context, emote_id: str) -> None:
    await client.party.me.clear_emote()
    await client.party.me.set_emote(
        asset=emote_id
    )

    await ctx.send(f'Emote set to {emote_id}!')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Clears/stops the emote currently playing.",
    help="Clears/stops the emote currently playing.\n"
    "Example: !stop"
)
async def stop(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.clear_emote()
    await ctx.send('Stopped emoting.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the backpack of the client using BID.",
    help="Sets the backpack of the client using BID.\n"
    "Example: !bid BID_023_Pinkbear"
)
async def bid(ctx: fortnitepy.ext.commands.Context, backpack_id: str) -> None:
    await client.party.me.set_backpack(
        asset=backpack_id
    )

    await ctx.send(f'Backbling set to {backpack_id}!')


@commands.dm_only()
@client.command(
    aliases=['legacypickaxe'],
    description="[Cosmetic] Sets the pickaxe of the client using PICKAXE_ID",
    help="Sets the pickaxe of the client using PICKAXE_ID\n"
    "Example: !pickaxe_id Pickaxe_ID_073_Balloon"
)
async def pickaxe_id(ctx: fortnitepy.ext.commands.Context, pickaxe_id_: str) -> None:
    await client.party.me.set_pickaxe(
        asset=pickaxe_id_
    )

    await ctx.send(f'Pickaxe set to {pickaxe_id_}')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the pet of the client using PetCarrier_.",
    help="Sets the pet of the client using PetCarrier_.\n"
    "Example: !pet_carrier PetCarrier_002_Chameleon"
)
async def pet_carrier(ctx: fortnitepy.ext.commands.Context, pet_carrier_id: str) -> None:
    await client.party.me.set_pet(
        asset=pet_carrier_id
    )

    await ctx.send(f'Pet set to {pet_carrier_id}!')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the emoji of the client using Emoji_.",
    help="Sets the emoji of the client using Emoji_.\n"
    "Example: !emoji_id Emoji_PeaceSign"
)
async def emoji_id(ctx: fortnitepy.ext.commands.Context, emoji_: str) -> None:
    await client.party.me.clear_emote()
    await client.party.me.set_emoji(
        asset=emoji_
    )

    await ctx.send(f'Emoji set to {emoji_}!')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the contrail of the client using Trails_.",
    help="Sets the contrail of the client using Trails_.\n"
    "Example: !trails Trails_ID_075_Celestial"
)
async def trails(ctx: fortnitepy.ext.commands.Context, trails_: str) -> None:
    await client.party.me.set_contrail(
        asset=trails_
    )

    await ctx.send(f'Contrail set to {trails}!')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets pickaxe using PICKAXE_ID or display name & does 'Point it Out'. If no pickaxe is "
                "specified, only the emote will be played.",
    help="Sets pickaxe using PICKAXE_ID or display name & does 'Point it Out'. If no pickaxe is "
         "specified, only the emote will be played.\n"
    "Example: !point Pickaxe_ID_029_Assassin"
)
async def point(ctx: fortnitepy.ext.commands.Context, *, content: Union[str, None] = None) -> None:
    if content is None:
        await client.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Point it Out played.')
    elif 'pickaxe_id' in content.lower():
        await client.party.me.set_pickaxe(asset=content)
        await client.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Pickaxe set to {content} & Point it Out played.')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )

            await client.party.me.set_pickaxe(asset=cosmetic.id)
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset='EID_IceKing')
            await ctx.send(f'Pickaxe set to {content} & Point it Out played.')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f"Failed to find a pickaxe with the name: {content}")


@commands.dm_only()
@client.command(
    description="[Party] Sets the readiness of the client to ready.",
    help="Sets the readiness of the client to ready.\n"
    "Example: !ready"
)
async def ready(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send('Ready!')


@commands.dm_only()
@client.command(
    aliases=['sitin'],
    description="[Party] Sets the readiness of the client to unready.",
    help="Sets the readiness of the client to unready.\n"
    "Example: !unready"
)
async def unready(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Unready!')


@commands.dm_only()
@client.command(
    description="[Party] Sets the readiness of the client to SittingOut.",
    help="Sets the readiness of the client to SittingOut.\n"
    "Example: !sitout"
)
async def sitout(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await ctx.send('Sitting Out!')


@commands.dm_only()
@client.command(
    description="[Party] Sets the battlepass info of the client.",
    help="Sets the battlepass info of the client.\n"
    "Example: !bp 100"
)
async def bp(ctx: fortnitepy.ext.commands.Context, tier: int) -> None:
    await client.party.me.set_battlepass_info(
        has_purchased=True,
        level=tier,
    )

    await ctx.send(f'Set battle pass tier to {tier}.')


@commands.dm_only()
@client.command(
    description="[Party] Sets the level of the client.",
    help="Sets the level of the client.\n"
    "Example: !level 999"
)
async def level(ctx: fortnitepy.ext.commands.Context, banner_level: int) -> None:
    await client.party.me.set_banner(
        season_level=banner_level
    )

    await ctx.send(f'Set level to {level}.')


@commands.dm_only()
@client.command(
    description="[Party] Sends message to party chat with the given content.",
    help="Sends message to party chat with the given content.\n"
    "Example: !echo i cant fix the fucking public lobby bots"
)
async def echo(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    await client.party.send(content)
    await ctx.send('Sent message to party chat.')


@commands.dm_only()
@client.command(
    description="[Client] Sends and sets the status.",
    help="Sends and sets the status.\n"
    "Example: !status Presence Unknown"
)
async def status(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    await client.set_status(content)

    await ctx.send(f'Status set to {content}')
    print(f'[PartyBot] [{time()}] Status set to {content}.')


@commands.dm_only()
@client.command(
    description="[Party] Leaves the current party.",
    help="Leaves the current party.\n"
    "Example: !leave"
)
async def leave(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote('EID_Wave')
    await asyncio.sleep(2)
    await client.party.me.leave()
    await ctx.send('Bye!')

    print(f'[PartyBot] [{time()}] Left the party as I was requested.')


@commands.dm_only()
@client.command(
    description="[Party] Kicks the inputted user.",
    help="Kicks the inputted user.\n"
    "Example: !kick Cxnyaa"
)
async def kick(ctx: fortnitepy.ext.commands.Context, *, epic_username: str) -> None:
    user = await client.fetch_profile(epic_username)
    member = client.party.members.get(user.id)

    if member is None:
        await ctx.send("Failed to find that user, are you sure they're in the party?")
    else:
        try:
            await member.kick()
            await ctx.send(f"Kicked user: {member.display_name}.")
            print(f"[PartyBot] [{time()}] Kicked user: {member.display_name}")
        except fortnitepy.errors.Forbidden:
            await ctx.send(f"Failed to kick {member.display_name}, as I'm not party leader.")
            print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                              "Failed to kick member as I don't have the required permissions."))


@commands.dm_only()
@client.command(
    aliases=['unhide'],
    description="[Party] Promotes the defined user to party leader. If friend is left blank, "
                "the message author will be used.",
    help="Promotes the defined user to party leader. If friend is left blank, the message author will be used.\n"
    "Example: !promote Terbau"
)
async def promote(ctx: fortnitepy.ext.commands.Context, *, epic_username: Union[str, None] = None) -> None:
    if epic_username is None:
        user = await client.fetch_profile(ctx.author.display_name)
        member = client.party.members.get(user.id)
    else:
        user = await client.fetch_profile(epic_username)
        member = client.party.members.get(user.id)

    if member is None:
        await ctx.send("Failed to find that user, are you sure they're in the party?")
    else:
        try:
            await member.promote()
            await ctx.send(f"Promoted user: {member.display_name}.")
            print(f"[PartyBot] [{time()}] Promoted user: {member.display_name}")
        except fortnitepy.errors.Forbidden:
            await ctx.send(f"Failed topromote {member.display_name}, as I'm not party leader.")
            print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                              "Failed to kick member as I don't have the required permissions."))


@commands.dm_only()
@client.command(
    description="[Party] Sets the lobbies selected playlist.",
    help="Sets the lobbies selected playlist.\n"
    "Example: !playlist_id Playlist_Tank_Solo"
)
async def playlist_id(ctx: fortnitepy.ext.commands.Context, playlist_: str) -> None:
    try:
        await client.party.set_playlist(playlist=playlist_)
        await ctx.send(f'Gamemode set to {playlist_}')
    except fortnitepy.errors.Forbidden:
        await ctx.send(f"Failed to set gamemode to {playlist_}, as I'm not party leader.")
        print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                          "Failed to set gamemode as I don't have the required permissions."))


@commands.dm_only()
@client.command(
    description="[Party] Sets the parties current privacy.",
    help="Sets the parties current privacy.\n"
    "Example: !privacy private"
)
async def privacy(ctx: fortnitepy.ext.commands.Context, privacy_type: str) -> None:
    try:
        if privacy_type.lower() == 'public':
            await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
        elif privacy_type.lower() == 'private':
            await client.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
        elif privacy_type.lower() == 'friends':
            await client.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS)
        elif privacy_type.lower() == 'friends_allow_friends_of_friends':
            await client.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS_ALLOW_FRIENDS_OF_FRIENDS)
        elif privacy_type.lower() == 'private_allow_friends_of_friends':
            await client.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE_ALLOW_FRIENDS_OF_FRIENDS)

        await ctx.send(f'Party privacy set to {client.party.privacy}.')
        print(f'[PartyBot] [{time()}] Party privacy set to {client.party.privacy}.')

    except fortnitepy.errors.Forbidden:
        await ctx.send(f"Failed to set party privacy to {privacy_type}, as I'm not party leader.")
        print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                          "Failed to set party privacy as I don't have the required permissions."))


@commands.dm_only()
@client.command(
    description="[Cosmetic] Copies the cosmetic loadout of the defined user. If user is left blank, "
                "the message author will be used.",
    help="Copies the cosmetic loadout of the defined user. If user is left blank, the message author will be used.\n"
    "Example: !copy Terbau"
)
async def copy(ctx: fortnitepy.ext.commands.Context, *, epic_username: Union[str, None] = None) -> None:
    if epic_username is None:
        member = client.party.members.get(ctx.author.id)
    else:
        user = await client.fetch_profile(epic_username)
        member = client.party.members.get(user.id)

    await client.party.me.edit(
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

    await client.party.me.set_emote(asset=member.emote)
    await ctx.send(f'Copied the loadout of {member.display_name}.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Shortcut for equipping the skin CID_VIP_Athena_Commando_M_GalileoGondola_SG.",
    help="Shortcut for equipping the skin CID_VIP_Athena_Commando_M_GalileoGondola_SG.\n"
    "Example: !hologram"
)
async def hologram(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )

    await ctx.send('Skin set to Star Wars Hologram!')
    print(f'[PartyBot] [{time()}] Skin set to Star Wars Hologram.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Shortcut for equipping the skin CID_VIP_Athena_Commando_M_GalileoGondola_SG.",
    help="Shortcut for equipping the skin CID_VIP_Athena_Commando_M_GalileoGondola_SG.\n"
    "Example: !gift is a joke command."
)
async def gift(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.clear_emote()

    await client.party.me.set_emote(
        asset='EID_NeverGonna'
    )

    await ctx.send('What did you think would happen?')


@commands.dm_only()
@client.command(
    description="[Party] Sets the parties custom matchmaking code.",
    help="Sets the parties custom matchmaking code.\n"
    "Example: !skin Nog Ops"
)
async def matchmakingcode(ctx: fortnitepy.ext.commands.Context, *, custom_matchmaking_key: str) -> None:
    await client.party.set_custom_key(
        key=custom_matchmaking_key
    )

    await ctx.send(f'Custom matchmaking code set to: {custom_matchmaking_key}')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Shortcut for equipping the emote EID_TourBus.",
    help="Shortcut for equipping the emote EID_TourBus.\n"
    "Example: !ponpon"
)
async def ponpon(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_TourBus'
    )

    await ctx.send('Emote set to Ninja Style!')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the enlightened value of a skin "
                "(used for skins such as glitched Scratch or Golden Peely).",
    help="Sets the enlightened value of a skin.\n"
    "Example: !enlightened CID_701_Athena_Commando_M_BananaAgent 2 350"
)
async def enlightened(ctx: fortnitepy.ext.commands.Context, cosmetic_id: str, br_season: int, skin_level: int) -> None:
    variant_types = {
        1: client.party.me.create_variants(progressive=4),
        2: client.party.me.create_variants(progressive=4),
        3: client.party.me.create_variants(material=2)
    }

    if 'cid' in cosmetic_id.lower():
        await client.party.me.set_outfit(
            asset=cosmetic_id,
            variants=variant_types[br_season] if br_season in variant_types else variant_types[2],
            enlightenment=(br_season, level)
        )

        await ctx.send(f'Skin set to {character_id} at level {skin_level} (for Season 1{br_season}).')
    elif 'bid' in cosmetic_id.lower():
        await client.party.me.set_backpack(
            asset=cosmetic_id,
            variants=client.party.me.create_variants(progressive=2),
            enlightenment=(br_season, level)
        )
        await ctx.send(f'Backpack set to {character_id} at level {skin_level} (for Season 1{br_season}).')

    print(f'[PartyBot] [{time()}] Enlightenment for {cosmetic_id} set to level {skin_level} (for Season 1{br_season}).')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Shortcut for equipping the skin CID_605_Athena_Commando_M_TourBus.",
    help="Shortcut for equipping the skin CID_605_Athena_Commando_M_TourBus.\n"
    "Example: !ninja"
)
async def ninja(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_605_Athena_Commando_M_TourBus'
    )

    await ctx.send('Skin set to Ninja!')
    print(f'[PartyBot] [{time()}] Skin set to Ninja.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Equips all very rare skins.",
    help="Equips all very rare skins.\n"
    "Example: !rareskins"
)
async def rareskins(ctx: fortnitepy.ext.commands.Context) -> None:
    await ctx.send('Showing all rare skins now.')

    await client.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants=client.party.me.create_variants(clothing_color=1)
    )

    await ctx.send('Skin set to Purple Skull Trooper!')
    print(f"[PartyBot] [{time()}] Skin set to Purple Skull Trooper.")
    await asyncio.sleep(2)

    await client.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=client.party.me.create_variants(material=3)
    )

    await ctx.send('Skin set to Pink Ghoul Trooper!')
    print(f"[PartyBot] [{time()}] Skin set to Pink Ghoul Trooper.")
    await asyncio.sleep(2)

    for rare_skin in ('CID_028_Athena_Commando_F', 'CID_017_Athena_Commando_M'):
        await client.party.me.set_outfit(
            asset=rare_skin
        )

        await ctx.send(f'Skin set to {rare_skin}!')
        print(f"[PartyBot] [{time()}] Skin set to: {rare_skin}!")
        await asyncio.sleep(2)


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to Golden Peely "
                "(shortcut for !enlightened CID_701_Athena_Commando_M_BananaAgent 2 350).",
    help="Sets the outfit of the client to Golden Peely.\n"
    "Example: !goldenpeely"
)
async def goldenpeely(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=client.party.me.create_variants(progressive=4),
        enlightenment=(2, 350)
    )

    await ctx.send(f'Skin set to Golden Peely.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Randomly finds & equips a skin. Types currently include skin, backpack, emote & all. "
                "If type is left blank, a random skin will be equipped.",
    help="Randomly finds & equips a skin.\n"
    "Example: !random skin"
)
async def random(ctx: fortnitepy.ext.commands.Context, cosmetic_type: str = 'skin') -> None:
    if cosmetic_type == 'skin':
        all_outfits = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaCharacter"
        )

        random_skin = py_random.choice(all_outfits).id

        await client.party.me.set_outfit(
            asset=random_skin,
            variants=client.party.me.create_variants(profile_banner='ProfileBanner')
        )

        await ctx.send(f'Skin randomly set to {skin}.')

    elif cosmetic_type == 'backpack':
        all_backpacks = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaBackpack"
        )

        random_backpack = py_random.choice(all_backpacks).id

        await client.party.me.set_backpack(
            asset=random_backpack,
            variants=client.party.me.create_variants(profile_banner='ProfileBanner')
        )

        await ctx.send(f'Backpack randomly set to {backpack}.')

    elif cosmetic_type == 'emote':
        all_emotes = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaDance"
        )

        random_emote = py_random.choice(all_emotes).id

        await client.party.me.set_emote(
            asset=random_emote
        )

        await ctx.send(f'Emote randomly set to {emote}.')

    elif cosmetic_type == 'all':
        all_outfits = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaCharacter"
        )

        all_backpacks = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaBackpack"
        )

        all_emotes = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaDance"
        )

        random_outfit = py_random.choice(all_outfits).id
        random_backpack = py_random.choice(all_backpacks).id
        random_emote = py_random.choice(all_emotes).id

        await client.party.me.set_outfit(
            asset=random_outfit
        )

        await ctx.send(f'Skin randomly set to {random_outfit}.')

        await client.party.me.set_backpack(
            asset=random_backpack
        )

        await ctx.send(f'Backpack randomly set to {random_backpack}.')

        await client.party.me.set_emote(
            asset=random_emote
        )

        await ctx.send(f'Emote randomly set to {random_emote}.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Clears the currently set backpack.",
    help="Clears the currently set backpack.\n"
    "Example: !nobackpack"
)
async def nobackpack(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.clear_backpack()
    await ctx.send('Removed backpack.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Clears the currently set pet.",
    help="Clears the currently set pet.\n"
    "Example: !nopet"
)
async def nopet(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.clear_pet()
    await ctx.send('Removed pet.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Clears the currently set contrail.",
    help="Clears the currently set contrail.\n"
    "Example: !nocontrail"
)
async def nocontrail(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.clear_contrail()
    await ctx.send('Removed contrail.')


@commands.dm_only()
@client.command(
    description="[Party] Sets the client to the \"In Match\" state. If the first argument is 'progressive', "
                "the players remaining will gradually drop to mimic a real game.",
    help="Sets the client to the \"In Match\" state.\n"
    "Example: !match 69 420"
)
async def match(ctx: fortnitepy.ext.commands.Context, players: Union[str, int] = 0, match_time: int = 0) -> None:
    if players == 'progressive':
        match_time = datetime.datetime.utcnow()

        await client.party.me.set_in_match(
            players_left=100,
            started_at=match_time
        )

        while (100 >= client.party.me.match_players_left > 0
               and client.party.me.in_match()):

            await client.party.me.set_in_match(
                players_left=client.party.me.match_players_left - py_random.randint(3, 6),
                started_at=match_time
            )

            await asyncio.sleep(py_random.randint(45, 65))

    else:
        await client.party.me.set_in_match(
            players_left=int(players),
            started_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=match_time)
        )

        await ctx.send(f'Set state to in-game in a match with {players} players.'
                       '\nUse the command: !lobby to revert back to normal.')


@commands.dm_only()
@client.command(
    description="[Party] Sets the client to normal pre-game lobby state.",
    help="Sets the client to normal pre-game lobby state.\n"
    "Example: !lobby"
)
async def lobby(ctx: fortnitepy.ext.commands.Context) -> None:
    if client.default_party_member_config.cls == fortnitepy.JustChattingClientPartyMember:
        client.default_party_member_config.cls = fortnitepy.ClientPartyMember

        party_id = client.party.id
        await client.party.me.leave()

        await ctx.send('Removed state of Just Chattin\'. Now attempting to rejoin party.')

        try:
            await client.join_to_party(party_id)
        except fortnitepy.errors.Forbidden:
            await ctx.send('Failed to join back as party is set to private.')
        except fortnitepy.errors.NotFound:
            await ctx.send('Party not found, are you sure Fortnite is open?')

    await client.party.me.clear_in_match()

    await ctx.send('Set state to the pre-game lobby.')


@commands.dm_only()
@client.command(
    description="[Party] Joins the party of the defined friend. If friend is left blank, "
                "the message author will be used.",
    help="Joins the party of the defined friend.\n"
    "Example: !join Terbau"
)
async def join(ctx: fortnitepy.ext.commands.Context, *, epic_username: Union[str, None] = None) -> None:
    if epic_username is None:
        epic_friend = client.get_friend(ctx.author.id)
    else:
        user = await client.fetch_profile(epic_username)

        if user is not None:
            epic_friend = client.get_friend(user.id)
        else:
            epic_friend = None
            await ctx.send(f'Failed to find user with the name: {epic_username}.')

    if isinstance(epic_friend, fortnitepy.Friend):
        try:
            await epic_friend.join_party()
            await ctx.send(f'Joined the party of {epic_friend.display_name}.')
        except fortnitepy.errors.Forbidden:
            await ctx.send('Failed to join party since it is private.')
        except fortnitepy.errors.PartyError:
            await ctx.send('Party not found, are you sure Fortnite is open?')
    else:
        await ctx.send('Cannot join party as the friend is not found.')


@commands.dm_only()
@client.command(
    description="[Party] Sends the defined user a friend request.",
    help="Sends the defined user a friend request.\n"
    "Example: !friend Ninja"
)
async def friend(ctx: fortnitepy.ext.commands.Context, *, epic_username: str) -> None:
    if data['friend_accept']:
        await ctx.send('All friend requests will be accepted so there is no need to add manually.')
        print(f'[PartyBot] [{time()}] !friend command ignored as friend requests will be accepted '
              'so there is no need to add manually.')
    else:
        user = await client.fetch_profile(epic_username)

        if user is not None:
            await client.add_friend(user.id)
            await ctx.send(f'Sent/accepted friend request to/from {user.display_name}.')
            print(f'[PartyBot] [{time()}] Sent/accepted friend request to/from {user.display_name}.')
        else:
            await ctx.send(f'Failed to find user with the name: {epic_username}.')
            print(crayons.red(f"[PartyBot] [{time()}] [ERROR] Failed to find a user with the name {epic_username}."))


@commands.dm_only()
@client.command(
    description="[Party] Sets the lobbies selected playlist using playlist name.",
    help="Sets the lobbies selected playlist using playlist name.\n"
    "Example: !playlist Food Fight"
)
async def playlist(ctx: fortnitepy.ext.commands.Context, *, playlist_name: str) -> None:
    try:
        scuffedapi_playlist_id = await get_playlist(playlist_name)

        if scuffedapi_playlist_id is not None:
            await client.party.set_playlist(playlist=scuffedapi_playlist_id)
            await ctx.send(f'Playlist set to {scuffedapi_playlist_id}.')
            print(f'[PartyBot] [{time()}] Playlist set to {scuffedapi_playlist_id}.')

        else:
            await ctx.send(f'Failed to find a playlist with the name: {playlist_name}.')
            print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                              f"Failed to find a playlist with the name: {playlist_name}."))

    except fortnitepy.errors.Forbidden:
        await ctx.send(f"Failed to set playlist to {playlist_name}, as I'm not party leader.")
        print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                          "Failed to set playlist as I don't have the required permissions."))


@commands.dm_only()
@client.command(
    description="[Party] Invites the defined friend to the party. If friend is left blank, "
                "the message author will be used.",
    help="Invites the defined friend to the party.\n"
    "Example: !invite Terbau"
)
async def invite(ctx: fortnitepy.ext.commands.Context, *, epic_username: Union[str, None] = None) -> None:
    if epic_username is None:
        epic_friend = client.get_friend(ctx.author.id)
    else:
        user = await client.fetch_profile(epic_username)

        if user is not None:
            epic_friend = client.get_friend(user.id)
        else:
            epic_friend = None
            await ctx.send(f'Failed to find user with the name: {epic_username}.')
            print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                              f"Failed to find user with the name: {epic_username}."))

    if isinstance(epic_friend, fortnitepy.Friend):
        try:
            await epic_friend.invite()
            await ctx.send(f'Invited {epic_friend.display_name} to the party.')
            print(f"[PartyBot] [{time()}] [ERROR] Invited {epic_friend.display_name} to the party.")
        except fortnitepy.errors.PartyError:
            await ctx.send('Failed to invite friend as they are either already in the party or it is full.')
            print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                              "Failed to invite to party as friend is already either in party or it is full."))
    else:
        await ctx.send('Cannot invite to party as the friend is not found.')
        print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                          "Failed to invite to party as the friend is not found."))


@commands.dm_only()
@client.command(
    description="[Party] Hides everyone in the party except for the bot but if a player is specified, "
                "that specific player will be hidden.",
    help="Hides members of the party.\n"
    "Example: !hide"
)
async def hide(ctx: fortnitepy.ext.commands.Context, party_member: Union[str, None] = None) -> None:
    if client.party.me.leader:
        if party_member is not None:
            user = await client.fetch_profile(party_member)
            member = client.party.members.get(user.id)

            if member is not None:
                raw_squad_assignments = client.party.meta.get_prop(
                    'Default:RawSquadAssignments_j'
                )["RawSquadAssignments"]

                for player in raw_squad_assignments:
                    if player['memberId'] == member.id:
                        raw_squad_assignments.remove(player)

                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j', {
                        'RawSquadAssignments': raw_squad_assignments
                    }
                )
            else:
                await ctx.send(f'Failed to find user with the name: {party_member}.')
                print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                                  f"Failed to find user with the name: {party_member}."))
        else:
            await set_and_update_party_prop(
                'Default:RawSquadAssignments_j', {
                    'RawSquadAssignments': [{'memberId': client.user.id, 'absoluteMemberIdx': 1}]
                }
            )

            await ctx.send('Hid everyone in the party. Use !unhide if you want to unhide everyone.'
                           '\nReminder: Crashing lobbies is bannable offense which will result in a permanent ban.')
            print(f'[PartyBot] [{time()}] Hid everyone in the party.')
    else:
        await ctx.send("Failed to hide everyone, as I'm not party leader")
        print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
                          "Failed to hide everyone as I don't have the required permissions."))


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client using the outfits name with the ghost variant.",
    help="Sets the outfit of the client using the outfits name with the ghost variant.\n"
    "Example: !ghost Meowscles"
)
async def ghost(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        skin_variants = client.party.me.create_variants(
            progressive=2
        )

        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaCharacter"
        )

        await client.party.me.set_outfit(
            asset=cosmetic.id,
            variants=skin_variants
        )

        await ctx.send(f'Skin set to Ghost {cosmetic.name}!')
        print(f'[PartyBot] [{time()}] Skin set to Ghost {cosmetic.name}.')

    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a skin with the name: {content}.")
        print(f"[PartyBot] [{time()}] Failed to find a skin with the name: {content}.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client using the outfits name with the shadow variant.",
    help="Sets the outfit of the client using the outfits name with the shadow variant.\n"
    "Example: !shadow Midas"
)
async def shadow(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        skin_variants = client.party.me.create_variants(
            progressive=3
        )

        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaCharacter"
        )

        await client.party.me.set_outfit(
            asset=cosmetic.id,
            variants=skin_variants
        )

        await ctx.send(f'Skin set to Shadow {cosmetic.name}!')
        print(f'[PartyBot] [{time()}] Skin set to Ghost {cosmetic.name}.')

    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a skin with the name: {content}.")
        print(f"[PartyBot] [{time()}] Failed to find a skin with the name: {content}.")


@commands.dm_only()
@client.command(
    description="[Client] Sets the clients kairos/PartyHub avatar.",
    help="Sets the clients kairos/PartyHub avatar.\n"
    "Example: !avatar stw_soldier_f"
)
async def avatar(ctx: fortnitepy.ext.commands.Context, kairos_cid: str) -> None:
    kairos_avatar = fortnitepy.Avatar(
        asset=kairos_cid
    )

    client.set_avatar(kairos_avatar)

    await ctx.send(f'Kairos avatar set to {kairos_cid}.')
    print(f'[PartyBot] [{time()}] Kairos avatar set to {kairos_cid}.')


@commands.dm_only()
@client.command(
    aliases=['clear'],
    description="[Client] Clears command prompt/terminal.",
    help="Clears command prompt/terminal.\n"
    "Example: !clean"
)
async def clean(ctx: fortnitepy.ext.commands.Context) -> None:
    os.system('cls' if 'win' in sys.platform else 'clear')

    print(crayons.cyan(f'[PartyBot] [{time()}] PartyBot made by xMistt. '
                       'Massive credit to Terbau for creating the library.'))
    print(crayons.cyan(f'[PartyBot] [{time()}] Discord server: https://discord.gg/fnpy - For support, questions, etc.'))

    await ctx.send('Command prompt/terminal cleared.')
    print(f'[PartyBot] [{time()}] Command prompt/terminal cleared.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Equips all cosmetics from a set.",
    help="Equips all cosmetics from a set.\n"
    "Example: !set Fort Knights"
)
async def set(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    cosmetic_types = {
        "AthenaBackpack": client.party.me.set_backpack,
        "AthenaCharacter": client.party.me.set_outfit,
        "AthenaEmoji": client.party.me.set_emoji,
        "AthenaDance": client.party.me.set_emote
    }

    set_items = await BenBotAsync.get_cosmetics(
        lang="en",
        searchLang="en",
        matchMethod="contains",
        set=content
    )

    await ctx.send(f'Equipping all cosmetics from the {set_items[0].set} set.')
    print(f'[PartyBot] [{time()}] Equipping all cosmetics from the {set_items[0].set} set.')

    for cosmetic in set_items:
        if cosmetic.backend_type.value in cosmetic_types:
            await cosmetic_types[cosmetic.backend_type.value](asset=cosmetic.id)

            await ctx.send(f'{cosmetic.short_description} set to {cosmetic.name}!')
            print(f'[PartyBot] [{time()}] {cosmetic.short_description} set to {cosmetic.name}.')

            await asyncio.sleep(3)

    await ctx.send(f'Finished equipping all cosmetics from the {set_items[0].set} set.')
    print(f'[PartyBot] [{time()}] Fishing equipping  all cosmetics from the {set_items[0].set} set.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Creates the variants list by the variants you set from skin name. "
                "If you want to include spaces in the skin name, you need to enclose it in \"'s.",
    help="Creates the variants list by the variants you set from skin name.\n"
    "Example: !style \"Skull Trooper\" clothing_color 1"
)
async def style(ctx: fortnitepy.ext.commands.Context, cosmetic_name: str, variant_type: str, variant_int: str) -> None:
    # cosmetic_types = {
    #     "AthenaCharacter": client.party.me.set_outfit,
    #     "AthenaBackpack": client.party.me.set_backpack,
    #     "AthenaPickaxe": client.party.me.set_pickaxe
    # }

    cosmetic = await BenBotAsync.get_cosmetic(
        lang="en",
        searchLang="en",
        matchMethod="contains",
        name=cosmetic_name,
        backendType="AthenaCharacter"
    )

    cosmetic_variants = client.party.me.create_variants(
        # item=cosmetic.backend_type.value,
        **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
    )

    # await cosmetic_types[cosmetic.backend_type.value](
    await client.party.me.set_outfit(
        asset=cosmetic.id,
        variants=cosmetic_variants
    )

    await ctx.send(f'Set variants of {cosmetic.id} to {variant_type} {variant_int}.')
    print(f'[PartyBot] [{time()}] Set variants of {cosmetic.id} to {variant_type} {variant_int}.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Equips all new non encrypted skins.",
    help="Equips all new non encrypted skins.\n"
    "Example: !new"
)
async def new(ctx: fortnitepy.ext.commands.Context) -> None:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='https://benbotfn.tk/api/v1/files/added',
        )

        response = await request.json()

    for new_skin in [new_cid for new_cid in response if new_cid.split('/')[-1].lower().startswith('cid_')]:
        await client.party.me.set_outfit(
            asset=new_skin.split('/')[-1].split('.uasset')[0]
        )

        await ctx.send(f"Skin set to {new_skin.split('/')[-1].split('.uasset')[0]}!")
        print(f"[PartyBot] [{time()}] Skin set to: {new_skin.split('/')[-1].split('.uasset')[0]}!")

        await asyncio.sleep(3)

    await ctx.send(f'Finished equipping all new unencrypted skins.')
    print(f'[PartyBot] [{time()}] Finished equipping all new unencrypted skins.')

    for new_emote in [new_eid for new_eid in response if new_eid.split('/')[-1].lower().startswith('eid_')]:
        await client.party.me.set_emote(
            asset=new_skin.split('/')[-1].split('.uasset')[0]
        )

        await ctx.send(f"Emote set to {new_eid.split('/')[-1].split('.uasset')[0]}!")
        print(f"[PartyBot] [{time()}] Emote set to: {new_eid.split('/')[-1].split('.uasset')[0]}!")

        await asyncio.sleep(3)

    await ctx.send(f'Finished equipping all new unencrypted skins.')
    print(f'[PartyBot] [{time()}] Finished equipping all new unencrypted skins.')


@commands.dm_only()
@client.command(
    description="[Party] Sets the client to the \"Just Chattin'\" state.",
    help="Sets the client to the \"Just Chattin'\" state.\n"
    "Example: !justchattin"
)
async def justchattin(ctx: fortnitepy.ext.commands.Context) -> None:
    client.default_party_member_config.cls = fortnitepy.JustChattingClientPartyMember

    party_id = client.party.id
    await client.party.me.leave()

    await ctx.send('Set state to Just Chattin\'. Now attempting to rejoin party.'
                   '\nUse the command: !lobby to revert back to normal.')

    try:
        await client.join_to_party(party_id)
    except fortnitepy.errors.Forbidden:
        await ctx.send('Failed to join back as party is set to private.')
    except fortnitepy.errors.NotFound:
        await ctx.send('Party not found, are you sure Fortnite is open?')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Equips all skins currently in the item shop.",
    help="Equips all skins currently in the item shop.\n"
    "Example: !shop"
)
async def shop(ctx: fortnitepy.ext.commands.Context) -> None:
    store = await client.fetch_item_shop()

    await ctx.send(f"Equipping all skins in today's item shop.")
    print(f"[PartyBot] [{time()}] Equipping all skins in today's item shop.")

    for item in store.special_featured_items + store.special_daily_items + special_featured_items + special_daily_items:
        for grant in item.grants:
            if grant['type'] == 'AthenaCharacter':
                await client.party.me.set_outfit(
                    asset=grant['asset']
                )

                await ctx.send(f"Skin set to {item.display_names[0]}!")
                print(f"[PartyBot] [{time()}] Skin set to: {item.display_names[0]}!")

                await asyncio.sleep(3)

    await ctx.send(f'Finished equipping all skins in the item shop.')
    print(f'[PartyBot] [{time()}] Finished equipping all skins in the item shop.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Equips a random old default skin.",
    help="Equips a random old default skin.\n"
    "Example: !olddefault"
)
async def olddefault(ctx: fortnitepy.ext.commands.Context) -> None:
    random_default = py_random.choice(
        [cid_ for cid_ in dir(fortnitepy.DefaultCharactersChapter1) if not cid_.startswith('_')]
    )

    await client.party.me.set_outfit(
        asset=random_default
    )

    await ctx.send(f'Skin set to {random_default}!')
    print(f"[PartyBot] [{time()}] Skin set to {random_default}.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to Hatless Recon Expert.",
    help="Sets the outfit of the client to Hatless Recon Expert.\n"
    "Example: !hatlessrecon"
)
async def hatlessrecon(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        parts=2
    )

    await client.party.me.set_outfit(
        asset='CID_022_Athena_Commando_F',
        variants=skin_variants
    )

    await ctx.send('Skin set to Hatless Recon Expert!')
    print(f'[PartyBot] [{time()}] Skin set to Hatless Recon Expert.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the to the max tier skin in the defined season.",
    help="Sets the outfit of the to the max tier skin in the defined season.\n"
    "Example: !season 2"
)
async def season(ctx: fortnitepy.ext.commands.Context, br_season: int) -> None:
    max_tier_skins = {
        1: "CID_028_Athena_Commando_F",
        2: "CID_035_Athena_Commando_M_Medieval",
        3: "CID_084_Athena_Commando_M_Assassin",
        4: "CID_116_Athena_Commando_M_CarbideBlack",
        5: "CID_165_Athena_Commando_M_DarkViking",
        6: "CID_230_Athena_Commando_M_Werewolf",
        7: "CID_288_Athena_Commando_M_IceKing",
        8: "CID_352_Athena_Commando_F_Shiny",
        9: "CID_407_Athena_Commando_M_BattleSuit",
        10: "CID_484_Athena_Commando_M_KnightRemix",
        11: "CID_572_Athena_Commando_M_Viper",
        12: "CID_694_Athena_Commando_M_CatBurglar",
        13: "CID_767_Athena_Commando_F_BlackKnight"
    }

    await client.party.me.set_outfit(asset=max_tier_skins[br_season])

    await ctx.send(f'Skin set to {max_tier_skins[br_season]}!')
    print(f"[PartyBot] [{time()}] Skin set to {max_tier_skins[br_season]}.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to a random Henchman skin.",
    help="Sets the outfit of the client to a random Henchman skin.\n"
    "Example: !henchman"
)
async def henchman(ctx: fortnitepy.ext.commands.Context) -> None:
    random_henchman = py_random.choice(
        "CID_794_Athena_Commando_M_HenchmanBadShorts_D",
        "CID_NPC_Athena_Commando_F_HenchmanSpyDark",
        "CID_791_Athena_Commando_M_HenchmanGoodShorts_D",
        "CID_780_Athena_Commando_M_HenchmanBadShorts",
        "CID_NPC_Athena_Commando_M_HenchmanGood",
        "CID_692_Athena_Commando_M_HenchmanTough",
        "CID_707_Athena_Commando_M_HenchmanGood",
        "CID_792_Athena_Commando_M_HenchmanBadShorts_B",
        "CID_793_Athena_Commando_M_HenchmanBadShorts_C",
        "CID_NPC_Athena_Commando_M_HenchmanBad",
        "CID_790_Athena_Commando_M_HenchmanGoodShorts_C",
        "CID_779_Athena_Commando_M_HenchmanGoodShorts",
        "CID_NPC_Athena_Commando_F_RebirthDefault_Henchman",
        "CID_NPC_Athena_Commando_F_HenchmanSpyGood",
        "CID_706_Athena_Commando_M_HenchmanBad",
        "CID_789_Athena_Commando_M_HenchmanGoodShorts_B"
    )

    await client.party.me.set_outfit(
        asset=random_henchman
    )

    await ctx.send(f'Skin set to {random_henchman}!')
    print(f"[PartyBot] [{time()}] Skin set to {random_henchman}.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the emote of the client to Floss.",
    help="Sets the emote of the client to Floss.\n"
    "Example: !floss"
)
async def floss(ctx: fortnitepy.ext.commands.Context) -> None:
    # // You caused this FunGames, you caused this...
    await client.party.me.set_emote(
        asset='EID_Floss'
    )

    await ctx.send('Emote set to Floss!')
    print(f"[PartyBot] [{time()}] Emote set to Floss.")


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to a random marauder skin.",
    help="Sets the outfit of the client to a random marauder skin.\n"
    "Example: !marauder"
)
async def marauder(ctx: fortnitepy.ext.commands.Context) -> None:
    random_marauder = py_random.choice(
        "CID_NPC_Athena_Commando_M_MarauderHeavy",
        "CID_NPC_Athena_Commando_M_MarauderElite",
        "CID_NPC_Athena_Commando_M_MarauderGrunt"
    )

    await client.party.me.set_outfit(
        asset=random_marauder
    )

    await ctx.send(f'Skin set to {random_marauder}!')
    print(f"[PartyBot] [{time()}] Skin set to {random_marauder}.")


@commands.dm_only()
@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to Golden Brutus "
                "(shortcut for !enlightened CID_692_Athena_Commando_M_HenchmanTough 2 180).",
    help="Sets the outfit of the client to Golden Brutus.\n"
    "Example: !goldenbrutus"
)
async def goldenbrutus(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_692_Athena_Commando_M_HenchmanTough',
        variants=client.party.me.create_variants(progressive=4),
        enlightenment=(2, 180)
    )

    await ctx.send(f'Skin set to Golden Brutus.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to Golden Meowscles "
                "(shortcut for !enlightened CID_693_Athena_Commando_M_BuffCat 2 220).",
    help="Sets the outfit of the client to Golden Meowscles.\n"
    "Example: !goldenmeowscles"
)
async def goldenmeowscles(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_693_Athena_Commando_M_BuffCat',
        variants=client.party.me.create_variants(progressive=4),
        enlightenment=(2, 220)
    )

    await ctx.send(f'Skin set to Golden Meowscles.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to Golden Midas "
                "(shortcut for !enlightened CID_694_Athena_Commando_M_CatBurglar 2 140).",
    help="Sets the outfit of the client to Golden Peely.\n"
    "Example: !goldenmidas"
)
async def goldenmidas(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_694_Athena_Commando_M_CatBurglar',
        variants=client.party.me.create_variants(progressive=4),
        enlightenment=(2, 140)
    )

    await ctx.send(f'Skin set to Golden Midas.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to Golden Skye "
                "(shortcut for !enlightened CID_690_Athena_Commando_F_Photographer 2 300).",
    help="Sets the outfit of the client to Golden Skye.\n"
    "Example: !goldenskye"
)
async def goldenskye(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_690_Athena_Commando_F_Photographer',
        variants=client.party.me.create_variants(progressive=4),
        enlightenment=(2, 300)
    )

    await ctx.send(f'Skin set to Golden Skye.')


@commands.dm_only()
@client.command(
    description="[Cosmetic] Sets the outfit of the client to Golden TNTina "
                "(shortcut for !enlightened CID_691_Athena_Commando_F_TNTina 2 350).",
    help="Sets the outfit of the client to Golden TNTina.\n"
    "Example: !goldentntina"
)
async def goldentntina(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_691_Athena_Commando_F_TNTina',
        variants=client.party.me.create_variants(progressive=7),
        enlightenment=(2, 260)
    )

    await ctx.send(f'Skin set to Golden TNTina.')


if (data['email'] and data['password']) and (data['email'] != 'email@email.com' and data['password'] != 'password1'):
    try:
        client.run()
    except fortnitepy.errors.AuthException as e:
        print(crayons.red(f"[PartyBot] [{time()}] [ERROR] {e}"))
else:
    print(crayons.red(f"[PartyBot] [{time()}] [ERROR] Failed to login as no (or default) account details provided."))
