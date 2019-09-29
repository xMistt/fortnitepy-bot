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
"email": "",                                                - The bot account's email.
"password": "",                                             - The bot account's password.
"netcl": "8371783",                                         - Fortnite party netcl.
"cid": "CID_313_Athena_Commando_M_KpopFashion",             - The skin that the bot wears when it joins.
"bid": "BID_138_Celestial",                                 - The backpack that the bot wears when it joins.
"eid": "EID_DeepDab",                                       - The emote that the bot does when it joins.
"banner": "otherbanner28",                                  - The banner icon the bot uses.
"banner_colour": "defaultcolor15",                          - The colour of the banner icon.
"level": "100",                                             - Sets the clients level. (seen on it's banner)
"bp_tier": 999999999,                                       - Sets the clients battle pass tier.
"self_xp_boost": 999999999,                                 - Sets the clients xp boost. 
"friend_xp_boost": 999999999,                               - Sets the clients friend xp boost.
"friendaccept": "true"                                      - If the bot will accept every friend request.
```

## Commands
```
* !skin - Makes the account wear the skin specified.        Usage: !skin <skin name>
* CID_ - Makes the account wear the CID specified.          Usage: <CID>
* EID_ - Makes the account do the emote specified.          Usage: <EID>
* BID_ - Makes the account wear the BID specified.          Usage: <BID>
* PICKAXE_ID_ - Equips the pickaxe specified.               Usage: <PICKAXE_ID>
* !purpleskull - Shortcut for purple skull trooper.         Usage: !purpleskull
* !variants - Sets the skin variant.                        Usage: !variants <CID> <variant_type> <integer>
* !checkeredrenegade - Shortcut for the checkered renegade. Usage: !checkeredrenegade
* !banner - Set's the accounts banner, colour & level.      Usage: !banner <banner> <color> <level>
* !stop - Stops the bot's emote if it's emoting.            Usage: !stop
* !ready - Makes the bot ready up.                          Usage: !ready
* !unready - Makes the bot unready.                         Usage: !unready
* !bp - Changes the bot's battlepass & xp boosts.           Usage: !bp <TIER> <XP BOOST> <FRIEND XP BOOST>
* !help - Shows a list of commands. (like this)             Usage: !help
```

If you need help with ``!variants``, check out the variants wiki page: https://github.com/xMistt/fortnitepy-bot/wiki/Variants Any further help you need, feel free to join our discord support server.

## How can I contribute?
Fork this repo, add/fix what you want to do and then submit a pull request back.

