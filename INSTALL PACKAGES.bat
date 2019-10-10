@echo off
ECHO Installing the required packages for the bot!
TIMEOUT 3

py -3 -m pip install -U git+https://github.com/Terbau/fortnitepy.git@dev
py -3 -m pip install -U aiohttp

ECHO Done! Now run START BOT.bat
PAUSE

