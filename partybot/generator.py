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

Software: DeviceAuthGenerator

License: Apache 2.0 Modified.
"""

import asyncio
import webbrowser
import json
import platform
import os
import sys

import aiohttp

# "Constants" ? I don't know.
DAUNTLESS_TOKEN = "YjA3MGYyMDcyOWY4NDY5M2I1ZDYyMWM5MDRmYzViYzI6SEdAWEUmVEdDeEVKc2dUIyZfcDJdPWFSbyN+Pj0+K2M2UGhSKXpYUA=="
SWITCH_TOKEN = "NTIyOWRjZDNhYzM4NDUyMDhiNDk2NjQ5MDkyZjI1MWI6ZTNiZDJkM2UtYmY4Yy00ODU3LTllN2QtZjNkOTQ3ZDIyMGM3="
IOS_TOKEN = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="


class EpicUser:
    def __init__(self, data: dict = {}):
        self.raw = data

        self.access_token = data.get('access_token', '')
        self.expires_in = data.get('expires_in', 0)
        self.expires_at = data.get('expires_at', '')
        self.token_type = data.get('token_type', '')
        self.refresh_token = data.get('refresh_token', '')
        self.refresh_expires = data.get('refresh_expires', '')
        self.refresh_expires_at = data.get('refresh_expires_at', '')
        self.account_id = data.get('account_id', '')
        self.client_id = data.get('client_id', '')
        self.internal_client = data.get('internal_client', False)
        self.client_service = data.get('client_service', '')
        self.display_name = data.get('displayName', '')
        self.app = data.get('app', '')
        self.in_app_id = data.get('in_app_id', '')


class EpicGenerator:
    def __init__(self) -> None:
        self.http = None

        self.access_token = ""
        self.user_agent = f"DeviceAuthGenerator/1.0.0 {platform.system()}/{platform.version()}"

    async def generate_device_auths(self) -> None:
        self.http = aiohttp.ClientSession(
            headers={
                'User-Agent': self.user_agent
            }
        )

        self.access_token = await self.get_access_token()

        device_code = await self.create_device_code()
        webbrowser.open(f"https://www.epicgames.com/activate?userCode={device_code[0]}", new=1)
        user = await self.wait_for_device_code_completion(code=device_code[1])
        device_auths = await self.create_device_auths(user)

        await self.http.close()

        return device_auths

    async def get_access_token(self) -> str:
        async with self.http.request(
                method="POST",
                url="https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"basic {DAUNTLESS_TOKEN}"
                },
                data={
                    "grant_type": "client_credentials",
                }
        ) as request:
            data = await request.json()

        return data['access_token']

    async def create_device_code(self) -> tuple:
        async with self.http.request(
                method="POST",
                url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/deviceAuthorization",
                headers={
                    "Authorization": f"bearer {self.access_token}",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
        ) as request:
            data = await request.json()

        return data['user_code'], data['device_code']

    async def wait_for_device_code_completion(self, code: str) -> EpicUser:
        while True:
            async with self.http.request(
                method="POST",
                url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
                headers={
                    "Authorization": f"basic {SWITCH_TOKEN}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "device_code",
                    "device_code": code
                }
            ) as request:
                token = await request.json()

                if request.status == 200:
                    break
                else:
                    if token['errorCode'] == 'errors.com.epicgames.account.oauth.authorization_pending':
                        pass
                    elif token['errorCode'] == 'errors.com.epicgames.not_found':
                        pass
                    else:
                        print(json.dumps(token, sort_keys=False, indent=4))

                await asyncio.sleep(5)

        async with self.http.request(
            method="GET",
            url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/exchange",
            headers={
                "Authorization": f"bearer {token['access_token']}"
            }
        ) as request:
            exchange = await request.json()

        async with self.http.request(
            method="POST",
            url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
            headers={
                "Authorization": f"basic {IOS_TOKEN}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={
                "grant_type": "exchange_code",
                "exchange_code": exchange['code']
            }
        ) as request:
            auth_information = await request.json()

            return EpicUser(
                data=auth_information
            )

    async def create_device_auths(self, user: EpicUser) -> dict:
        async with self.http.request(
            method="POST",
            url="https://account-public-service-prod.ol.epicgames.com/"
                f"account/api/public/account/{user.account_id}/deviceAuth",
            headers={
                "Authorization": f"bearer {user.access_token}",
                "Content-Type": "application/json"
            }
        ) as request:
            data = await request.json()

        return {
            "device_id": data['deviceId'],
            "account_id": data['accountId'],
            "secret": data['secret'],
            "user_agent": data['userAgent'],
            "created": {
                "location": data['created']['location'],
                "ip_address": data['created']['ipAddress'],
                "datetime": data['created']['dateTime']
            }
        }