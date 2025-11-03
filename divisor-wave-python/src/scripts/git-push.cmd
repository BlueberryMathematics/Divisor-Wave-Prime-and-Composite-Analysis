@echo off

REM Prompt the user for a commit message
set /p message=Enter a commit message:

REM Change the current directory to the Git repository directory
cd /d "C:\Users\Leo\Desktop\Riemann_Zeta\gitprime"

REM Open a Git Bash in the current directory
start "" "C:\Program Files\Git\git-bash.exe" --cd-to-home

REM Run the necessary Git commands
git status
git pull
git add .
git commit -m "%message%"
git push origin master