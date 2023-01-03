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
import json

# Third party imports.
import aiofiles


class BotSettings:
    def __init__(self,
                 email: str = "",
                 password: str = "",
                 cid: str = "",
                 bid: str = "",
                 eid: str = "",
                 pickaxe_id: str = "",
                 banner: str = "",
                 banner_colour: str = "",
                 level: int = 0,
                 bp_tier: int = 0,
                 status: str = "",
                 platform: str = "",
                 debug: bool = False,
                 friend_accept: bool = True
                 ) -> None:
        self.email = email
        self.password = password
        self.cid = cid
        self.bid = bid
        self.eid = eid
        self.pickaxe_id = pickaxe_id
        self.banner = banner
        self.banner_colour = banner_colour
        self.level = level
        self.bp_tier = bp_tier
        self.status = status
        self.platform = platform
        self.debug = debug
        self.friend_accept = friend_accept

    async def load_settings_from_file(self, filename: str) -> None:
        async with aiofiles.open(filename, mode='r+') as f:
            raw = await f.read()

        data = json.loads(raw)

        self.email = data.get('email', self.email)
        self.password = data.get('password', self.password)
        self.cid = data.get('cid', self.cid)
        self.bid = data.get('bid', self.bid)
        self.eid = data.get('eid', self.eid)
        self.pickaxe_id = data.get('pickaxe_id', self.pickaxe_id)
        self.banner = data.get('banner', self.banner)
        self.banner_colour = data.get('banner_colour', self.banner_colour)
        self.level = data.get('level', self.level)
        self.bp_tier = data.get('bp_tier', self.bp_tier)
        self.status = data.get('status', self.status)
        self.platform = data.get('platform', self.platform)
        self.debug = data.get('debug', self.debug)
        self.friend_accept = data.get('friend_accept', self.friend_accept)

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "password": self.password,
            "cid": self.cid,
            "bid": self.bid,
            "eid": self.eid,
            "pickaxe_id": self.pickaxe_id,
            "banner": self.banner,
            "banner_colour": self.banner_colour,
            "level": self.level,
            "bp_tier": self.bp_tier,
            "status": self.status,
            "platform": self.platform,
            "debug": self.debug,
            "friend_accept": self.friend_accept
        }


