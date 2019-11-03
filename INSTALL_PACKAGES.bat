@echo off
ECHO Installing the required packages for the bot!

py -m pip install -U git+https://github.com/Terbau/fortnitepy.git@dev
py -3 -m pip install -U aiohttp
py -3 -m pip install -U colorama
py -3 -m pip install -U BenBotAsync
py -3 -m pip install -U livejson

ECHO Done! Now run START BOT.bat
PAUSE

