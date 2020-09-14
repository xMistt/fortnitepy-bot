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

# System imports.
from typing import Optional

import json

# Third party imports.
import aiofiles


class DeviceAuth:
    def __init__(self,
                 email: Optional[str] = None,
                 device_id: Optional[str] = None,
                 account_id: Optional[str] = None,
                 secret: Optional[str] = None
                 ) -> None:
        self.email = email
        self.device_id = device_id
        self.account_id = account_id
        self.secret = secret


class DeviceAuths:
    def __init__(self, filename: str) -> None:
        self.device_auths = {}
        self.filename = filename

    async def load_device_auths(self) -> None:
        async with aiofiles.open(self.filename, mode='r') as f:
            raw = await f.read()

        data = json.loads(raw)

        for key, value in data.items():
            self.device_auths[key] = DeviceAuth(
                email=key,
                device_id=value['device_id'],
                account_id=value['account_id'],
                secret=value['secret']
            )

    async def save_device_auth(self, device_auth: DeviceAuth) -> None:
        async with aiofiles.open(self.filename, mode='r+') as f:
            raw_input = await f.read()

        data = json.loads(raw_input)

        data[device_auth.email] = {
            "device_id": device_auth.device_id,
            "account_id": device_auth.account_id,
            "secret": device_auth.secret
        }

        parsed_output = json.dumps(
            data,
            sort_keys=False,
            indent=4
        )

        async with aiofiles.open(self.filename, mode='w+') as f:
            await f.write(parsed_output)

    def get_device_auth(self, email: str) -> DeviceAuth:
        return self.device_auths[email] if email in self.device_auths else DeviceAuth()

