# GitHub Actions Setup Guide

This guide will help you set up automated flight deal searches using GitHub Actions.

## Overview

The GitHub Actions workflow will:
- ✅ Run automatically on a schedule (every 6 hours by default)
- ✅ Search for flight deals based on your configuration
- ✅ Send email/SMS alerts when deals are found
- ✅ Run for free on GitHub's hosted runners
- ✅ Can be triggered manually anytime

## Step 1: Push to GitHub

### Initialize Git Repository

```bash
cd /Users/jack.zhao/Documents/projects/plane-ticket-query

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Plane ticket query system with award chart evaluation"
```

### Create GitHub Repository

1. Go to [github.com](https://github.com) and log in
2. Click the **"+"** icon → **"New repository"**
3. Name it: `plane-ticket-query` (or your preferred name)
4. Choose **Private** (recommended - contains your search preferences)
5. **Don't** initialize with README, .gitignore, or license (we have those)
6. Click **"Create repository"**

### Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/plane-ticket-query.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Configure GitHub Secrets

GitHub Secrets keep your API keys and credentials secure.

### Add Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**

### Required Secrets

Add each of these as a separate secret:

#### Amadeus API (Required)
```
Name: AMADEUS_API_KEY
Value: your_api_key_from_amadeus

Name: AMADEUS_API_SECRET
Value: your_api_secret_from_amadeus
```

Get these from: [developers.amadeus.com](https://developers.amadeus.com)

#### Email Notifications (Required)
```
Name: SMTP_SERVER
Value: smtp.gmail.com

Name: SMTP_PORT
Value: 587

Name: SMTP_USERNAME
Value: your_email@gmail.com

Name: SMTP_PASSWORD
Value: your_gmail_app_password

Name: ALERT_EMAIL
Value: where_to_send_alerts@gmail.com
```

**Gmail App Password**: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

#### Amex Account (Optional)
```
Name: AMEX_USERNAME
Value: your_amex_username

Name: AMEX_PASSWORD
Value: your_amex_password
```

#### SMS Notifications (Optional)
```
Name: TWILIO_ACCOUNT_SID
Value: your_twilio_sid

Name: TWILIO_AUTH_TOKEN
Value: your_twilio_token

Name: TWILIO_PHONE_NUMBER
Value: +1234567890

Name: ALERT_PHONE_NUMBER
Value: +1234567890
```

Get Twilio credentials from: [twilio.com](https://www.twilio.com/try-twilio)

## Step 3: Configure Schedule

Edit `.github/workflows/search-deals.yml`:

```yaml
schedule:
  # Run every 6 hours
  - cron: '0 */6 * * *'
```

### Cron Schedule Examples

| Schedule | Cron Expression | Description |
|----------|----------------|-------------|
| Every hour | `0 * * * *` | Run at minute 0 of every hour |
| Every 4 hours | `0 */4 * * *` | Run at 00:00, 04:00, 08:00, etc. |
| Every 6 hours | `0 */6 * * *` | Run at 00:00, 06:00, 12:00, 18:00 |
| Twice daily | `0 8,20 * * *` | Run at 8am and 8pm UTC |
| Daily at 9am UTC | `0 9 * * *` | Once per day |
| Weekdays only | `0 */6 * * 1-5` | Every 6 hours, Mon-Fri |

**Note**: GitHub Actions cron uses UTC time. Convert your local time to UTC.

### Cron Syntax

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday=0)
│ │ │ │ │
* * * * *
```

## Step 4: Test the Workflow

### Manual Trigger

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Click **"Search Flight Deals"** workflow
4. Click **"Run workflow"** → **"Run workflow"**
5. Watch it run in real-time!

### Check Results

- ✅ Green checkmark = Success (deals found and alerts sent)
- ❌ Red X = Failed (check logs for errors)
- 🟡 Yellow = Running

### View Logs

1. Click on a workflow run
2. Click on the **"search-flights"** job
3. Expand each step to see details

## Step 5: Monitor & Maintain

### Email Notifications

When deals are found, you'll receive:
- Email alerts with deal details
- SMS alerts (if configured)
- Formatted with award chart analysis

### GitHub Actions Usage

- **Free tier**: 2,000 minutes/month for private repos
- **This workflow**: ~5 minutes per run
- **Every 6 hours**: 4 runs/day × 5 min = 20 min/day = 600 min/month ✅
- **Plenty of headroom** for free tier!

### Troubleshooting

#### Workflow not running?

1. Check if secrets are set correctly
2. Verify cron syntax
3. GitHub Actions must be enabled in repo settings
4. Check if you've exceeded free tier limits

#### No deals found?

1. Check logs for API errors
2. Verify API keys are valid
3. Adjust deal thresholds in `config/settings.yaml`
4. Try broader date ranges

#### Emails not sending?

1. Check SMTP credentials
2. Verify Gmail app password (not regular password)
3. Check spam folder
4. Review workflow logs for errors

## Step 6: Customize Configuration

### Edit Search Preferences

Modify `config/settings.yaml` and push changes:

```bash
# Edit the file
nano config/settings.yaml

# Commit and push
git add config/settings.yaml
git commit -m "Update search configuration"
git push
```

Changes take effect on the next scheduled run.

### Quick Configuration Changes

**Widen search:**
```yaml
departure_countries:
  - "US"
  - "CA"  # Add Canada

arrival_countries:
  - "JP"
  - "KR"
  - "TW"  # Add Taiwan
  - "SG"  # Add Singapore
```

**Stricter deals:**
```yaml
deals:
  award_chart_min_quality: "great"  # Only great/exceptional
  max_cash_price: 600  # Stricter cash limit
```

**More frequent checks:**
```yaml
# In .github/workflows/search-deals.yml
schedule:
  - cron: '0 */4 * * *'  # Every 4 hours instead of 6
```

## Advanced: Multiple Workflows

You can create separate workflows for different searches:

### `.github/workflows/search-asia.yml`
```yaml
name: Search Asia Deals
schedule:
  - cron: '0 */6 * * *'
# Customize config for Asia routes
```

### `.github/workflows/search-europe.yml`
```yaml
name: Search Europe Deals
schedule:
  - cron: '0 8,20 * * *'
# Customize config for Europe routes
```

## Security Best Practices

✅ **Use GitHub Secrets** - Never commit API keys to code
✅ **Private Repository** - Keep your search preferences private
✅ **Rotate Keys** - Change API keys periodically
✅ **Review Logs** - Check workflow logs occasionally
✅ **Limit Scope** - Only add necessary secrets

## Cost Considerations

### GitHub Actions (Free Tier)
- ✅ 2,000 minutes/month for private repos
- ✅ Unlimited for public repos
- ✅ This workflow uses ~600 min/month at 6-hour schedule

### API Costs
- ✅ Amadeus: 2,000 free calls/month (plenty!)
- ✅ Twilio: Free trial ($15 credit)
- ✅ Email: Free (using your Gmail)

### Total Cost: $0/month! 🎉

## Example: Complete Setup

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/plane-ticket-query.git
git push -u origin main

# 2. Add secrets in GitHub UI
# (Follow Step 2 above)

# 3. Trigger first run
# Go to Actions tab → Run workflow

# 4. Wait for email alert! 📧
```

## Monitoring Dashboard

GitHub provides a dashboard showing:
- ✅ Successful runs
- ❌ Failed runs
- ⏱️ Execution time
- 📊 Usage statistics

Access at: `https://github.com/YOUR_USERNAME/plane-ticket-query/actions`

## Support

If you encounter issues:
1. Check workflow logs
2. Verify secrets are set
3. Test locally first: `python src/main.py --once`
4. Review `QUICKSTART.md` for configuration help

## Summary

✅ Push to GitHub
✅ Add secrets (API keys, email credentials)
✅ Configure schedule (cron expression)
✅ Enable workflow
✅ Sit back and receive deal alerts!

**The system will now search for deals automatically and email you when it finds exceptional opportunities!** 🚀
