# -*- coding: utf-8 -*-

"""
“Commons Clause” License Condition v1.0
Copyright Oli 2019-2021

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

License: Apache 2.0 Modified.
"""

try:
    # System imports.
    import asyncio
    import json
    import logging
    import sys
    import datetime

    # Third party imports.
    import partybot
    import aiofiles
    import rebootpy
    import crayons
    import aiohttp
except ModuleNotFoundError as e:
    print(e)
    print('Failed to import 1 or more modules, running "INSTALL PACKAGES.bat" '
          'might fix the issue, if not please create an issue or join '
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


def enable_debug() -> None:
    modules = {
        'fortnitepy.http': 6,
        'fortnitepy.xmpp': 5
    }
    
    for module, colour in module.items():
        logger = logging.getLogger(module)
        logger.setLevel(level=logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(f'\u001b[3{colour}m %(asctime)s:%(levelname)s:%(name)s: %(message)s'
                                               ' \u001b[0m'))
        logger.addHandler(handler)

        
async def main() -> None:
    settings = partybot.BotSettings()

    await settings.load_settings_from_file('config.json')

    if settings.debug:
        enable_debug()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method="GET",
                url="https://partybot.net/api/discord",
                timeout=3
            ) as r:
                invite = (await r.json())['invite'] if r.status == 200 else "8heARRB"
    except (asyncio.TimeoutError, aiohttp.client_exceptions.ContentTypeError):
        invite = "8heARRB"

    print(crayons.cyan(f"[PartyBot] [{datetime.datetime.now().strftime('%H:%M:%S')}] PartyBot made by xMistt. "
                       'Massive credit to Terbau for creating the library.'))
    print(crayons.cyan(f"[PartyBot] [{datetime.datetime.now().strftime('%H:%M:%S')}] Discord server: "
                       f"https://discord.gg/{invite} - For support, questions, etc."))

    device_auths = partybot.DeviceAuths(
        filename='device_auths.json'
    )

    try:
        await device_auths.load_device_auths()
    except partybot.errors.MissingDeviceAuth:
        print(f"[PartyBot] [{datetime.datetime.now().strftime('%H:%M:%S')}] Automatically opening Epic Games login, "
              f"please sign in.")

        gen = partybot.EpicGenerator()
        new_device_auths = await gen.generate_device_auths()
        device_auths.set_device_auth(
            **new_device_auths
        )

        await device_auths.save_device_auths()

    client = partybot.PartyBot(
        settings=settings,
        device_auths=device_auths
    )

    client.add_cog(partybot.CosmeticCommands(client))
    client.add_cog(partybot.PartyCommands(client))
    client.add_cog(partybot.ClientCommands(client))

    try:
        await client.start()
    except rebootpy.errors.AuthException as e:
        print(crayons.red(client.message % f"[ERROR] {e}"))

    await client.http.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())