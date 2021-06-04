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

from .errors import MissingDeviceAuth

from typing import Optional, Union

import json

import aiofiles


class DeviceAuth:
    def __init__(self,
                 device_id: Optional[str] = None,
                 account_id: Optional[str] = None,
                 secret: Optional[str] = None,
                 **kwargs
                 ) -> None:
        self.device_id = device_id
        self.account_id = account_id
        self.secret = secret


class DeviceAuths:
    def __init__(self, filename: str) -> None:
        self.device_auth = None
        self.filename = filename

    async def load_device_auths(self) -> None:
        try:
            async with aiofiles.open(self.filename, mode='r') as fp:
                data = await fp.read()
                raw_device_auths = json.loads(data)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            raw_device_auths = {}

        if 'device_id' not in raw_device_auths or \
            'account_id' not in raw_device_auths or \
                'secret' not in raw_device_auths:
            raise MissingDeviceAuth('Missing required device auth key.')

        self.device_auth = DeviceAuth(
            device_id=raw_device_auths.get('device_id'),
            account_id=raw_device_auths.get('account_id'),
            secret=raw_device_auths.get('secret')
        )

    async def save_device_auths(self) -> None:
        async with aiofiles.open(self.filename, mode='w') as fp:
            await fp.write(json.dumps(
                {
                    "account_id": self.device_auth.account_id,
                    "device_id": self.device_auth.device_id,
                    "secret": self.device_auth.secret
                },
                sort_keys=False,
                indent=4
            ))

    def set_device_auth(self, **kwargs) -> None:
        self.device_auth = DeviceAuth(
            **kwargs
        )

    def get_device_auth(self) -> Union[DeviceAuth, None]:
        return self.device_auth
