import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Blox Fruits ke saare fruits ki complete list emojis ke sath
ALL_FRUITS = [
    "🍎 Rocket",
    "🔄 Spin",
    "🗡️ Blade (Chop)",
    "🔔 Spring",
    "💣 Bomb",
    "💨 Smoke",
    "🦅 Spike",
    "🔥 Flame",
    "🧊 Ice",
    "🦅 Falcon",
    "🏜️ Sand",
    "✨ Dark",
    "💎 Diamond",
    "💡 Light",
    "ゴム Rubber",
    "🚧 Barrier",
    "👻 Ghost",
    "🌋 Magma",
    "📿 Quake",
    "❤️ Love",
    "🕷️ Spider",
    "🎵 Sound",
    "⛩️ Phoenix",
    "🌀 Portal",
    "⚡ Lightning",
    "🐾 Pain",
    "❄️ Blizzard",
    "🧘 Buddha",
    "🧬 Control",
    "🦇 Shadow",
    "💉 Venom",
    "👻 Spirit",
    "🍩 Dough",
    "🦖 T-Rex",
    "🦣 Mammoth",
    "🐉 Dragon",
    "🦊 Kitsune",
    "🐆 Leopard",
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
        InlineKeyboardButton("📦 Check Stock", callback_data="show_stock")
    )
    bot.reply_to(message, "👇 Niche diye gaye button par click karke stock dekhein:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "show_stock":
        # Saari list ko format kar rahe hain
        fruit_list = "\n• ".join(ALL_FRUITS)
        footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"
        
        response_text = f"🔥 *Blox Fruits Complete List / Stock:*\n\n• {fruit_list}{footer_text}"
        
        bot.answer_callback_query(call.id, "Stock load ho gaya!")
        bot.send_message(call.message.chat.id, response_text, parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
