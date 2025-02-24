import asyncio
import requests
import random
import schedule
import time
import os
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)
LEETCODE_API = "https://leetcode.com/api/problems/algorithms/"

def get_random_problem():
    response = requests.get(LEETCODE_API)
    data = response.json()
    problems = [
        p for p in data["stat_status_pairs"]
        if p["difficulty"]["level"] in [1, 2]  # 1 = Easy, 2 = Medium
    ]
    problem = random.choice(problems)
    title = problem["stat"]["question__title"]
    link = f"https://leetcode.com/problems/{problem['stat']['question__title_slug']}/"
    return f"💡 Accept your weekly coding challenge:\n\n**{title}**\n🔗 {link}"

async def send_message_w_problem():
    message = get_random_problem()
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

async def send_reminder_wed():
    message = "⏳ Reminder: Have you already started solving this week's Leetcode problem?"
    await bot.send_message(chat_id=CHAT_ID, text=message)

async def send_reminder_fri():
    """Sends a reminder on Friday at 7 PM GMT+4 for the solution meeting."""
    message = "⏳ Reminder: After 1 hour we are meeting hereee to share our solutions!! Are you ready?"
    await bot.send_message(chat_id=CHAT_ID, text=message)

def run_scheduler():
    schedule.every().monday.at("08:00").do(lambda: asyncio.run(send_message_w_problem()))

    schedule.every().wednesday.at("08:00").do(lambda: asyncio.run(send_reminder_wed()))

    schedule.every().friday.at("15:00").do(lambda: asyncio.run(send_reminder_fri()))

    print("Scheduler started... Bot is running.")
    while True:
        schedule.run_pending()
        time.sleep(60)  

run_scheduler()
