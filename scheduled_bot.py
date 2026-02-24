import os
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from check_court_availability import check_court_availability
from datetime import datetime, timedelta, time
from dotenv import load_dotenv
import pytz
import asyncio

load_dotenv()

# Set timezone to IST (India Standard Time)
IST = pytz.timezone('Asia/Kolkata')

# Your Telegram User ID - get it by messaging @userinfobot on Telegram
YOUR_CHAT_ID = None  # Will be set when you send /start

async def get_availability_message():
    """Generate availability message for both time slots."""
    time_slots = [
        ("20:00:00", "8-9 PM"),
        ("21:00:00", "9-10 PM")
    ]
    
    message_lines = ["🎾 Court Availability Update:\n"]
    
    for days_ahead in range(4):
        check_date = datetime.now() + timedelta(days=days_ahead)
        date_str = check_date.strftime("%Y-%m-%d")
        day_name = check_date.strftime("%A")
        
        result = check_court_availability(date=date_str)
        
        if result and result.get('requestStatus') == 1:
            court_info = result.get('data', {}).get('courtInfo', [])
            date_has_courts = False
            
            for target_time, time_label in time_slots:
                available_courts = []
                
                for court in court_info:
                    court_name = court.get('courtName')
                    slots = court.get('slotInfo', [])
                    
                    for slot in slots:
                        if slot.get('time') == target_time and slot.get('status') == 1:
                            available_courts.append(f"    • {court_name} - ₹{slot.get('price')}")
                            break
                
                if available_courts:
                    if not date_has_courts:
                        message_lines.append(f"\n📅 {date_str} ({day_name}):")
                        date_has_courts = True
                    message_lines.append(f"  ⏰ {time_label}:")
                    message_lines.extend(available_courts)
            
            if not date_has_courts:
                message_lines.append(f"\n📅 {date_str} ({day_name}): ❌ No courts")
    
    return "\n".join(message_lines)

async def send_scheduled_update(context: ContextTypes.DEFAULT_TYPE):
    """Send scheduled update to user."""
    if YOUR_CHAT_ID:
        message = await get_availability_message()
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=message)
        print(f"✅ Sent update at {datetime.now()}")

async def start(update, context):
    """Handle /start command and save user's chat ID."""
    global YOUR_CHAT_ID
    YOUR_CHAT_ID = update.effective_chat.id
    
    await update.message.reply_text(
        "🎾 Court Availability Bot\n\n"
        "✅ You will receive automatic updates 3 times daily:\n"
        "  • 8:00 AM IST\n"
        "  • 4:00 PM IST\n"
        "  • 12:00 AM IST\n\n"
        "Commands:\n"
        "/check - Check available courts now\n"
        "/help - Show this message"
    )
    print(f"📝 Saved chat ID: {YOUR_CHAT_ID}")

async def check_courts(update, context):
    """Check court availability on demand."""
    await update.message.reply_text("🔍 Checking court availability...")
    message = await get_availability_message()
    await update.message.reply_text(message)

async def help_command(update, context):
    """Send help message."""
    await start(update, context)

def main():
    """Start the bot with scheduled updates."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not set")
        return
    
    # Create application with job queue enabled
    application = (
        Application.builder()
        .token(token)
        .build()
    )
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", check_courts))
    application.add_handler(CommandHandler("help", help_command))
    
    # Get job queue
    job_queue = application.job_queue
    
    if job_queue is None:
        print("❌ Error: JobQueue not available")
        print("🔄 Running without scheduled updates...")
        application.run_polling(allowed_updates=['message', 'callback_query'])
        return
    
    # Schedule updates 3 times a day (every 8 hours) in IST
    job_queue.run_daily(send_scheduled_update, time=time(8, 0, 0, tzinfo=IST))   # 8 AM IST
    job_queue.run_daily(send_scheduled_update, time=time(16, 0, 0, tzinfo=IST))  # 4 PM IST
    job_queue.run_daily(send_scheduled_update, time=time(0, 0, 0, tzinfo=IST))   # 12 AM IST
    
    print("🤖 Bot is running with scheduled updates...")
    print("📅 Updates scheduled at: 8:00 AM, 4:00 PM, 12:00 AM IST")
    
    # Start the bot
    application.run_polling(allowed_updates=['message', 'callback_query'])

if __name__ == '__main__':
    main()
