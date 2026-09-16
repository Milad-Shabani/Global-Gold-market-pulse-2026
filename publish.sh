#!/usr/bin/env bash
# One-click publish for the Global Gold Market Pulse repo.
# Requires: git, GitHub CLI (`gh`) authenticated (`gh auth login`).
set -euo pipefail

REPO_NAME="global-gold-market-pulse-2026"
DESCRIPTION="Interactive, source-cited BI dashboard on world gold reserves, production & demand — real World Gold Council / IMF IFS & USGS data, Python-to-Excel pipeline + white-background HTML dashboard."
GIT_USER_NAME="Milad Shabani"
GIT_USER_EMAIL="MILAD.SHABANI6515@GMAIL.COM"

echo "==> Configuring git identity for this repo"
git init -q
git config user.name "$GIT_USER_NAME"
git config user.email "$GIT_USER_EMAIL"

echo "==> Staging and committing"
git add -A
git commit -q -m "Initial commit: Global Gold Market Pulse dashboard + Excel pipeline" || echo "(nothing new to commit)"
git branch -M main

echo "==> Creating GitHub repository: $REPO_NAME"
if ! gh repo view "$REPO_NAME" >/dev/null 2>&1; then
  gh repo create "$REPO_NAME" --public --source=. --remote=origin --description "$DESCRIPTION"
else
  echo "Repo already exists on GitHub, adding remote if missing..."
  git remote add origin "https://github.com/$(gh api user --jq .login)/$REPO_NAME.git" 2>/dev/null || true
fi

echo "==> Pushing"
git push -u origin main

echo "==> Setting topics"
gh repo edit --add-topic business-intelligence \
             --add-topic data-analytics \
             --add-topic python \
             --add-topic excel \
             --add-topic dashboard \
             --add-topic gold \
             --add-topic imf \
             --add-topic data-visualization

echo "==> Enabling GitHub Pages (serves /dashboard via a workflow — see .github/workflows/pages.yml)"
OWNER=$(gh api user --jq .login)
gh api -X PUT "repos/$OWNER/$REPO_NAME/pages" \
  -f build_type="workflow" >/dev/null 2>&1 || echo "(Pages may already be configured, or will activate after the first workflow run)"

echo ""
echo "✅ Done. Repo: https://github.com/$(gh api user --jq .login)/$REPO_NAME"
echo "   Dashboard (after Pages workflow runs): https://$(gh api user --jq .login).github.io/$REPO_NAME/"
