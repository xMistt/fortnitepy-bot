"""
“Commons Clause” License Condition v1.0
Copyright Oli 2019-2023

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

# System imports.
from typing import Any

import uuid
import datetime
import asyncio
import functools

# Third party imports.
from rebootpy.ext import commands

import rebootpy
import crayons
import FortniteAPIAsync
import pypresence

# Local imports
from .settings import BotSettings
from .deviceauths import DeviceAuth, DeviceAuths
# from .helper import HelperFunctions


class PartyBot(commands.Bot):
    def __init__(self, settings: BotSettings, device_auths: DeviceAuths) -> None:
        self.device_auths = device_auths.get_device_auth()
        self.settings = settings

        self.fortnite_api = FortniteAPIAsync.APIClient()

        super().__init__(
            command_prefix='!',
            auth=rebootpy.DeviceAuth(
                device_id=self.device_auths.device_id,
                account_id=self.device_auths.account_id,
                secret=self.device_auths.secret
            ),
            status=self.settings.status,
            platform=rebootpy.Platform(self.settings.platform)
        )

    @property
    def message(self) -> str:
        return f'[PartyBot] [{datetime.datetime.now().strftime("%H:%M:%S")}] %s'

    async def start_discord_rich_presence(self) -> None:
        rpc = pypresence.AioPresence(
            client_id='717610574837710919',
            loop=self.loop
        )

        try:
            await rpc.connect()
        except Exception as discord_error:
            print(f'There was an error: {discord_error}.')

        start_time = datetime.datetime.now().timestamp()

        while True:
            try:
                outfit = (await self.fortnite_api.cosmetics.get_cosmetic_from_id(
                    fortnite_id=self.party.me.outfit
                )).name
            except FortniteAPIAsync.exceptions.NotFound:
                outfit = self.party.me.outfit

            await rpc.update(
                details=f"Logged in as {self.user.display_name}.",
                state=f"{self.party.leader.display_name}'s party.",
                large_image="skull_trooper",
                large_text="discord.gg/8heARRB",
                small_image="outfit",
                small_text=outfit,
                start=int(start_time),
                party_id=self.party.id,
                party_size=[self.party.member_count, 16],
                join=uuid.uuid4().hex
            )

            await asyncio.sleep(20)

    async def set_and_update_member_prop(self, schema_key: str, new_value: Any) -> None:
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.me.patch(updated=prop)

    async def set_and_update_party_prop(self, schema_key: str, new_value: Any) -> None:
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.patch(updated=prop)

    async def event_device_auth_generate(self, details: dict, email: str) -> None:
        device_auth = DeviceAuth(
            email=email,
            **details
        )

        await self.device_auths.save_device_auth(device_auth)

    async def event_ready(self) -> None:
        print(crayons.green(self.message % f'Client ready as {self.user.display_name}.'))
        
        if self.party.me.leader:
            await self.party.set_privacy(rebootpy.PartyPrivacy.PUBLIC)

        # discord_exists = await self.loop.run_in_executor(None, HelperFunctions.check_if_process_running, 'Discord')

        # if discord_exists:
        #     asyncio.get_event_loop().create_task(self.start_discord_rich_presence())

        # NOTE: Ignore this commented out code below, I use it to generate the "docs".
        # command_docs = [
        #     (
        #         "Contents:\n"
        #         "* [Cosmetic Commands](https://github.com/xMistt/fortnitepy-bot/wiki/Commands#cosmetic-commands)\n"
        #         "* [Party Commands](https://github.com/xMistt/fortnitepy-bot/wiki/Commands#party-commands)\n"
        #         "* [Client Commands](https://github.com/xMistt/fortnitepy-bot/wiki/Commands#client-commands)\n"
        #     )
        # ]
        #
        # sorted_commands = {
        #     "Cosmetic": [],
        #     "Party": [],
        #     "Client": []
        # }
        #
        # for command in self.commands:
        #     if not command.help:
        #         print(f'{command.name} is missing documentation')
        #         continue
        #
        #     if not command.cog:
        #         print(f'{command.name} is outside of a cog')
        #         continue
        #
        #     description, example = command.help.rsplit('Example: ', 1)
        #     sorted_commands[command.cog.name].append((
        #         command.name,
        #         f"* !{command.name} - {description.replace('\n', '<br>')}\n"
        #         f"``Usage: {command.usage}``<br>\n"
        #         f"``Example: {example}``\n"
        #     ))
        #
        # for category in sorted_commands:
        #     sorted_commands[category].sort(key=lambda command: command[0])
        #
        # for command_group, commands in sorted_commands.items():
        #     command_docs.append(f"## {command_group} Commands")
        #     for command in commands:
        #         command_docs.append(command[1])
        #
        # import pyperclip
        # pyperclip.copy("\n".join(command_docs))
        # print("Copied commands documentation to clipboard")

        for pending in self.incoming_pending_friends:
            try:
                epic_friend = await pending.accept() if self.settings.friend_accept else await pending.decline()
                if isinstance(epic_friend, rebootpy.Friend):
                    print(self.message % f"Accepted friend request from: {epic_friend.display_name}.")
                else:
                    print(self.message % f"Declined friend request from: {pending.display_name}.")
            except rebootpy.HTTPException as epic_error:
                if epic_error.message_code != 'errors.com.epicgames.common.throttled':
                    raise

                await asyncio.sleep(int(epic_error.message_vars[0] + 1))
                await pending.accept() if self.settings.friend_accept else await pending.decline()

    async def event_party_invite(self, invite: rebootpy.ReceivedPartyInvitation) -> None:
        await invite.accept()
        print(self.message % f'Accepted party invite from {invite.sender.display_name}.')

    async def event_friend_request(self, request: rebootpy.IncomingPendingFriend) -> None:
        if isinstance(request, rebootpy.OutgoingPendingFriend):
            return

        print(self.message % f"Received friend request from: {request.display_name}.")

        if self.settings.friend_accept:
            await request.accept()
            print(self.message % f"Accepted friend request from: {request.display_name}.")
        else:
            await request.decline()
            print(self.message % f"Declined friend request from: {request.display_name}.")

    async def event_party_member_join(self, member: rebootpy.PartyMember) -> None:
        if self.user.id != member.id:
            await self.party.send(
                'Notice: Join discord.gg/8heARRB for a free lobby bot.'
            )
            print(
                f"[PartyBot] [{datetime.datetime.now().strftime('%H:%M:%S')}] "
                f"{member.display_name} has joined the lobby."
            )

        config = self.settings.to_dict()
        await self.party.me.edit_and_keep(
            functools.partial(
                self.party.me.set_outfit,
                config['cid']
            ),
            functools.partial(
                self.party.me.set_backpack,
                config['bid']
            ),
            functools.partial(
                self.party.me.set_pickaxe,
                config['pickaxe_id']
            ),
            functools.partial(
                self.party.me.set_banner,
                icon=config['banner'],
                color=config['banner_colour'],
                season_level=config['level']
            ),
            functools.partial(
                self.party.me.set_battlepass_info,
                has_purchased=True,
                level=config['bp_tier']
            )
        )

        await asyncio.sleep(1)

        await self.party.me.clear_emote()
        await self.party.me.set_emote(asset=config['eid'])

    async def event_friend_message(self, message: rebootpy.FriendMessage) -> None:
        print(self.message % f'{message.author.display_name}: {message.content}')

    async def event_command_error(self, ctx: rebootpy.ext.commands.Context,
                                  error: rebootpy.ext.commands.CommandError) -> None:
        if isinstance(error, rebootpy.ext.commands.errors.CommandNotFound):
            if isinstance(ctx.message, rebootpy.FriendMessage):
                await ctx.send('Command not found, are you sure it exists?')
            else:
                pass
        elif isinstance(error, rebootpy.ext.commands.errors.MissingRequiredArgument):
            await ctx.send('Failed to execute commands as there are missing requirements, please check usage.')
        elif isinstance(error, rebootpy.ext.commands.errors.PrivateMessageOnly):
            pass
        else:
            await ctx.send(f'When trying to process !{ctx.command.name}, an error occured: "{error}"\n'
                           f'Please report this on Discord or GitHub.')
            raise error
