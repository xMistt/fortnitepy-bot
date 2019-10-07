# fortnitepy-bot
A fortnite XAMPP bot coded in Python with party capabilites.

## Discord Support
<a href="https://discord.gg/9y9Sqt2"><img src="https://i.imgur.com/wWTDpdl.png"></a>

## How do I get started?

* Install [Python 3.6](https://www.python.org/downloads/release/python-360/ "Python 3.6 Download") (suggested, any 3.x version *should* work)

* Then open command prompt/terminal and enter these commands:
```
# windows
py -3 -m pip install -U fortnitepy
py -3 -m pip install -U aiohttp

# linux / macOS
python3 -m pip install -U fortnitepy
python3 -m pip install -U aiohttp
```

Then fill out ``config.json`` with your configuration & run the fortnite.py file!


## Config Documentation
```
"email": "",                                                                - The bot account's email.
"password": "",                                                             - The bot account's password.
"netcl": "8371783",                                                         - Fortnite party netcl.
"cid": "CID_313_Athena_Commando_M_KpopFashion",                             - The skin that the bot wears when it joins.
"bid": "BID_138_Celestial",                                                 - The backpack that the bot wears when it joins.
"eid": "EID_DeepDab",                                                       - The emote that the bot does when it joins.
"banner": "otherbanner28",                                                  - The banner icon the bot uses.
"banner_colour": "defaultcolor15",                                          - The colour of the banner icon.
"level": "100",                                                             - Sets the clients level. (seen on it's banner)
"bp_tier": 999999999,                                                       - Sets the clients battle pass tier.
"self_xp_boost": 999999999,                                                 - Sets the clients xp boost. 
"friend_xp_boost": 999999999,                                               - Sets the clients friend xp boost.
"status": "Created by xMistt, enjoy! <3",                                   - Sets the clients presence.
"platform": "ANDROID",                                                      - Sets the clients platform seen in the lobby.
"debug": "False",                                                           - If you don't know what this means, ignore it.
"friendaccept": "true"                                                      - If the bot will accept every friend request.
```

## Commands
```
* !skin - Sets the outfit of the client using the outfits name.             Usage: !skin <skin name>
* !backpack - Sets the backpack of the client using the backpacks name.     Usage: !backpack <backpack name>
* !emote - Sets the emote of the client using the emotes name.              Usage: !emote <emote name>
* !pickaxe - Sets the pickaxe of the client using the pickaxe name.         Usage: !pickaxe <pickaxe name>
* !variants - Creates the variants list by the variants you set.            Usage: !variants <CID> <style type> <integer>
* !purpleskull - Sets the outfit of the client to Purple Skull Trooper.     Usage: !purpleskull
* !purpleportal - Sets the backpack of the client to Purple Ghost Portal.   Usage: !purpleportal
* !checkeredrenegade - Sets the outfit of the client to Checkered Renegade. Usage: !checkeredrenegade
* !banner - Sets the banner of the client.                                  Usage: !banner <icon> <colour> <level>
* CID_ - Sets the outfit of the client using CID.                           Usage: <CID>
* BID_ Sets the backpack of the client using BID.                           Usage: <BID>
* PICKAXE_ID_ - Sets the pickaxe of the client using PICKAXE_ID.            Usage: <PICKAXE_ID>
* EID_ - Sets the emote of the client using EID.                            Usage: <EID>
* !stop - Clears/stops the emote currently playing.                         Usage: !stop
* !help - Displays a link to this webpage.                                  Usage: !help
* !legacypickaxe - Sets the pickaxe of the client using Pickaxe_            Usage: !legacypickaxe <Pickaxe_>
* !ready - Sets the readiness of the client to ready.                       Usage: !ready
* !unready - Sets the readiness of the client to unready.                   Usage: !unready
* !bp - Sets the battlepass info of the client.                             Usage: !bp <level> <xp boost> <friend xp boost>
* !point - Sets pickaxe using PICKAXE_ID & does 'Point it Out'              Usage: !point <PICKAXE_ID>
* !searchpoint - Sets pickaxe using pickaxe name & does 'Point it Out'      Usage: !searchpoint <pickaxe name>
* !echo - Sends message to party chat with the given content.               Usage: !echo <message> 

```

If you need help with ``!variants``, check out the variants wiki page: https://github.com/xMistt/fortnitepy-bot/wiki/Variants Any further help you need, feel free to join our discord support server.

## How can I contribute?
Fork this repo, add/fix what you want to do and then submit a pull request back.

