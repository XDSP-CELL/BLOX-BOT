import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Blox Fruits ke latest stock items emojis ke sath
CURRENT_STOCK = [
    "🗡️ Blade (Chop)",
    "💨 Smoke",
    "🔥 Flame",
    "👻 Ghost",
    "🧊 Ice",
    "💡 Light",
    "🌋 Magma",
    "🧘 Buddha",
    "🌀 Portal",
    "⚡ Lightning",
    "🍩 Dough",
    "🦊 Kitsune",
    "❄️ Yeti",
    "⛽ Gas"
]

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Bot active hai! Stock check karne ke liye /stock bhejein.")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("📦 Check Live Stock", callback_data="show_stock")
    )
    bot.reply_to(message, "👇 Niche diye gaye button par click karke current stock dekhein:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "show_stock":
        fruit_list = "\n• ".join(CURRENT_STOCK[:8]) # Top active stock items
        footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"
        
        response_text = f"🔥 *Blox Fruits Current Stock:*\n\n• {fruit_list}{footer_text}"
        
        bot.answer_callback_query(call.id, "Stock load ho gaya!")
        bot.send_message(call.message.chat.id, response_text, parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
