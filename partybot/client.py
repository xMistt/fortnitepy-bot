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
import os
import sys

from typing import Optional, Union

# Third party imports.
import rebootpy
import aiohttp
import crayons

from rebootpy.ext import commands


class ClientCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.dm_only()
    @commands.command(
        description="[Client] Sends and sets the status.",
        help="Sends and sets the status.\n"
             "Example: !status Presence Unknown"
    )
    async def status(self, ctx: rebootpy.ext.commands.Context, *, content: str) -> None:
        await self.bot.set_presence(content)

        await ctx.send(f'Status set to {content}')
        print(self.bot.message % f'Status set to {content}.')

    @commands.dm_only()
    @commands.command(
        aliases=['clear'],
        description="[Client] Clears command prompt/terminal.",
        help="Clears command prompt/terminal.\n"
             "Example: !clean"
    )
    async def clean(self, ctx: rebootpy.ext.commands.Context) -> None:
        os.system('cls' if 'win' in sys.platform else 'clear')

        print(crayons.cyan(self.bot.message % f'PartyBot made by xMistt. '
                           'Massive credit to Terbau for creating the library.'))
        print(crayons.cyan(
            self.bot.message % f'Discord server: https://discord.gg/8heARRB - For support, questions, etc.'))

        await ctx.send('Command prompt/terminal cleared.')
        print(self.bot.message % f'Command prompt/terminal cleared.')

    @commands.dm_only()
    @commands.command(
        description="[Client] Sends and sets the status to away.",
        help="Sends and sets the status to away.\n"
             "Example: !away"
    )
    async def away(self, ctx: rebootpy.ext.commands.Context) -> None:
        await self.bot.set_presence(
            status=self.bot.status,
            away=rebootpy.AwayStatus.AWAY
        )

        await ctx.send('Status set to away, you can use !status to revert.')
        print(self.bot.message % f'Status set to away.')

    @commands.dm_only()
    @commands.command(
        aliases=['updates'],
        description="[Client] Sends the most recent commit/s.",
        help="Sends the most recent commit/s.\n"
             "Example: !update"
    )
    async def update(self, ctx: rebootpy.ext.commands.Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method="GET",
                url="https://api.github.com/repos/xMistt/rebootpy-bot/commits/master"
            ) as request:
                data = await request.json()

        date = rebootpy.Client.from_iso(data['commit']['committer']['date'])
        pretty_date = f'{date.day}/{date.month}/{date.year} @ {date.hour}:{date.minute}'
        commit_title = data['commit']['message'].split('\n')[0]

        await ctx.send(f"Last commit by {data['committer']['login']} made on {pretty_date}:\n"
                       f"[{data['sha'][0:7]}] {commit_title}")

        print(self.bot.message % f'Sent last commit information.')

    @commands.dm_only()
    @commands.command(
        description="[Party] Sends the defined user a friend request.",
        help="Sends the defined user a friend request.\n"
             "Example: !friend Ninja"
    )
    async def friend(self, ctx: rebootpy.ext.commands.Context, *, epic_username: str) -> None:
        user = await self.bot.fetch_user(epic_username)

        if user is not None:
            await self.bot.add_friend(user.id)
            await ctx.send(f'Sent/accepted friend request to/from {user.display_name}.')
            print(self.bot.message % f'Sent/accepted friend request to/from {user.display_name}.')
        else:
            await ctx.send(f'Failed to find user with the name: {epic_username}.')
            print(
                crayons.red(self.bot.message % f"[ERROR] Failed to find a user with the name {epic_username}."))
