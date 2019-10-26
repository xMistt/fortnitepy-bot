@echo off
ECHO Installing the required packages for the bot!
TIMEOUT 3

python3 -m pip install -U fortnitepy
python3 -m pip install -U aiohttp
python3 -m pip install -U colorama
python3 -m pip install -U BenBot-async


ECHO Done! Now run START BOT.bat
PAUSE

