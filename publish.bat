@echo off
REM One-click publish for the Global Gold Market Pulse repo (Windows).
REM Requires: git, GitHub CLI (gh) authenticated (gh auth login).

setlocal
set REPO_NAME=global-gold-market-pulse-2026
set DESCRIPTION=Interactive, source-cited BI dashboard on world gold reserves, production ^& demand — real World Gold Council / IMF IFS ^& USGS data, Python-to-Excel pipeline + white-background HTML dashboard.
set GIT_USER_NAME=Milad Shabani
set GIT_USER_EMAIL=MILAD.SHABANI6515@GMAIL.COM

echo ==^> Configuring git identity for this repo
git init -q
git config user.name "%GIT_USER_NAME%"
git config user.email "%GIT_USER_EMAIL%"

echo ==^> Staging and committing
git add -A
git commit -q -m "Initial commit: Global Gold Market Pulse dashboard + Excel pipeline"
git branch -M main

echo ==^> Creating GitHub repository: %REPO_NAME%
gh repo view %REPO_NAME% >nul 2>&1
if errorlevel 1 (
    gh repo create %REPO_NAME% --public --source=. --remote=origin --description "%DESCRIPTION%"
) else (
    echo Repo already exists on GitHub, skipping create.
)

echo ==^> Pushing
git push -u origin main

echo ==^> Setting topics
gh repo edit --add-topic business-intelligence --add-topic data-analytics --add-topic python --add-topic excel --add-topic dashboard --add-topic gold --add-topic imf --add-topic data-visualization

echo ==^> Enabling GitHub Pages (workflow build)
for /f "delims=" %%i in ('gh api user --jq .login') do set OWNER=%%i
gh api -X PUT "repos/%OWNER%/%REPO_NAME%/pages" -f build_type=workflow

echo.
echo Done. Repo: https://github.com/%OWNER%/%REPO_NAME%
echo Dashboard (after Pages workflow runs): https://%OWNER%.github.io/%REPO_NAME%/
endlocal
