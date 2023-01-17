@echo off

REM Check if git is installed
git --version 2>nul
if %errorlevel% neq 0 (
    echo Git is not installed. Please install Git and try again.
    pause
    exit
)

REM Check if the current working directory contains "specific-folder"
cd | find "Synchronized-Keyboard-Replay" >nul
if %errorlevel% neq 0 (
    echo The current folder is not "Synchronized-Keyboard-Replay"
    echo You will be downloading files to the current directory: %CD%
    choice /N /C:YN /M "Do you want to continue? (Y/N)"
      if errorlevel == 2 exit
)

REM Check if the current directory is a git repository
git rev-parse --git-dir 2>nul
if %errorlevel% neq 0 (
    REM Initialize git repository
    git init
)

REM Check if the remote repository is already set
git remote -v | find "origin" > nul
if %errorlevel% neq 0 (
    REM Set the remote repository
    git remote add origin https://github.com/El-Bad/Synchronized-Keyboard-Replay.git
)

REM Pull the latest version from the remote repository
git add *
git stash
git pull origin main

if %errorlevel% neq 0 (
    echo An error occurred while pulling from the remote repository. Exiting...
    pause
    exit
)

echo Update complete!
pause
