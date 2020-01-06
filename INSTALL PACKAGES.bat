@echo off
ECHO Installing the required packages for the bot!
TIMEOUT 3

py -3 -m pip install -U -r requirements.txt

ECHO Zakończono! Teraz uruchom START BOT.bat
PAUSE

