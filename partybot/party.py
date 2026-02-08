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
import asyncio
import datetime
import random

from typing import Optional, Union

# Third party imports.
import rebootpy
import aiohttp
import crayons

from rebootpy.ext import commands


class PartyCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.name = 'Party'

    @commands.dm_only()
    @commands.command(
        description="[Party] Sets the banner of the self.bot.",
        help="Sets the banner of the self.bot.\n"
             "Example: !banner BRSeason01 defaultcolor15 100",
        usage="!banner <icon> <colour> <banner_level>"
    )
    async def banner(self, ctx: rebootpy.ext.commands.Context,
                     icon: Optional[str] = None,
                     colour: Optional[str] = None,
                     banner_level: Optional[int] = None
                     ) -> None:
        await self.bot.party.me.set_banner(icon=icon, color=colour, season_level=banner_level)

        await ctx.send(f'Banner set to: {icon} with {colour} at level {banner_level}.')
        print(self.bot.message % f"Banner set to: {icon} with {colour} at level {banner_level}.")

    @commands.dm_only()
    @commands.command(
        description="[Party] Sets the readiness of the client to ready.",
        help="Sets the readiness of the client to ready.\n"
             "Example: !ready",
        usage="!ready"
    )
    async def ready(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_ready(rebootpy.ReadyState.READY)
        await ctx.send('Ready!')

    @commands.dm_only()
    @commands.command(
        aliases=['sitin'],
        description="[Party] Sets the readiness of the client to unready.",
        help="Sets the readiness of the client to unready.\n"
             "Example: !unready",
        usage="!unready"
    )
    async def unready(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_ready(rebootpy.ReadyState.NOT_READY)
        await ctx.send('Unready!')

    @commands.dm_only()
    @commands.command(
        description="[Party] Sets the readiness of the client to SittingOut.",
        help="Sets the readiness of the client to SittingOut.\n"
             "Example: !sitout",
        usage="!sitout"
    )
    async def sitout(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_ready(rebootpy.ReadyState.SITTING_OUT)
        await ctx.send('Sitting Out!')

    @commands.dm_only()
    @commands.command(
        description="[Party] Sets the battlepass info of the self.bot.",
        help="Sets the battlepass info of the self.bot.\n"
             "Example: !bp 100",
        usage="!bp <tier>"
    )
    async def bp(self, ctx: rebootpy.ext.commands.Context, tier: int) -> None:
        await self.bot.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier,
        )

        await ctx.send(f'Set battle pass tier to {tier}.')

    @commands.dm_only()
    @commands.command(
        description="[Party] Sets the level of the self.bot.",
        help="Sets the level of the self.bot.\n"
             "Example: !level 999",
        usage="!level <banner_level>"
    )
    async def level(self, ctx: rebootpy.ext.commands.Context, banner_level: int) -> None:
        await self.bot.party.me.set_banner(
            season_level=banner_level
        )

        await ctx.send(f'Set level to {level}.')

    @commands.dm_only()
    @commands.command(
        description="[Party] Sends message to party chat with the given content.",
        help="Sends message to party chat with the given content.\n"
             "Example: !echo i cant fix the fucking public lobby bots",
        usage="!echo <content>"
    )
    async def echo(self, ctx: rebootpy.ext.commands.Context, *, content: str) -> None:
        await self.bot.party.send(content)
        await ctx.send('Sent message to party chat.')

    @commands.dm_only()
    @commands.command(
        description="[Party] Leaves the current party.",
        help="Leaves the current party.\n"
             "Example: !leave",
        usage="!leave"
    )
    async def leave(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.set_emote('EID_Wave')
        await asyncio.sleep(2)
        await self.bot.party.me.leave()
        await ctx.send('Bye!')

        print(self.bot.message % f'Left the party as I was requested.')

    @commands.dm_only()
    @commands.command(
        description="[Party] Kicks the inputted user.",
        help="Kicks the inputted user.\n"
             "Example: !kick Cxnyaa",
        usage="!kick <epic_username>"
    )
    async def kick(self, ctx: rebootpy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        if epic_username is None:
            user = await self.bot.fetch_user(ctx.author.display_name)
            member = self.bot.party.get_member(user.id)
        else:
            user = await self.bot.fetch_user(epic_username)
            member = self.bot.party.get_member(user.id)

        if member is None:
            await ctx.send("Failed to find that user, are you sure they're in the party?")
        else:
            try:
                await member.kick()
                await ctx.send(f"Kicked user: {member.display_name}.")
                print(self.bot.message % f"Kicked user: {member.display_name}")
            except rebootpy.errors.Forbidden:
                await ctx.send(f"Failed to kick {member.display_name}, as I'm not party leader.")
                print(crayons.red(self.bot.message % f"[ERROR] "
                                  "Failed to kick member as I don't have the required permissions."))

    @commands.dm_only()
    @commands.command(
        aliases=['unhide'],
        description="[Party] Promotes the defined user to party leader. If friend is left blank, "
                    "the message author will be used.",
        help="Promotes the defined user to party leader. If friend is left blank, the message author will be used.\n"
             "Example: !promote Terbau",
        usage="!promote <epic_username>"
    )
    async def promote(self, ctx: rebootpy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        if epic_username is None:
            user = await self.bot.fetch_user(ctx.author.display_name)
            member = self.bot.party.get_member(user.id)
        else:
            user = await self.bot.fetch_user(epic_username)
            member = self.bot.party.get_member(user.id)

        if member is None:
            await ctx.send("Failed to find that user, are you sure they're in the party?")
        else:
            try:
                await member.promote()
                await ctx.send(f"Promoted user: {member.display_name}.")
                print(self.bot.message % f"Promoted user: {member.display_name}")
            except rebootpy.errors.Forbidden:
                await ctx.send(f"Failed topromote {member.display_name}, as I'm not party leader.")
                print(crayons.red(self.bot.message % f"[ERROR] "
                                  "Failed to promote member as I don't have the required permissions."))

    @commands.dm_only()
    @commands.command(
        description="[Party] Sets the lobbies selected playlist.",
        help="Sets the lobbies selected playlist.\n"
             "Example: !playlist_id Playlist_Tank_Solo",
        usage="!playlist_id <playlist_>"
    )
    async def playlist_id(self,
                          ctx: rebootpy.ext.commands.Context,
                          playlist_: str
                          ) -> None:
        try:
            await self.bot.party.set_playlist(playlist=playlist_)
            await ctx.send(f'Gamemode set to {playlist_}')
        except rebootpy.errors.Forbidden:
            await ctx.send(
                f"Failed to set gamemode to {playlist_}, as I'm not party leader."
            )
            print(
                crayons.red(
                    self.bot.message % f"[ERROR] "
                    "Failed to set gamemode as I don't have the required permissions."
                )
            )

    @commands.dm_only()
    @commands.command(
        description="[Party] Sets the parties current privacy.",
        help="Sets the parties current privacy.\n"
             "Example: !privacy private",
        usage="!privacy <privacy_type>"
    )
    async def privacy(self, ctx: rebootpy.ext.commands.Context, privacy_type: str) -> None:
        try:
            if privacy_type.lower() == 'public':
                await self.bot.party.set_privacy(rebootpy.PartyPrivacy.PUBLIC)
            elif privacy_type.lower() == 'private':
                await self.bot.party.set_privacy(rebootpy.PartyPrivacy.PRIVATE)
            elif privacy_type.lower() == 'friends':
                await self.bot.party.set_privacy(rebootpy.PartyPrivacy.FRIENDS)
            elif privacy_type.lower() == 'friends_allow_friends_of_friends':
                await self.bot.party.set_privacy(rebootpy.PartyPrivacy.FRIENDS_ALLOW_FRIENDS_OF_FRIENDS)
            elif privacy_type.lower() == 'private_allow_friends_of_friends':
                await self.bot.party.set_privacy(rebootpy.PartyPrivacy.PRIVATE_ALLOW_FRIENDS_OF_FRIENDS)

            await ctx.send(f'Party privacy set to {self.bot.party.privacy}.')
            print(self.bot.message % f'Party privacy set to {self.bot.party.privacy}.')

        except rebootpy.errors.Forbidden:
            await ctx.send(f"Failed to set party privacy to {privacy_type}, as I'm not party leader.")
            print(crayons.red(self.bot.message % f"[ERROR] "
                              "Failed to set party privacy as I don't have the required permissions."))

    @commands.dm_only()
    @commands.command(
        description="[Party] Sets the parties custom matchmaking code.",
        help="Sets the parties custom matchmaking code.\n"
             "Example: !matchmakingcode solo123",
        usage="!matchmakingcode <custom_matchmaking_key>"
    )
    async def matchmakingcode(self, ctx: rebootpy.ext.commands.Context, *, custom_matchmaking_key: str) -> None:
        await self.bot.party.set_custom_key(
            key=custom_matchmaking_key
        )

        await ctx.send(f'Custom matchmaking code set to: {custom_matchmaking_key}')

    @commands.dm_only()
    @commands.command(
        description="[Party] Sets the client to the \"In Match\" state.",
        help="Sets the client to the \"In Match\" state.\n"
             "Example: !match",
        usage="!match"
    )
    async def match(self, ctx: rebootpy.ext.commands.Context, players: Union[str, int] = 0,
                    match_time: int = 0) -> None:
        await self.bot.party.me.set_in_match()
        await ctx.send('Set state to in match.')

    @commands.dm_only()
    @commands.command(
        description="[Party] Sets the client to normal pre-game lobby state.",
        help="Sets the client to normal pre-game lobby state.\n"
             "Example: !lobby",
        usage="!lobby"
    )
    async def lobby(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.party.me.clear_in_match()

        await ctx.send('Set state to the pre-game lobby.')

    @commands.dm_only()
    @commands.command(
        description="[Party] Joins the party of the defined friend. If friend is left blank, "
                    "the message author will be used.",
        help="Joins the party of the defined friend.\n"
             "Example: !join Terbau",
        usage="!join <epic_username>"
    )
    async def join(self, ctx: rebootpy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        if epic_username is None:
            epic_friend = self.bot.get_friend(ctx.author.id)
        else:
            user = await self.bot.fetch_user(epic_username)

            if user is not None:
                epic_friend = self.bot.get_friend(user.id)
            else:
                epic_friend = None
                await ctx.send(f'Failed to find user with the name: {epic_username}.')

        if isinstance(epic_friend, rebootpy.Friend):
            try:
                await epic_friend.join_party()
                await ctx.send(f'Joined the party of {epic_friend.display_name}.')
            except rebootpy.errors.Forbidden:
                await ctx.send('Failed to join party since it is private.')
            except rebootpy.errors.PartyError:
                await ctx.send('Party not found, are you sure Fortnite is open?')
        else:
            await ctx.send('Cannot join party as the friend is not found.')

    @commands.dm_only()
    @commands.command(
        description="[Party] Changes the current playlist by playlist name.",
        help="Changes the current playlist by playlist name.\n"
             "Example: !playlist Blitz",
        usage="!playlist <playlist_name>"
    )
    async def playlist(self, ctx: rebootpy.ext.commands.Context, *, playlist_name: str) -> None:
        try:
            playlists = await self.bot.fortnite_api.get_playlists()
            playlist = next(
                (
                    p for p in playlists if
                    playlist_name.lower() in p.name.lower()
                ),
                None
            )

            if playlist:
                await self.bot.party.set_playlist(playlist=playlist.id)
                await ctx.send(f'Playlist set to {playlist.id}')
                print(self.bot.message % f'Playlist set to {playlist.id}')
            else:
                await ctx.send('Failed to find playlist.')
                print(self.bot.message % 'Failed to find playlist.')

        except rebootpy.errors.Forbidden:
            await ctx.send(
                f"Failed to set playlist to {playlist_name}, as I'm not party leader."
            )
            print(
                crayons.red(
                    self.bot.message % f"[ERROR] "
                    "Failed to set playlist as I don't have the required permissions."
                )
            )

    @commands.dm_only()
    @commands.command(
        name="invite",
        description="[Party] Invites the defined friend to the party. If friend is left blank, "
                    "the message author will be used.",
        help="Invites the defined friend to the party.\n"
             "Example: !invite Terbau"
    )
    async def _invite(self, ctx: rebootpy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        if epic_username is None:
            epic_friend = self.bot.get_friend(ctx.author.id)
        else:
            user = await self.bot.fetch_user(epic_username)

            if user is not None:
                epic_friend = self.bot.get_friend(user.id)
            else:
                epic_friend = None
                await ctx.send(f'Failed to find user with the name: {epic_username}.')
                print(crayons.red(self.bot.message % f"[ERROR] "
                                  f"Failed to find user with the name: {epic_username}."))

        if isinstance(epic_friend, rebootpy.Friend):
            try:
                await epic_friend.invite()
                await ctx.send(f'Invited {epic_friend.display_name} to the party.')
                print(self.bot.message % f"[ERROR] Invited {epic_friend.display_name} to the party.")
            except rebootpy.errors.PartyError:
                await ctx.send('Failed to invite friend as they are either already in the party or it is full.')
                print(crayons.red(self.bot.message % f"[ERROR] "
                                  "Failed to invite to party as friend is already either in party or it is full."))
        else:
            await ctx.send('Cannot invite to party as the friend is not found.')
            print(crayons.red(self.bot.message % f"[ERROR] "
                              "Failed to invite to party as the friend is not found."))

    @commands.dm_only()
    @commands.command(
        description="[Party] Hides everyone in the party except for the bot but if a player is specified, "
                    "that specific player will be hidden.",
        help="Hides members of the party.\n"
             "Example: !hide",
        usage="!hide <party_member>"
    )
    async def hide(self, ctx: rebootpy.ext.commands.Context, party_member: Optional[str] = None) -> None:
        if self.bot.party.me.leader:
            if party_member is not None:
                user = await self.bot.fetch_user(party_member)
                member = self.bot.party.get_member(user.id)

                if member is not None:
                    raw_squad_assignments = self.bot.party.meta.get_prop(
                        'Default:RawSquadAssignments_j'
                    )["RawSquadAssignments"]

                    for player in raw_squad_assignments:
                        if player['memberId'] == member.id:
                            raw_squad_assignments.remove(player)

                    await self.bot.set_and_update_party_prop(
                        'Default:RawSquadAssignments_j', {
                            'RawSquadAssignments': raw_squad_assignments
                        }
                    )
                else:
                    await ctx.send(f'Failed to find user with the name: {party_member}.')
                    print(crayons.red(self.bot.message % f"[ERROR] "
                                      f"Failed to find user with the name: {party_member}."))
            else:
                await self.bot.set_and_update_party_prop(
                    'Default:RawSquadAssignments_j', {
                        'RawSquadAssignments': [{'memberId': self.bot.user.id, 'absoluteMemberIdx': 1}]
                    }
                )

                await ctx.send('Hid everyone in the party. Use !unhide if you want to unhide everyone.'
                               '\nReminder: Crashing lobbies is bannable offense which will result in a permanent ban.')
                print(self.bot.message % f'Hid everyone in the party.')
        else:
            await ctx.send("Failed to hide everyone, as I'm not party leader")
            print(crayons.red(self.bot.message % f"[ERROR] "
                              "Failed to hide everyone as I don't have the required permissions."))
