@echo off
ECHO Installing the required packages for the bot!
TIMEOUT 3

py -3 -m pip install -U -r requirements.txt

ECHO Done! Now run START BOT.bat
PAUSE

