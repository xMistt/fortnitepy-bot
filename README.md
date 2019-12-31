-- BIG credits to xMistt for the source code and inspiration of this bot.

# fortnitepy-bot
A fortnite XMPP bot coded in Python with party capabilites.

## How do I get started?

* Install [Python 3.6](https://www.python.org/downloads/release/python-360/ "Python 3.6 Download") (suggested, any 3.x version *should* work, **APART FROM 3.8 DO NOT USE 3.8 OR ELSE YOU'LL GET A LOT OF ERRORS**.)


* Then run ``INSTALL PACKAGES.bat`` if you're on Windows or type these commands into console if you're on macOS / linux:
```
python3 -m pip install -U fortnitepy
python3 -m pip install -U aiohttp
python3 -m pip install -U colorama
python3 -m pip install -U BenBotAsync==1.0.1
```

Then fill out ``config.json`` with your configuration & run the fortnite.py file!

## Commands
For a list of commands, <a href="https://github.com/KaosDrip/fortnitepy-bot/wiki/Commands">click here.</a>

## Config Documentation
```
"email": "",                                                - The bot accounts email.
"password": "",                                             - The bot accounts password.
"cid": "CID_028_Athena_Commando_F",                         - The skin that the bot wears when it joins.
"bid": "BID_004_BlackKnight",                               - The backpack that the bot wears when it joins.
"eid": "EID_Clapperboard",                                  - The emote that the bot does when it joins.
"pid": "Pickaxe_Lockjaw",                                   - The pickaxe that the bot has equiped.
"banner": "otherbanner28",                                  - The banner icon the bot uses.
"banner_colour": "defaultcolor15",                          - The colour of the banner icon.
"level": "100",                                             - Sets the clients level.
"bp_tier": 999999999,                                       - Sets the clients battle pass tier.
"status": "Created by xMistt, enjoy! <3",                   - Sets the clients presence.
"platform": "AND",                                          - Sets the clients platform seen in the lobby.
 ** ALL Platforms: **
 * XBL
 * NTS
 * PSN
 * WIN
 * IOS
 * AND
"friendaccept": "True",                                     - If the bot will accept every friend request.
"joinoninvite": "True",                                     - If the bot will join every party they are invited to.
"AdminPassword": "0001",                                    - The password to use to add themselves the the admin list.
"FullAccess": [                                             \
    "(Your Epic Name)"                                       - Decides who has access to EVERY command.
],                                                          /
"BlockList": [                                              \
    "(User's Epic Name)"                                     - Decides who doesn't have access to ANY command.
]                                                           /
```   

## Creative Commons License
By downloading this, you agree to the Creative Commons license and that you're not allowed to sell this repository or any code from this repository. For more info see https://commonsclause.com/.
