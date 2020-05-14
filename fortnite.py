# -*- coding: utf-8 -*-

"""
“Commons Clause” License Condition v1.0
Copyright Oli 2020

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

Software: PartyServer

License: Apache 2.0
"""

import sanic
import datetime


def to_fortnite_iso(time: datetime.datetime) -> str:
    return f'{str(time)[slice(23)]}Z'.replace(' ', 'T')


app = sanic.Sanic(name="PartyServer")


@app.route("/account/api/oauth/token", methods=["POST", ])
async def token(request: sanic.request.Request) -> sanic.response.HTTPResponse:
    return sanic.response.json(
        {
            "access_token": "ACCESS_TOKEN",
            "expires_in": 28800,
            "expires_at": to_fortnite_iso(datetime.datetime.now() + datetime.timedelta(hours=8)),
            "token_type": "bearer",
            "refresh_token": "REFRESH_TOKEN",
            "refresh_expires": 86400,
            "refresh_expires_at": to_fortnite_iso(datetime.datetime.now() + datetime.timedelta(hours=24)),
            "account_id": "ACCOUNT_ID",
            "client_id": "CLIENT_ID",
            "internal_client": True,
            "client_service": "fortnite",
            "displayName": "Oli",
            "app": "fortnite",
            "in_app_id": "ACCOUNT_ID",
            "device_id": "DEVICE_ID"
        },
        status=200
    )


@app.route("/waitingroom/api/waitingroom")
async def waiting_room(request: sanic.request.Request) -> sanic.response.HTTPResponse:
    return sanic.response.text(
        "",
        status=204
    )


@app.route("account/api/oauth/sessions/kill", methods=["DELETE", ])
async def kill_token(request: sanic.request.Request) -> sanic.response.HTTPResponse:
    return sanic.response.text(
        "",
        status=204
    )


@app.route("/account/api/public/account/<account_id>")
async def account_lookup(request: sanic.request.Request, account_id: str) -> sanic.response.HTTPResponse:
    return sanic.response.json(
        {
            "id": account_id,
            "displayName": "Oli",
            "name": 'PARTYSERVER',
            "email": "PARTYSERVER@gmail.com",
            "failedLoginAttempts": 0,
            "lastLogin": "2020-05-11T21:14:12.698Z",
            "numberOfDisplayNameChanges": 0,
            "ageGroup": "UNKNOWN",
            "headless": False,
            "country": "GB",
            "lastName": "PARTYSERVER",
            "preferredLanguage": "en",
            "canUpdateDisplayName": True,
            "tfaEnabled": False,
            "emailVerified": True,
            "minorVerified": False,
            "minorExpected": False,
            "minorStatus": "UNKNOWN"
        },
        status=200
    )


@app.route("/account/api/public/account/<account_id>/externalAuths")
async def external_auths(request: sanic.request.Request, account_id: str) -> sanic.response.HTTPResponse:
    return sanic.response.json(
        [],
        status=200
    )


@app.route("/fortnite/api/game/v2/tryPlayOnPlatform/account/<account_id>", methods=["POST", ])
async def platform_check(request: sanic.request.Request, account_id: str) -> sanic.response.HTTPResponse:
    return sanic.response.text(
        True,
        status=200
    )


@app.route("lightswitch/api/service/bulk/status")
async def server_status(request: sanic.request.Request) -> sanic.response.HTTPResponse:
    return sanic.response.json(
        [
            {
                "serviceInstanceId": "fortnite",
                "status": "UP",
                "message": "Up",
                "maintenanceUri": None,
                "overrideCatalogIds": [
                    "a7f138b2e51945ffbfdacc1af0541053"
                ],
                "allowedActions": [
                    "PLAY",
                    "DOWNLOAD"
                ],
                "banned": False,
                "launcherInfoDTO": {
                    "appName": "Fortnite",
                    "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
                    "namespace": "fn"
                }
            }
        ],
        status=200
    )


@app.route("/fortnite/api/game/v2/enabled_features")
async def enabled_features(request: sanic.request.Request) -> sanic.response.HTTPResponse:
    return sanic.response.json(
        [],
        status=200
    )


@app.route("fortnite/api/cloudstorage/user/<account_id>")
async def cloudstorage(request: sanic.request.Request, account_id: str) -> sanic.response.HTTPResponse:
    return sanic.response.json(
        [],
        status=200
    )


