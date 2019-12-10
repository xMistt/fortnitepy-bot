@echo off
ECHO Installing the required packages for the bot!
TIMEOUT 3

py -3 -m pip install -U fortnitepy
py -3 -m pip install -U aiohttp
py -3 -m pip install -U colorama
py -3 -m pip install -U BenBotAsync==1.0.1


ECHO Done! Now run START BOT.bat
PAUSE

