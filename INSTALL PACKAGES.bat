@echo off
:: Check for Python Installation
py -3 --version 2>NUL
if errorlevel 1 goto errorNoPython

:: Reaching here means Python is installed.
IF EXIST "python-3.6.0-amd64.exe" (
    del "python-3.6.0-amd64.exe"
)

cls

ECHO Installing the required packages for the bot!
TIMEOUT 3

py -3 -m pip install -U -r requirements.txt

ECHO Done! Now run START BOT.bat
PAUSE

:: Once done, exit the batch file -- skips executing the errorNoPython section
goto:eof

:errorNoPython
echo Error^: Python not installed or not added to PATH.
:: set mypath=%cd%
:: bitsadmin.exe /transfer "InstallPython" https://www.python.org/ftp/python/3.6.0/python-3.6.0-amd64.exe %mypath%\PythonInstaller.exe

IF EXIST "python-3.6.0-amd64.exe" (
    echo Python Installer is already installed, install and/or add Python to PATH
) ELSE (
    echo Installing Python Installer now, this will take a minute or 2.
    powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.6.0/python-3.6.0-amd64.exe', 'python-3.6.0-amd64.exe')"
    powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.6.0/python-3.6.0-amd64.exe -OutFile python-3.6.0-amd64.exe"   
    echo Python Installer is now installed, install and/or add Python to PATH.
)

cmd /k