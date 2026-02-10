# Quick Start Guide

Get your flight alert system running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Get API Keys

### Amadeus API (Required)
1. Go to [developers.amadeus.com](https://developers.amadeus.com/register)
2. Sign up for a free account
3. Create a new app to get your API Key and Secret

### Email Setup (Required for alerts)
**Gmail Example:**
1. Enable 2-factor authentication on your Google account
2. Generate an App Password: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Use this app password (not your regular Gmail password)

### SMS Setup (Optional)
1. Sign up at [twilio.com](https://www.twilio.com/try-twilio)
2. Get a free trial phone number
3. Copy your Account SID and Auth Token

## Step 3: Configure

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Minimum required in `.env`:
```
AMADEUS_API_KEY=your_api_key
AMADEUS_API_SECRET=your_api_secret
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_EMAIL=where_to_send_alerts@gmail.com
```

## Step 4: Set Your Route

Edit `config/settings.yaml`:

```yaml
search:
  departure_country: "US"
  departure_airports:
    - "JFK"
    - "EWR"

  arrival_country: "JP"
  arrival_airports:
    - "NRT"
    - "HND"
```

## Step 5: Run It!

### Test Run (one-time check)
```bash
python src/main.py --once
```

### Continuous Monitoring
```bash
python src/main.py
```

This will check for deals every hour (configurable in settings.yaml) and email you when good deals are found!

## Customization

### Adjust Deal Thresholds
In `config/settings.yaml`:
```yaml
deals:
  max_cash_price: 800    # Max price in USD
  max_points: 60000      # Max Amex points
  min_cpp: 1.5          # Minimum cents per point value
```

### Change Check Frequency
```yaml
alerts:
  check_interval: 60  # Minutes between checks
```

### Add Date Ranges
```yaml
search:
  date_ranges:
    - start: "2026-06-01"
      end: "2026-08-31"
    - start: "2026-12-15"
      end: "2027-01-10"
```

## Troubleshooting

### "Missing configuration" error
- Make sure you created `.env` file (not `.env.example`)
- Double-check your API keys are correct

### "No flights found"
- Try widening your date ranges
- Check that airport codes are valid IATA codes
- Amadeus free tier has rate limits (10 requests/sec)

### Email not sending
- Gmail users: Make sure you're using an App Password, not your regular password
- Check SMTP settings in `.env`

## Next Steps

### Switch to Selenium (for Amex Travel direct scraping)
When you're ready to scrape Amex Travel directly:

1. The architecture is ready - just implement `src/searchers/selenium_searcher.py`
2. Update `config/settings.yaml`: `searcher: type: "selenium"`
3. The rest of the code will work the same way!

### Add More Features
- Round-trip searches
- Multi-city itineraries
- Flexible date searches (+/- 3 days)
- Price tracking over time
- Database to avoid duplicate alerts
