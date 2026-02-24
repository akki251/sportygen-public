from flask import Flask
import os
import threading
from scheduled_bot import main as run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "🎾 Sportygen Bot is running!"

@app.route('/health')
def health():
    return {"status": "healthy", "bot": "running"}

if __name__ == '__main__':
    # Run bot in a separate thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Run Flask server for Render
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
