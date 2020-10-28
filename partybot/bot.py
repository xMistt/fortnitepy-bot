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

from .settings import BotSettings
from .deviceauths import DeviceAuth, DeviceAuths
from .helper import HelperFunctions

# System imports.
from typing import Any

import uuid
import datetime
import asyncio

# Third party imports.
from fortnitepy.ext import commands

import fortnitepy
import crayons
import BenBotAsync
import FortniteAPIAsync
import pypresence


class PartyBot(commands.Bot):
    def __init__(self, settings: BotSettings, device_auths: DeviceAuths) -> None:
        self.device_auths = device_auths
        self.settings = settings

        self.fortnite_api = FortniteAPIAsync.APIClient()

        account_device_auths = self.device_auths.get_device_auth(
            email=settings.email
        )

        super().__init__(
            command_prefix='!',
            auth=fortnitepy.AdvancedAuth(
                email=self.settings.email,
                password=self.settings.password,
                prompt_authorization_code=True,
                delete_existing_device_auths=True,
                device_id=account_device_auths.device_id,
                account_id=account_device_auths.account_id,
                secret=account_device_auths.secret
            ),
            status=self.settings.status,
            platform=fortnitepy.Platform(self.settings.platform),
            avatar=fortnitepy.Avatar(
                asset=self.settings.cid,
                background_colors=fortnitepy.KairosBackgroundColorPreset.PINK.value
            )
        )

        self.message = f'[PartyBot] [{datetime.datetime.now().strftime("%H:%M:%S")}] %s'

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
                large_text="discord.gg/fnpy",
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

        # discord_exists = await self.loop.run_in_executor(None, HelperFunctions.check_if_process_running, 'Discord')

        # if discord_exists:
        #     asyncio.get_event_loop().create_task(self.start_discord_rich_presence())

        for pending in self.incoming_pending_friends:
            try:
                epic_friend = await pending.accept() if self.settings.friend_accept else await pending.decline()
                if isinstance(epic_friend, fortnitepy.Friend):
                    print(self.message % f"Accepted friend request from: {epic_friend.display_name}.")
                else:
                    print(self.message % f"Declined friend request from: {pending.display_name}.")
            except fortnitepy.HTTPException as epic_error:
                if epic_error.message_code != 'errors.com.epicgames.common.throttled':
                    raise

                await asyncio.sleep(int(epic_error.message_vars[0] + 1))
                await pending.accept() if self.settings.friend_accept else await pending.decline()

    async def event_party_invite(self, invite: fortnitepy.ReceivedPartyInvitation) -> None:
        await invite.accept()
        print(self.message % f'Accepted party invite from {invite.sender.display_name}.')

    async def event_friend_request(self, request: fortnitepy.IncomingPendingFriend) -> None:
        if isinstance(request, fortnitepy.OutgoingPendingFriend):
            return

        print(self.message % f"Received friend request from: {request.display_name}.")

        if self.settings.friend_accept:
            await request.accept()
            print(self.message % f"Accepted friend request from: {request.display_name}.")
        else:
            await request.decline()
            print(self.message % f"Declined friend request from: {request.display_name}.")

    async def event_party_member_join(self, member: fortnitepy.PartyMember) -> None:
        await BenBotAsync.set_default_loadout(
            self,
            self.settings.to_dict(),
            member
        )

    async def event_friend_message(self, message: fortnitepy.FriendMessage) -> None:
        print(self.message % f'{message.author.display_name}: {message.content}')

    async def event_command_error(self, ctx: fortnitepy.ext.commands.Context,
                                  error: fortnitepy.ext.commands.CommandError) -> None:
        if isinstance(error, fortnitepy.ext.commands.errors.CommandNotFound):
            if isinstance(ctx.message, fortnitepy.FriendMessage):
                await ctx.send('Command not found, are you sure it exists?')
            else:
                pass
        elif isinstance(error, fortnitepy.ext.commands.errors.MissingRequiredArgument):
            await ctx.send('Failed to execute commands as there are missing requirements, please check usage.')
        elif isinstance(error, fortnitepy.ext.commands.errors.PrivateMessageOnly):
            pass
        else:
            raise error
