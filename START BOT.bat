@ECHO OFF
:: Check for Python Installation
py -3 --version 2>NUL
if errorlevel 1 goto errorNoPython

:: Reaching here means Python is installed.
IF EXIST "python-3.6.0-amd64.exe" (
    del "python-3.6.0-amd64.exe"
)

cls
TITLE PartyBot Official ^| github.com/xMistt/fortnitepy-bot
@ECHO ON
py fortnite.py
cmd /k

:: Once done, exit the batch file -- skips executing the errorNoPython section
goto:eof

:errorNoPython
TITLE PartyBot^: Error
ECHO Error^: Python not installed or has not been added to PATH.

IF EXIST "python-3.7.0-amd64.exe" (
    echo Python Installer is already installed, install and/or add Python to PATH
) ELSE (
    ECHO Installing Python Installer now, this will take a minute or 2.
    powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.7.0/python-3.7.0-amd64.exe', 'python-3.7.0-amd64.exe')"
    powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.7.0/python-3.7.0-amd64.exe -OutFile python-3.7.0-amd64.exe"   
    ECHO Python Installer is now installed, install and/or add Python to PATH.
)
cmd /k