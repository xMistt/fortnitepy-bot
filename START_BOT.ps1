$pythonVersions = 36..38
$CURRENT_PYTHON = "3.8.4"
$REQUIREMENTS = "fortnitepy","BenBotAsync","crayons","pypresence","psutil"

function Which($name) {
    if ($name) { $_input = $name }
    Get-Command $_input | Select-Object -ExpandProperty Path
}
function InstallPython
{
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/$CURRENT_PYTHON/python-$CURRENT_PYTHON.exe" -OutFile "$env:Temp/python-$CURRENT_PYTHON.exe"
    Start-Process -FilePath "$env:Temp/python-$CURRENT_PYTHON.exe" -ArgumentList "/quiet","InstallAllUsers=0","PrependPath=1","Include_test=0"
}
function GetPython
{
    $pythonExists = [bool](Get-Command "python -V" -ErrorAction SilentlyContinue)
    if ($pythonExists) {
        $finalPythonPath = which -name "python"
    }
    $pythonInstalledResult = $false
    $finalPythonPath = $null
    foreach ($path in $pythonVersions) {
        $finalPath = "\Programs\Python\Python$path-32\python.exe"
        $pythonPath = Join-Path -Path $env:LOCALAPPDATA -ChildPath $finalPath
        $result = Test-Path -Path $pythonPath
        if ($result) {
            $pythonInstalledResult = $true
            $finalPythonPath = $pythonPath
        }
        continue
    }
    if (!$pythonInstalledResult){
        Write-Host "Python not found, installing python..."
        InstallPython
    }
    return $finalPythonPath

}
$pythonPath = GetPython

foreach ($requirement in $REQUIREMENTS) {
    (& $pythonPath "-c" "import $requirement" | Set-Variable -Name output) 2>&1 | Set-Variable stdError
    if ($stdError -like "*ModuleNotFoundError*") {
        "Package not found, installing $requirement"
        & $pythonPath "-m" "pip" "install" "$requirement" | Set-Variable -Name _ 2>&1 | Set-Variable _
        "Sucesfully installed `"$requirement`""
    } elseif ($stdError -like "*Error*") {
        "Unknown error, please report the issue in the discord or open an issue on github"
        "Please provide the log file `"powershell_log.txt`""
        "Import issue caused with import `"$requirement`""
        if (!(Test-Path -Path "powershell_log.txt")) {
            New-Item "powershell_log.txt"
        }
        Set-Content "powershell_log.txt" "STDOUT:$output`nSTDERR:$stdError"
        $stdError = ""
        $output = ""
    }
}


"Running bot..."

& $pythonPath "fortnite.py"