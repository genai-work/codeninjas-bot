import requests
import asyncio
import random
import schedule
import time
import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TOKEN = "7080134470:AAEosQ1o36oW3OuRmqqPSTltGTbCJcLAM1k"
CHAT_ID = "-1002485084050"

bot = Bot(token=TOKEN)
LEETCODE_API = "https://leetcode.com/api/problems/algorithms/"

def get_random_problem():
    response = requests.get(LEETCODE_API)
    data = response.json()
    problems = [
        p for p in data["stat_status_pairs"]
        if p["difficulty"]["level"] in [1, 2]
    ]
    problem = random.choice(problems)
    title = problem["stat"]["question__title"]
    link = f"https://leetcode.com/problems/{problem['stat']['question__title_slug']}/"
    return f"💡 Accept your weekly coding challenge:\n**{title}**\n🔗 {link}"

async def send_message_w_problem():
    message = get_random_problem()
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

async def send_reminder_wed():
    await bot.send_message(chat_id=CHAT_ID, text="⏳ Reminder: Have you solved this week's Leetcode problem?")

async def send_reminder_fri():
    await bot.send_message(chat_id=CHAT_ID, text="⏳ Reminder: After 1 hour we are meeting hereee to share our solutions!! Are you ready?")

schedule.every().monday.at("12:00").do(asyncio(send_message_w_problem))
schedule.every().wednesday.at("12:00").do(asyncio(send_reminder_wed))
schedule.every().friday.at("12:00").do(asyncio(send_reminder_fri))

asyncio.run(send_message_w_problem())

while True:
    schedule.run_pending()
    time.sleep(60)
