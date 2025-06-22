import telebot
from telebot import types
import random
import time

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_USERNAME = "@memclasic"
TON_WALLET = "UQAWFliR3tChdxdKfV9ieM4MBcCy1-eNlNUwyRqUyecIEKn"

bot = telebot.TeleBot(BOT_TOKEN)

users = {}
referrals = {}

# Daily task generator
def generate_tasks():
    return [
        {"task": "Tap 100 times", "reward": 0.1},
        {"task": "Watch 3 ads", "reward": 0.05},
        {"task": "Invite a friend", "reward": 0.05},
    ]

daily_tasks = generate_tasks()

# Helper functions
def post_daily_tasks():
    msg = "🎯 *MemClasic Daily Tasks*\n"
    for t in daily_tasks:
        msg += f"✅ {t['task']} → +{t['reward']} MEMC\n"
    msg += "\n🚀 Start earning: https://t.me/daaesco_bot"
    bot.send_message(CHANNEL_USERNAME, msg, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"balance": 0, "taps": 0}
        args = message.text.split()
        if len(args) > 1:
            ref = args[1]
            if ref != str(user_id):
                ref_id = int(ref)
                if ref_id in users:
                    users[ref_id]["balance"] += 0.001
                    users[user_id]["balance"] += 0.001
                    bot.send_message(ref_id, f"🎉 You earned 0.001 MEMC for inviting!")
                    bot.send_message(user_id, f"🎉 You earned 0.001 MEMC for joining via referral!")
    bot.send_message(user_id, f"Welcome to MemClasic! Your balance: {users[user_id]['balance']} MEMC\nJoin our channel: {CHANNEL_USERNAME}")

@bot.message_handler(commands=['tap'])
def tap(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"balance": 0, "taps": 0}
    users[user_id]["taps"] += 1
    users[user_id]["balance"] += 0.0001
    bot.send_message(user_id, f"Tap recorded! Balance: {users[user_id]['balance']:.4f} MEMC")

@bot.message_handler(commands=['tasks'])
def tasks(message):
    user_id = message.from_user.id
    msg = "🎯 *Today's Tasks*\n"
    for t in daily_tasks:
        msg += f"✅ {t['task']} → +{t['reward']} MEMC\n"
    bot.send_message(user_id, msg, parse_mode="Markdown")
    bot.send_message(user_id, f"📢 Stay updated here: {CHANNEL_USERNAME}")

@bot.message_handler(commands=['withdraw'])
def withdraw(message):
    user_id = message.from_user.id
    if users[user_id]["balance"] < 1:
        bot.send_message(user_id, "❌ Minimum withdrawal is 1 MEMC.")
    else:
        bot.send_message(user_id, f"✅ Withdrawal request received. You will get your MEMC in your TON wallet: {TON_WALLET}")
        users[user_id]["balance"] = 0

post_daily_tasks()
bot.infinity_polling()
