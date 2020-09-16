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
    import asyncio
    import json
    import logging
    import sys

    # Third party imports.
    import partybot
    import aiofiles
    import fortnitepy
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


async def main() -> None:
    settings = partybot.BotSettings()
    device_auths = partybot.DeviceAuths(
        filename='device_auths.json'
    )

    await settings.load_settings_from_file('config.json')
    await device_auths.load_device_auths()

    if settings.debug:
        enable_debug()

    client = partybot.PartyBot(
        settings=settings,
        device_auths=device_auths
    )

    client.add_cog(partybot.CosmeticCommands(client))
    client.add_cog(partybot.PartyCommands(client))
    client.add_cog(partybot.ClientCommands(client))

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method="GET",
            url="https://partybot.net/api/discord"
        ) as r:
            invite = (await r.json())['invite'] if r.status == 200 else "8heARRB"

    print(crayons.cyan(client.message % 'PartyBot made by xMistt. '
                       'Massive credit to Terbau for creating the library.'))
    print(crayons.cyan(client.message % f'Discord server: https://discord.gg/{invite} - For support, questions, etc.'))

    if (settings.email and settings.password) and \
            (settings.email != 'email@email.com' and settings.password != 'password1'):
        try:
            await client.start()
        except fortnitepy.errors.AuthException as e:
            print(crayons.red(client.message % f"[ERROR] {e}"))
    else:
        print(crayons.red(client.message % f"[ERROR] Failed to login as no (or default) "
                          "account details provided."))

    await client.http.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
