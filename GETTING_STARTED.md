# Getting Started - Required Configuration

This guide shows exactly what you need to configure to start searching for real flight deals.

## ⚡ Quick Start Checklist

- [ ] Get Amadeus API credentials
- [ ] Configure email alerts
- [ ] Verify search settings
- [ ] Run first search
- [ ] (Optional) Add SMS alerts

## Step 1: Get Amadeus API Credentials (Required)

**You need this to search for real flights.**

### Sign Up

1. Go to [developers.amadeus.com](https://developers.amadeus.com)
2. Click **"Register"**
3. Fill in:
   - Email
   - Password
   - Company name (can be personal/individual)
   - Purpose: "Personal project"
4. Verify email

### Get API Keys

1. After login, click **"My Self-Service Workspace"**
2. Click **"Create New App"**
3. Name: "Plane Ticket Search" (or anything)
4. Click **"Create"**
5. You'll see:
   - **API Key**: `aBcDeFgH1234567890`
   - **API Secret**: `XyZ123456789abcd`

### Add to `.env` File

```bash
cd /Users/jack.zhao/Documents/projects/plane-ticket-query

# Copy the example file
cp .env.example .env

# Edit the file
nano .env
```

Add your credentials:
```bash
AMADEUS_API_KEY=your_actual_api_key_here
AMADEUS_API_SECRET=your_actual_api_secret_here
```

**Free Tier Limits:**
- 2,000 API calls per month
- Perfect for this project!

---

## Step 2: Configure Email Alerts (Required)

**You need this to receive deal notifications.**

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication**
   - Go to [myaccount.google.com/security](https://myaccount.google.com/security)
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - App: "Mail"
   - Device: "Other" → "Flight Search"
   - Click **"Generate"**
   - Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

3. **Add to `.env` file**
   ```bash
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=abcdefghijklmnop  # The app password (no spaces)
   ALERT_EMAIL=your_email@gmail.com  # Where to send alerts
   ```

### Alternative: Other Email Providers

**Outlook/Hotmail:**
```bash
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your_email@outlook.com
SMTP_PASSWORD=your_password
```

**Yahoo:**
```bash
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your_email@yahoo.com
SMTP_PASSWORD=your_app_password  # Generate at account.yahoo.com
```

---

## Step 3: Verify Search Settings

Your `config/settings.yaml` is already configured with good defaults:

```yaml
search:
  departure_countries: ["US"]
  arrival_countries: ["JP", "KR"]
  cabin_class: "BUSINESS"
  adults: 2
```

### Optional: Customize Dates

Add specific date ranges you want to search:

```yaml
search:
  date_ranges:
    - start: "2026-06-01"
      end: "2026-08-31"    # Summer travel
    - start: "2026-12-15"
      end: "2027-01-10"    # Holiday season
```

Leave empty to search all upcoming dates (next 6 months).

---

## Step 4: Run Your First Search

```bash
cd /Users/jack.zhao/Documents/projects/plane-ticket-query

# Run a single search
python src/main.py --once
```

### What Will Happen

1. ✅ Connects to Amadeus API
2. ✅ Searches US → JP/KR routes for business class (2 adults)
3. ✅ Evaluates against award chart
4. ✅ Filters for good deals
5. ✅ Sends email if deals found

### Expected Output

```
============================================================
🔍 Checking for deals at 2026-02-09 15:30:00
============================================================

📍 Search Configuration:
   Departure: 21 airports in ['US']
   Arrival: 7 airports in ['JP', 'KR']
   Total combinations: 21 × 7 = 147

Searching for flights on 2026-06-15...
✓ Found 50 flights: JFK → NRT
✓ Found 12 flights: LAX → ICN
...

💰 Analyzing deals...
✓ Found 5 good deal(s)!

📧 Sending alerts...
✓ Email alert sent to your_email@gmail.com
```

---

## Step 5 (Optional): Add SMS Alerts

### Twilio Setup

1. Go to [twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Sign up (free trial: $15 credit)
3. Get a phone number
4. Copy credentials:
   - Account SID: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Auth Token: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Phone Number: `+1234567890`

5. Add to `.env`:
   ```bash
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   ALERT_PHONE_NUMBER=+1234567890  # Your phone
   ```

6. Enable in `config/settings.yaml`:
   ```yaml
   alerts:
     sms: true
   ```

---

## Complete `.env` Template

Here's what your `.env` should look like:

```bash
# Amadeus API (REQUIRED)
AMADEUS_API_KEY=your_api_key_from_amadeus
AMADEUS_API_SECRET=your_api_secret_from_amadeus

# Email (REQUIRED)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
ALERT_EMAIL=your_email@gmail.com

# Amex Account (OPTIONAL - for Selenium scraping)
# AMEX_USERNAME=your_amex_username
# AMEX_PASSWORD=your_amex_password

# SMS (OPTIONAL)
# TWILIO_ACCOUNT_SID=your_account_sid
# TWILIO_AUTH_TOKEN=your_auth_token
# TWILIO_PHONE_NUMBER=+1234567890
# ALERT_PHONE_NUMBER=+1234567890
```

---

## Testing Your Configuration

### Test 1: Check API Connection

```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

print('API Key:', os.getenv('AMADEUS_API_KEY')[:10] + '...')
print('API Secret:', os.getenv('AMADEUS_API_SECRET')[:10] + '...')
print('Email:', os.getenv('SMTP_USERNAME'))
print('✓ Configuration loaded successfully!')
"
```

### Test 2: Run Demo (No API Required)

```bash
python src/test_demo.py
```

This tests the deal detection logic with fake data.

### Test 3: Run Real Search

```bash
python src/main.py --once
```

This searches real flights with Amadeus API.

---

## Troubleshooting

### Error: "API credentials not found"

**Solution:** Check `.env` file exists and has correct keys
```bash
cat .env | grep AMADEUS
```

### Error: "Failed to send email"

**Solutions:**
- Gmail: Use App Password, not regular password
- Check SMTP settings in `.env`
- Test email: `python -c "from notifiers.email_notifier import EmailNotifier; EmailNotifier()"`

### Error: "No flights found"

**Not an error!** This means:
- No flights available for those dates
- Or prices are above your thresholds
- Try different dates or adjust thresholds

### Rate Limit Errors

Free tier: 2,000 calls/month
- Each route combination = 1 call
- 147 combinations = 147 calls per run
- You can run ~13 times/month
- For more: Upgrade Amadeus plan

---

## Customization Tips

### Search Fewer Routes (Faster, Fewer API Calls)

```yaml
# Only search specific airports instead of all US
departure_airports:
  - "JFK"
  - "LAX"
  - "SFO"
arrival_airports:
  - "NRT"
  - "ICN"
# = 3 × 2 = 6 combinations instead of 147
```

### Stricter Deal Criteria (Fewer Alerts)

```yaml
deals:
  award_chart_min_quality: "great"  # Only great/exceptional
  max_cash_price: 600  # Lower threshold
```

### More Lenient (More Alerts)

```yaml
deals:
  award_chart_min_quality: "fair"  # Accept fair deals too
  max_cash_price: 1000  # Higher threshold
```

---

## Summary: Minimum Required Configuration

**Must Have:**
1. ✅ Amadeus API key & secret in `.env`
2. ✅ Email SMTP credentials in `.env`

**Should Review:**
3. ✅ Search configuration in `config/settings.yaml`
   - Countries
   - Cabin class
   - Adults

**Optional:**
4. ⭕ Date ranges (or search next 6 months)
5. ⭕ SMS alerts (Twilio)
6. ⭕ Amex login (for Selenium scraping)

---

## Next Steps

After configuration:

1. **Test locally:** `python src/main.py --once`
2. **Set up automation:** Push to GitHub (see `GITHUB_SETUP.md`)
3. **Monitor:** Receive email alerts when deals found
4. **Customize:** Adjust thresholds and routes as needed

**You're ready to find amazing flight deals!** ✈️
