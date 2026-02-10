#!/bin/bash

# GitHub CLI Setup and Push Script
# This script will create a GitHub repo and push your code

set -e  # Exit on error

echo "=============================================="
echo "🚀 GitHub CLI Setup & Push"
echo "=============================================="
echo ""

# Step 1: Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found!"
    echo "Install with: brew install gh"
    exit 1
fi

echo "✅ GitHub CLI found"
echo ""

# Step 2: Authenticate with GitHub
echo "Step 1: Authenticate with GitHub"
echo "----------------------------------------------"
gh auth status 2>/dev/null || {
    echo "Not logged in. Authenticating..."
    gh auth login
}

echo ""
echo "✅ Authenticated with GitHub"
echo ""

# Step 3: Initialize git repository
echo "Step 2: Initialize Git Repository"
echo "----------------------------------------------"

if [ -d .git ]; then
    echo "⚠️  Git repository already initialized"
else
    git init
    echo "✅ Git repository initialized"
fi

# Step 4: Add and commit files
echo ""
echo "Step 3: Add and Commit Files"
echo "----------------------------------------------"

git add .
git commit -m "Initial commit: Automated flight deal search system

Features:
- Hybrid search (API + Selenium)
- Award chart evaluation (distance-based)
- Country-level configuration
- GitHub Actions with cron scheduling
- Email & SMS alerts
- 50+ airports, multiple award charts
" || echo "⚠️  Nothing to commit or already committed"

echo "✅ Files committed"
echo ""

# Step 5: Create GitHub repository
echo "Step 4: Create GitHub Repository"
echo "----------------------------------------------"

read -p "Repository name [plane-ticket-query]: " REPO_NAME
REPO_NAME=${REPO_NAME:-plane-ticket-query}

read -p "Make repository private? (y/n) [y]: " PRIVATE
PRIVATE=${PRIVATE:-y}

if [[ "$PRIVATE" == "y" || "$PRIVATE" == "Y" ]]; then
    VISIBILITY="--private"
    echo "Creating PRIVATE repository..."
else
    VISIBILITY="--public"
    echo "Creating PUBLIC repository..."
fi

# Create repository
gh repo create "$REPO_NAME" $VISIBILITY --source=. --push

echo ""
echo "✅ Repository created and pushed!"
echo ""

# Step 6: Display next steps
echo "=============================================="
echo "✅ SUCCESS! Repository created and pushed"
echo "=============================================="
echo ""
echo "Repository URL:"
gh repo view --web || true
echo ""
echo "Next Steps:"
echo "----------------------------------------------"
echo ""
echo "1. Add GitHub Secrets for automation:"
echo "   gh secret set AMADEUS_API_KEY"
echo "   gh secret set AMADEUS_API_SECRET"
echo "   gh secret set SMTP_SERVER -b'smtp.gmail.com'"
echo "   gh secret set SMTP_PORT -b'587'"
echo "   gh secret set SMTP_USERNAME"
echo "   gh secret set SMTP_PASSWORD"
echo "   gh secret set ALERT_EMAIL"
echo ""
echo "2. Or add secrets via web interface:"
echo "   Settings → Secrets and variables → Actions"
echo ""
echo "3. Trigger workflow manually:"
echo "   gh workflow run search-deals.yml"
echo ""
echo "4. View workflow runs:"
echo "   gh run list"
echo ""
echo "See GITHUB_SETUP.md for detailed instructions!"
echo ""
