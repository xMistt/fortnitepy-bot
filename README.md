# PartyBot (previously fortnitepy-bot)
A fortnite XMPP bot coded in Python with party capabilites.

## Discord Support
<a href="https://discord.gg/8heARRB"><img src="https://discordapp.com/api/guilds/624635034225213440/widget.png?style=banner2"></a>

## How do I get started?

* Install [Python 3.6](https://www.python.org/downloads/release/python-360/ "Python 3.6 Download") (suggested, any 3.x version *should* work, **APART FROM 3.8 DO NOT USE 3.8 OR ELSE YOU'LL GET A LOT OF ERRORS**.)


* Then, if you're on Windows run ``INSTALL PACKAGES.bat``. Any other OSes, these commands into terminal.
```
python3 -m pip install -U -r requirements.txt
```

Then fill out ``config.json`` with your configuration & run the fortnite.py file!

## Commands
For a list of commands, <a href="https://github.com/xMistt/fortnitepy-bot/wiki/Commands">click here.</a>

## Config Documentation
```
"email": "",                                                - The bot accounts email.
"password": "",                                             - The bot accounts password.
"cid": "CID_313_Athena_Commando_M_KpopFashion",             - The skin that the bot wears when it joins.
"bid": "BID_138_Celestial",                                 - The backpack that the bot wears when it joins.
"eid": "EID_Floss",                                         - The emote that the bot does when it joins.
"banner": "otherbanner28",                                  - The banner icon the bot uses.
"banner_colour": "defaultcolor15",                          - The colour of the banner icon.
"level": 100,                                               - Sets the clients level.
"bp_tier": 999999999,                                       - Sets the clients battle pass tier.
"status": "Created by xMistt, enjoy! <3",                   - Sets the clients presence.
"platform": "AND",                                          - Sets the clients platform seen in the lobby.
"debug": false,                                             - If you don't know what this means, ignore it.
"friendaccept": true                                        - If the bot will accept every friend request.
```

If you need help with ``!variants``, check out the variants wiki page: https://github.com/xMistt/fortnitepy-bot/wiki/Variants Any further help you need, feel free to join our discord support server.

## When I start my bot, it asks for for an exchange code?
As of 27th January, when you start your bot, it may ask you for an exchange code. Here is an FAQ provided by Terbau.

**What is an exchange code?**
> An exchange code is a one time usable code that can be used to log into your account. The code expires after 5 minutes. Never share this code with anyone!

**How can I get an exchange code for my account?**
> You can get an exchange code by clicking the link below, logging in and then copying the visible code. You can generate a new exchange code by refreshing the page if needed.<br>
> https://www.epicgames.com/id/logout?lang=en-US&redirectUrl=https%3A//www.epicgames.com/id/login%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fexchange&lang=en-US

## How can I contribute?
Fork this repo, add/fix what you want to do and then submit a pull request back. Please do note, whatever you're writing must comply with PEP 8 Styling, more information on this styling can be found here https://www.python.org/dev/peps/pep-0008

## Commons Clause License
By downloading this, you agree to the Commons Clause license and that you're not allowed to sell this repository or any code from this repository. For more info see https://commonsclause.com/.