@app.route("fortnite/api/game/v2/profile/<account_id>/client/<command>", methods=["POST", ])
async def commands(request: sanic.request.Request, account_id: str, command: str) -> sanic.response.HTTPResponse:
    print(request.args)

    response = {
        "profileRevision": 1,
        "profileId": request.args['profileId'][0],
        "profileChangesBaseRevision": 1,
        "profileChanges": [],
        "profileCommandRevision": 1,
        "serverTime": to_fortnite_iso(datetime.datetime.now()),
        "responseVersion": 1
    }

    if command == "RefreshExpeditions":
        return sanic.response.json(
            response,
            status=200
        )

    elif command == "QueryProfile":
        return sanic.response.json(
            response,
            status=200
        )

    elif command == "ClientQuestLogin":
        return sanic.response.json(
            response,
            status=200
        )

    else:
        raise ValueError


@app.route("/fortnite/api/calendar/v1/timeline")
async def timeline(request: sanic.request.Request) -> sanic.response.HTTPResponse:
    return sanic.json(
        {
            "channels": {
                "client-matchmaking": {
                    "states": [
                        {
                            "validFrom": "2019-01-01T20:28:47.830Z",
                            "activeEvents": [],
                            "state": {
                                "region": {
                                    "OCE": {
                                        "eventFlagsForcedOn": [
                                            "Playlist_DefaultDuo"
                                        ]
                                    },
                                    "CN": {
                                        "eventFlagsForcedOn": [
                                            "Playlist_DefaultDuo"
                                        ]
                                    },
                                    "NAE": {
                                        "eventFlagsForcedOn": [
                                            "Playlist_DefaultDuo"
                                        ]
                                    },
                                    "NAW": {
                                        "eventFlagsForcedOn": [
                                            "Playlist_DefaultDuo"
                                        ]
                                    },
                                    "EU": {
                                        "eventFlagsForcedOn": [
                                            "Playlist_DefaultDuo"
                                        ]
                                    },
                                    "BR": {
                                        "eventFlagsForcedOn": [
                                            "Playlist_DefaultDuo"
                                        ]
                                    },
                                    "ASIA": {
                                        "eventFlagsForcedOn": [
                                            "Playlist_DefaultDuo"
                                        ]
                                    },
                                    "NA": {
                                        "eventFlagsForcedOn": [
                                            "Playlist_DefaultDuo"
                                        ]
                                    }
                                }
                            }
                        }
                    ],
                    "cacheExpire": "9999-01-01T22:28:47.830Z"
                },
                "client-events": {
                    "states": [
                        {
                            "validFrom": "2019-01-01T20:28:47.830Z",
                            "activeEvents": [
                                {
                                    "eventType": "EventFlag.Season1",
                                    "activeUntil": "2019-08-08T00:00:00.000Z",
                                    "activeSince": "2019-04-23T00:00:00.000Z"
                                },
                                {
                                    "eventType": "EventFlag.LobbySeason1",
                                    "activeUntil": "2019-08-15T14:00:00.000Z",
                                    "activeSince": "2019-05-07T13:00:00.000Z"
                                }
                            ],
                            "state": {
                                "activeStorefronts": [],
                                "eventNamedWeights": {},
                                "seasonNumber": 1,
                                "seasonTemplateId": "AthenaSeason:athenaseason1",
                                "matchXpBonusPoints": 0,
                                "seasonBegin": "2019-01-01T13:00:00Z",
                                "seasonEnd": "9999-01-01T14:00:00Z",
                                "seasonDisplayedEnd": "9999-01-01T07:30:00Z",
                                "weeklyStoreEnd": "9999-01-01T00:00:00Z",
                                "stwEventStoreEnd": "9999-01-01T00:00:00.000Z",
                                "stwWeeklyStoreEnd": "9999-01-01T00:00:00.000Z",
                                "dailyStoreEnd": "9999-01-01T00:00:00Z"
                            }
                        }
                    ],
                    "cacheExpire": "9999-01-01T22:28:47.830Z"
                }
            },
            "eventsTimeOffsetHrs": 0,
            "cacheIntervalMins": 9999,
            "currentTime": "2019-07-18T18:13:41.770Z"
        },status=200
    )


app.run(host="0.0.0.0", port="8080")
