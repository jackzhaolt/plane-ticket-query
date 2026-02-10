# Plane Ticket Query & Alert System

🎯 **Smart flight search system** that monitors for Amex points deals and sends you alerts.

## ✨ Key Features

- 🚀 **Hybrid Search**: Fast API screening + accurate Amex Travel scraping
- 💎 **Amex Points Focus**: Get exact points pricing, not just estimates
- 📧 **Smart Alerts**: Email/SMS when deals match your criteria
- 🤖 **Automated Monitoring**: Runs 24/7, checks as often as you want
- ⚡ **Intelligent Caching**: Avoids redundant work, maximizes efficiency
- 🔄 **Flexible Modes**: API-only, Selenium-only, or smart hybrid

## Project Structure

```
├── config/
│   └── settings.yaml          # User configuration
├── src/
│   ├── searchers/
│   │   ├── base.py           # Base searcher interface
│   │   ├── api_searcher.py   # API-based implementation
│   │   └── selenium_searcher.py  # Future Selenium implementation
│   ├── notifiers/
│   │   ├── email_notifier.py # Email alerts
│   │   └── sms_notifier.py   # SMS alerts
│   ├── deal_detector.py      # Logic to identify good deals
│   └── main.py               # Main orchestration
├── requirements.txt
└── .env.example              # Environment variables template
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

3. Configure your search preferences in `config/settings.yaml`

4. Run the script:
```bash
python src/main.py
```

## Configuration

Edit `config/settings.yaml` to set:
- Departure and arrival countries/airports
- Deal thresholds (max points/price)
- Alert preferences
- Search frequency

## API Keys & Credentials

| Service | Required? | Purpose | Get It |
|---------|-----------|---------|--------|
| **Amadeus API** | Recommended | Fast flight screening | [developers.amadeus.com](https://developers.amadeus.com) |
| **Email SMTP** | Yes | Send deal alerts | Gmail app password |
| **Twilio SMS** | Optional | SMS alerts | [twilio.com](https://twilio.com) |
| **Amex Account** | Optional | Member pricing | Your Amex login |

## How It Works

### 🎯 Hybrid Approach (Recommended)

```
1. Fast API Check (Amadeus)
   ↓ Every hour, scan 100s of flights in seconds

2. Smart Decision
   ↓ Found deals under $1000?

3. Deep Amex Scraping (Selenium)
   ↓ Get exact points pricing from Amex Travel

4. Alert You
   ↓ Email/SMS with best deals
```

### Three Search Modes

1. **Hybrid** (default): API for speed + Selenium for accuracy
2. **API-only**: Fast checks, estimated points
3. **Selenium-only**: Slow but exact Amex points

See `HYBRID_SYSTEM.md` for detailed explanation.
