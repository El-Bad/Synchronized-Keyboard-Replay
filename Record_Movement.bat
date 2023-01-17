@echo off

setlocal

REM Function to check the version of a command
:CheckCommandVersion
set command=%1
for /f "tokens=2 delims=." %%a in ('%command% --version 2^>nul') do (
    set version=%%a
    if defined version exit /b
)

REM Check the version of Python
call :CheckCommandVersion python
if not defined version (
    call :CheckCommandVersion python3
)

REM Check if Python version is greater than 3
if not defined version (
    echo Python is not installed. Please install Python and try again.
    pause
    exit
)

if %version% LSS 3 (
    echo Python version is too old. Please install a version higher than 3 and try again.
    pause
    exit
)

REM Check if the requirements are already installed
if not exist requirements.txt (
    echo Cannot find requirements.txt
    pause
    exit
)

REM pip install -r requirements.txt

for /f "tokens=*" %%i in (requirements.txt) do (
    pip list | find "%%i" > nul
    if %errorlevel% neq 0 (
        REM Install the requirement
        pip install %%i
    )
)

if %errorlevel% neq 0 (
    echo An error occurred while running the command: %command%
    echo Error code: %errorlevel%
    pause
    exit
)

REM Run the Python script
start %command%w gui.pyw
