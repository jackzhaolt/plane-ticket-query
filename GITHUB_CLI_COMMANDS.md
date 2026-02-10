# GitHub CLI Commands Reference

## Quick Setup (One Command)

```bash
# Run the automated setup script
./GITHUB_CLI_SETUP.sh
```

This will:
1. Authenticate with GitHub (if needed)
2. Initialize git repository
3. Commit all files
4. Create GitHub repository
5. Push code to GitHub

## Manual Commands

If you prefer to run commands manually:

### 1. Authenticate with GitHub

```bash
gh auth login
```

Follow the prompts:
- What account? **GitHub.com**
- What is your preferred protocol? **HTTPS** (recommended)
- Authenticate? **Login with a web browser**
- Copy the one-time code and press Enter
- Browser will open → paste code → authorize

### 2. Check Authentication

```bash
gh auth status
```

### 3. Initialize Git & Commit

```bash
cd /Users/jack.zhao/Documents/projects/plane-ticket-query

git init
git add .
git commit -m "Initial commit: Automated flight deal search system"
```

### 4. Create Repository & Push

```bash
# Create private repository and push
gh repo create plane-ticket-query --private --source=. --push

# Or create public repository
gh repo create plane-ticket-query --public --source=. --push
```

Options:
- `--private` or `--public` - Repository visibility
- `--source=.` - Use current directory
- `--push` - Push code immediately
- `--description "Description here"` - Add description

### 5. Add GitHub Secrets

```bash
# Add secrets one by one (will prompt for value)
gh secret set AMADEUS_API_KEY
gh secret set AMADEUS_API_SECRET
gh secret set SMTP_SERVER -b"smtp.gmail.com"
gh secret set SMTP_PORT -b"587"
gh secret set SMTP_USERNAME
gh secret set SMTP_PASSWORD
gh secret set ALERT_EMAIL

# Optional secrets
gh secret set AMEX_USERNAME
gh secret set AMEX_PASSWORD
gh secret set TWILIO_ACCOUNT_SID
gh secret set TWILIO_AUTH_TOKEN
gh secret set TWILIO_PHONE_NUMBER
gh secret set ALERT_PHONE_NUMBER
```

**Flags:**
- `-b` - Set value directly in command
- Without `-b` - Will prompt for value (more secure)

### 6. View Repository

```bash
# Open repository in browser
gh repo view --web

# View repository info in terminal
gh repo view
```

### 7. Manage Workflows

```bash
# List workflows
gh workflow list

# Run workflow manually
gh workflow run search-deals.yml

# View workflow runs
gh run list

# View specific run details
gh run view <run-id>

# Watch a running workflow
gh run watch
```

### 8. View Secrets

```bash
# List secrets (values are hidden)
gh secret list

# Delete a secret
gh secret delete AMADEUS_API_KEY
```

## Useful Commands

### Clone Repository Later

```bash
gh repo clone YOUR_USERNAME/plane-ticket-query
```

### Update Configuration

```bash
# Edit config
nano config/settings.yaml

# Commit and push
git add config/settings.yaml
git commit -m "Update search configuration"
git push
```

### View Logs

```bash
# View recent workflow runs
gh run list --workflow=search-deals.yml

# View logs for a specific run
gh run view <run-id> --log

# View logs and follow (live)
gh run view <run-id> --log-failed
```

### Trigger Workflow

```bash
# Trigger manually
gh workflow run search-deals.yml

# Trigger and watch
gh workflow run search-deals.yml && gh run watch
```

## Complete Workflow

Here's the complete setup in one go:

```bash
#!/bin/bash

# 1. Authenticate
gh auth login

# 2. Create and push
cd /Users/jack.zhao/Documents/projects/plane-ticket-query
git init
git add .
git commit -m "Initial commit: Automated flight deal search system"
gh repo create plane-ticket-query --private --source=. --push

# 3. Add secrets
gh secret set AMADEUS_API_KEY
gh secret set AMADEUS_API_SECRET
gh secret set SMTP_SERVER -b"smtp.gmail.com"
gh secret set SMTP_PORT -b"587"
gh secret set SMTP_USERNAME
gh secret set SMTP_PASSWORD
gh secret set ALERT_EMAIL

# 4. Trigger first run
gh workflow run search-deals.yml

# 5. Watch it run
gh run watch

# 6. Open in browser
gh repo view --web
```

## Troubleshooting

### Not authenticated?

```bash
gh auth login
```

### Repository already exists?

```bash
# Push to existing repo
git remote add origin https://github.com/YOUR_USERNAME/plane-ticket-query.git
git branch -M main
git push -u origin main
```

### Can't find workflow?

```bash
# Wait a moment for GitHub to process
# Then list workflows
gh workflow list
```

### Secrets not showing up?

```bash
# List to verify
gh secret list

# Re-add if needed
gh secret set AMADEUS_API_KEY
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `gh auth login` | Authenticate with GitHub |
| `gh auth status` | Check authentication status |
| `gh repo create NAME --private --source=. --push` | Create & push repo |
| `gh secret set NAME` | Add a secret |
| `gh secret list` | List secrets |
| `gh workflow list` | List workflows |
| `gh workflow run NAME` | Trigger workflow |
| `gh run list` | View workflow runs |
| `gh run watch` | Watch running workflow |
| `gh repo view --web` | Open repo in browser |

## GitHub CLI Documentation

Full docs: https://cli.github.com/manual/

## Summary

**Simplest approach:**
```bash
./GITHUB_CLI_SETUP.sh
```

**Manual approach:**
```bash
gh auth login
gh repo create plane-ticket-query --private --source=. --push
gh secret set AMADEUS_API_KEY
# ... add other secrets
gh workflow run search-deals.yml
```

Both accomplish the same thing - pick whichever you prefer! 🚀
