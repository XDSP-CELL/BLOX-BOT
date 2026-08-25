import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 41 Fruits ki Complete Normal List (Tiger aur Lightning updated)
NORMAL_FRUITS = [
    "🍎 Rocket", "🔄 Spin", "🗡️ Blade (Chop)", "🔔 Spring", "💣 Bomb",
    "💨 Smoke", "🦅 Spike", "🔥 Flame", "🧊 Ice", "🦅 Falcon",
    "🏜️ Sand", "✨ Dark", "💎 Diamond", "💡 Light", "ゴム Rubber",
    "🚧 Barrier", "👻 Ghost", "🌋 Magma", "📿 Quake", "❤️ Love",
    "🕷️ Spider", "🎵 Sound", "⛩️ Phoenix", "🌀 Portal", "⚡ Lightning",
    "🐾 Pain", "❄️ Blizzard", "🧘 Buddha", "🧬 Control", "🦇 Shadow",
    "💉 Venom", "👻 Spirit", "🍩 Dough", "🦖 T-Rex", "🦣 Mammoth",
    "🐉 Dragon", "🦊 Kitsune", "🐅 Tiger", "❄️ Yeti", "⛽ Gas", "🌟 Custom/Extra Fruit"
]

# 41 Fruits ki Complete Mirage List (Tiger aur Lightning updated)
MIRAGE_FRUITS = [
    "🍎 Rocket (Mirage)", "🔄 Spin (Mirage)", "🗡️ Blade (Mirage)", "🔔 Spring (Mirage)", "💣 Bomb (Mirage)",
    "💨 Smoke (Mirage)", "🦅 Spike (Mirage)", "🔥 Flame (Mirage)", "🧊 Ice (Mirage)", "🦅 Falcon (Mirage)",
    "🏜️ Sand (Mirage)", "✨ Dark (Mirage)", "💎 Diamond (Mirage)", "💡 Light (Mirage)", "ゴム Rubber (Mirage)",
    "🚧 Barrier (Mirage)", "👻 Ghost (Mirage)", "🌋 Magma (Mirage)", "📿 Quake (Mirage)", "❤️ Love (Mirage)",
    "🕷️ Spider (Mirage)", "🎵 Sound (Mirage)", "⛩️ Phoenix (Mirage)", "🌀 Portal (Mirage)", "⚡ Lightning (Mirage)",
    "🐾 Pain (Mirage)", "❄️ Blizzard (Mirage)", "🧘 Buddha (Mirage)", "🧬 Control (Mirage)", "🦇 Shadow (Mirage)",
    "💉 Venom (Mirage)", "👻 Spirit (Mirage)", "🍩 Dough (Mirage)", "🦖 T-Rex (Mirage)", "🦣 Mammoth (Mirage)",
    "🐉 Dragon (Mirage)", "🦊 Kitsune (Mirage)", "🐅 Tiger (Mirage)", "❄️ Yeti (Mirage)", "⛽ Gas (Mirage)", "🌟 Mirage Special"
]

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Bot active hai! Stock check karne ke liye /stock bhejein.")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    markup = InlineKeyboardMarkup()
    # Normal aur Mirage ke buttons
    markup.row(
        InlineKeyboardButton("🟢 Normal Stock", callback_data="normal_stock"),
        InlineKeyboardButton("✨ Mirage Stock", callback_data="mirage_stock")
    )
    # Website ka direct live link button
    markup.row(
        InlineKeyboardButton("🌐 Blox Fruit stock live (Website)", url="https://fruityblox.com/stock")
    )
    bot.reply_to(message, "👇 Niche diye gaye buttons mein se select karein:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"
    
    if call.data == "normal_stock":
        bot.answer_callback_query(call.id, "Normal stock load ho raha hai...")
        part1 = "\n• ".join(NORMAL_FRUITS[:20])
        part2 = "\n• ".join(NORMAL_FRUITS[20:])
        
        bot.send_message(call.message.chat.id, f"🔥 *Blox Fruit stock live (Normal - Part 1):*\n\n• {part1}", parse_mode='Markdown')
        bot.send_message(call.message.chat.id, f"🔥 *Blox Fruit stock live (Normal - Part 2):*\n\n• {part2}{footer_text}", parse_mode='Markdown')

    elif call.data == "mirage_stock":
        bot.answer_callback_query(call.id, "Mirage stock load ho raha hai...")
        part1 = "\n• ".join(MIRAGE_FRUITS[:20])
        part2 = "\n• ".join(MIRAGE_FRUITS[20:])
        
        bot.send_message(call.message.chat.id, f"✨ *Blox Fruit stock live (Mirage - Part 1):*\n\n• {part1}", parse_mode='Markdown')
        bot.send_message(call.message.chat.id, f"✨ *Blox Fruit stock live (Mirage - Part 2):*\n\n• {part2}{footer_text}", parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
