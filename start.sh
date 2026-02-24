#!/bin/bash

# Load environment variables
export $(cat .env | xargs)

# Run the bot
python telegram_bot.py
