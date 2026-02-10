#!/bin/bash

echo "=================================================="
echo "Pushing to https://github.com/jackzhaolt/plane-ticket-query"
echo "=================================================="
echo ""

# Initialize git if needed
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git branch -M main
fi

# Add all files
echo "Adding files..."
git add .

# Create commit
echo "Creating commit..."
git commit -m "Initial commit: Automated flight deal search system

Features:
- Hybrid search (API + Selenium)
- Award chart evaluation with distance-based bands
- Country-level configuration (US → JP, KR)
- Business class search for 2 adults
- GitHub Actions with cron scheduling
- Email & SMS alerts
- 50+ airports, multiple award charts
- Complete documentation
"

# Add remote
echo "Adding remote repository..."
git remote add origin https://github.com/jackzhaolt/plane-ticket-query.git 2>/dev/null || git remote set-url origin https://github.com/jackzhaolt/plane-ticket-query.git

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "=================================================="
echo "✅ Successfully pushed to GitHub!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Go to: https://github.com/jackzhaolt/plane-ticket-query/settings/secrets/actions"
echo "2. Add GitHub Secrets (see GITHUB_SETUP.md)"
echo "3. Trigger workflow: https://github.com/jackzhaolt/plane-ticket-query/actions"
echo ""
