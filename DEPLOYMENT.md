# Deployment Guide

## Deploy to Render (Free & Recommended)

1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Name: sportygen-bot
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python keep_alive.py`
5. Add Environment Variables (click "Advanced"):
   - `TELEGRAM_BOT_TOKEN` - Your bot token from @BotFather
   - `PLAYO_AUTH_TOKEN` - Your Playo API token
   - `PLAYO_MOBILE` - Your mobile number
   - `PLAYO_VENUE_ID` - Venue ID
   - `PLAYO_SPORT_ID` - Sport ID (e.g., SP5)
6. Click "Create Web Service"

Free tier: 750 hours/month (enough for 24/7)

## Deploy to Railway

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your repository
4. Add Environment Variables:
   - `TELEGRAM_BOT_TOKEN=your_token_here`
   - `PLAYO_AUTH_TOKEN=your_auth_token`
   - `PLAYO_MOBILE=your_mobile`
   - `PLAYO_VENUE_ID=your_venue_id`
   - `PLAYO_SPORT_ID=SP5`
5. Deploy automatically starts

Free tier: $5 credit/month

## Local Deployment (Mac)

Run in background:

```bash
nohup python scheduled_bot.py > bot.log 2>&1 &
```

Stop:

```bash
ps aux | grep scheduled_bot.py
kill <process_id>
```

## Environment Variables

Make sure to set all these variables in your deployment platform:

- `TELEGRAM_BOT_TOKEN` - Get from @BotFather on Telegram
- `PLAYO_AUTH_TOKEN` - Your Playo API authorization token
- `PLAYO_MOBILE` - Mobile number for booking
- `PLAYO_VENUE_ID` - Venue ID from Playo
- `PLAYO_SPORT_ID` - Sport ID (e.g., SP5 for badminton)

## Bot Features

- Automatic updates 3 times daily (8 AM, 4 PM, 12 AM)
- Manual check with `/check` command
- Checks 8-9 PM and 9-10 PM slots
- Shows availability for next 4 days
