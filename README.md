# 🎾 Sportygen Court Booking Bot

An automated Telegram bot that monitors and notifies users about court availability at Sportygen facilities. The bot checks availability for 8-9 PM and 9-10 PM slots and sends scheduled updates three times daily.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [System Flow](#system-flow)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [API Integration](#api-integration)

## ✨ Features

- 🤖 **Automated Updates**: Sends court availability updates 3 times daily (8 AM, 4 PM, 12 AM)
- ⏰ **Dual Time Slots**: Checks both 8-9 PM and 9-10 PM availability
- 📅 **4-Day Forecast**: Shows availability for current day + next 3 days
- 💰 **Price Information**: Displays pricing for each available court
- 🔔 **On-Demand Checks**: Manual availability check via `/check` command
- 🏟️ **Multi-Court Support**: Monitors all 6 synthetic courts

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Telegram Bot Architecture                 │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Telegram   │◄────────┤ Scheduled    │────────►│   Playo API  │
│     User     │         │     Bot      │         │   (Courts)   │
└──────────────┘         └──────────────┘         └──────────────┘
       │                        │                         │
       │ /start, /check         │                         │
       │                        │                         │
       ▼                        ▼                         ▼
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Command    │         │  Job Queue   │         │  API Client  │
│   Handlers   │         │  (APScheduler)│         │  (requests)  │
└──────────────┘         └──────────────┘         └──────────────┘
       │                        │                         │
       │                        │                         │
       └────────────────────────┴─────────────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │  Availability Logic  │
                    │  - Parse responses   │
                    │  - Filter time slots │
                    │  - Format messages   │
                    └──────────────────────┘
```

## 🔄 System Flow

### 1. User Interaction Flow

```
User Opens Bot
      │
      ▼
  /start Command
      │
      ├─► Save User Chat ID
      │
      ├─► Register for Scheduled Updates
      │
      └─► Show Welcome Message
            │
            ▼
      ┌─────────────────┐
      │  User Receives  │
      │  3 Daily Updates│
      │  (8AM, 4PM, 12AM)│
      └─────────────────┘
            │
            ▼
      Manual /check Command
            │
            ▼
      Get Instant Update
```

### 2. Availability Check Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  Availability Check Process                  │
└─────────────────────────────────────────────────────────────┘

Start Check
    │
    ▼
Loop: Days 0-3 (Today + 3 days)
    │
    ├─► Calculate Date (YYYY-MM-DD)
    │
    ├─► API Call: GET /availability/{date}
    │       │
    │       ├─► Headers: Authorization Token
    │       ├─► Params: mobile number
    │       └─► Response: Court data JSON
    │
    ├─► Parse Response
    │       │
    │       └─► Extract courtInfo array
    │
    ├─► Loop: Time Slots (20:00, 21:00)
    │       │
    │       └─► Loop: Each Court (1-6)
    │               │
    │               ├─► Find slot by time
    │               │
    │               ├─► Check status (1=available, 0=booked)
    │               │
    │               └─► If available: Add to results
    │                       - Court name
    │                       - Price
    │                       - Time slot
    │
    └─► Format Message
            │
            ├─► Group by date
            ├─► Group by time slot
            └─► Include pricing
                    │
                    ▼
            Send to User
```

### 3. Scheduled Update Flow

```
APScheduler Job Queue
        │
        ├─► Job 1: Daily at 08:00
        │       │
        │       └─► Trigger: send_scheduled_update()
        │
        ├─► Job 2: Daily at 16:00
        │       │
        │       └─► Trigger: send_scheduled_update()
        │
        └─► Job 3: Daily at 00:00
                │
                └─► Trigger: send_scheduled_update()
                        │
                        ▼
                Check if user registered (chat_id exists)
                        │
                        ├─► Yes: Run availability check
                        │         │
                        │         └─► Send formatted message
                        │
                        └─► No: Skip (user hasn't started bot)
```

## 📁 Project Structure

```
sportygen-automation/
│
├── check_court_availability.py   # Core API client & availability logic
│   ├── check_court_availability()  # Makes API calls to Playo
│   └── find_available_slots_8_9pm() # Searches for available dates
│
├── scheduled_bot.py               # Main bot with scheduling
│   ├── start()                     # /start command handler
│   ├── check_courts()              # /check command handler
│   ├── send_scheduled_update()     # Scheduled job function
│   ├── get_availability_message()  # Message formatter
│   └── main()                      # Bot initialization & job setup
│
├── requirements.txt               # Python dependencies
├── runtime.txt                    # Python version for deployment
├── Procfile                       # Render/Heroku deployment config
├── start.sh                       # Local startup script
├── .env                          # Environment variables (gitignored)
├── .gitignore                    # Git ignore rules
│
├── README.md                     # This file
└── DEPLOYMENT.md                 # Deployment instructions
```

## 🔧 Installation

### Prerequisites

- Python 3.13+
- pip (Python package manager)
- Telegram account
- Bot token from @BotFather

### Local Setup

1. **Clone the repository**

```bash
git clone https://github.com/akki251/sportygen-public.git
cd sportygen-public
```

2. **Create virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your credentials
# Required variables:
# - TELEGRAM_BOT_TOKEN
# - PLAYO_AUTH_TOKEN
# - PLAYO_MOBILE
# - PLAYO_VENUE_ID
# - PLAYO_SPORT_ID
```

5. **Run the bot**

```bash
python scheduled_bot.py
```

## ⚙️ Configuration

### Environment Variables

| Variable             | Description                        | Required | Example             |
| -------------------- | ---------------------------------- | -------- | ------------------- |
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather          | Yes      | `123456:ABC-DEF...` |
| `PLAYO_AUTH_TOKEN`   | Playo API authorization token      | Yes      | `uuid:uuid`         |
| `PLAYO_MOBILE`       | Mobile number for booking          | Yes      | `9876543210`        |
| `PLAYO_VENUE_ID`     | Venue ID from Playo                | Yes      | `uuid`              |
| `PLAYO_SPORT_ID`     | Sport ID (e.g., SP5 for badminton) | Yes      | `SP5`               |

### Bot Configuration

Edit `scheduled_bot.py` to customize:

```python
# Update times (currently 8 AM, 4 PM, 12 AM)
job_queue.run_daily(send_scheduled_update, time=time(8, 0, 0))
job_queue.run_daily(send_scheduled_update, time=time(16, 0, 0))
job_queue.run_daily(send_scheduled_update, time=time(0, 0, 0))

# Change time slots (currently 8-9 PM and 9-10 PM)
time_slots = [
    ("20:00:00", "8-9 PM"),
    ("21:00:00", "9-10 PM")
]

# Adjust forecast days (currently 4 days)
for days_ahead in range(4):  # Change 4 to desired number
```

## 📱 Usage

### Bot Commands

| Command  | Description                             |
| -------- | --------------------------------------- |
| `/start` | Initialize bot and register for updates |
| `/check` | Get instant availability update         |
| `/help`  | Show help message                       |

### Example Interaction

```
User: /start

Bot: 🎾 Court Availability Bot

✅ You will receive automatic updates 3 times daily:
  • 8:00 AM
  • 4:00 PM
  • 12:00 AM

Commands:
/check - Check available courts now
/help - Show this message

---

User: /check

Bot: 🔍 Checking court availability...

🎾 Available Courts:

📅 2026-02-26 (Thursday):
  ⏰ 8-9 PM:
    • Synthetic Court 4 - ₹440.0

📅 2026-02-27 (Friday):
  ⏰ 8-9 PM:
    • Synthetic Court 4 - ₹440.0
  ⏰ 9-10 PM:
    • Synthetic Court 2 - ₹440.0
```

## 🚀 Deployment

### Render (Recommended - Free)

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect GitHub repository
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python scheduled_bot.py`
6. Add environment variable: `TELEGRAM_BOT_TOKEN`
7. Deploy

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Railway

1. Go to [railway.app](https://railway.app)
2. Deploy from GitHub repo
3. Add environment variable
4. Auto-deploys

### Local (Background)

```bash
nohup python scheduled_bot.py > bot.log 2>&1 &
```

## 🔌 API Integration

### Playo API Endpoint

```
GET https://api.playo.io/booking-lab/availability/v1/{venue_id}/{sport_id}/{date}
```

### Request Details

**Headers:**

```
Authorization: {auth_token}
Accept: application/json
User-Agent: Ktor client
Content-Type: application/json
```

**Query Parameters:**

```
mobile: {user_mobile_number}
```

**Response Structure:**

```json
{
  "requestStatus": 1,
  "message": "success",
  "data": {
    "courtInfo": [
      {
        "courtName": "Synthetic Court 1",
        "courtId": 10333,
        "slotInfo": [
          {
            "time": "20:00:00",
            "status": 1,
            "price": 440.0
          }
        ]
      }
    ]
  }
}
```

**Status Codes:**

- `status: 1` = Available
- `status: 0` = Booked

## 🛠️ Technical Details

### Dependencies

- `python-telegram-bot[job-queue]` - Telegram bot framework with scheduling
- `requests` - HTTP client for API calls
- `python-dotenv` - Environment variable management
- `APScheduler` - Job scheduling library

### Key Components

1. **API Client** (`check_court_availability.py`)
   - Handles HTTP requests to Playo API
   - Parses JSON responses
   - Filters available slots

2. **Bot Handler** (`scheduled_bot.py`)
   - Manages Telegram bot lifecycle
   - Processes user commands
   - Schedules automated updates

3. **Job Scheduler** (APScheduler)
   - Runs tasks at specific times
   - Manages daily update schedule
   - Handles timezone conversions

## 📊 Data Flow Diagram

```
┌─────────────┐
│   User      │
│  Telegram   │
└──────┬──────┘
       │
       │ /check or Scheduled Time
       │
       ▼
┌─────────────────────────────────┐
│     scheduled_bot.py            │
│  ┌───────────────────────────┐  │
│  │ get_availability_message()│  │
│  └───────────┬───────────────┘  │
└──────────────┼──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  check_court_availability.py    │
│  ┌───────────────────────────┐  │
│  │ check_court_availability()│  │
│  └───────────┬───────────────┘  │
└──────────────┼──────────────────┘
               │
               │ HTTP GET Request
               │
               ▼
┌─────────────────────────────────┐
│        Playo API                │
│  /booking-lab/availability/v1/  │
└──────────────┬──────────────────┘
               │
               │ JSON Response
               │
               ▼
┌─────────────────────────────────┐
│     Parse & Filter              │
│  - Extract court info           │
│  - Check time slots (20:00,21:00)│
│  - Filter status = 1            │
│  - Format with prices           │
└──────────────┬──────────────────┘
               │
               │ Formatted Message
               │
               ▼
┌─────────────────────────────────┐
│   Send to User via Telegram     │
└─────────────────────────────────┘
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- Bot: [@Sportygen_bot](https://t.me/Sportygen_bot)
- Repository: [GitHub](https://github.com/akki251/sportygen-public)

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

Made with ❤️ for Sportygen court booking automation
