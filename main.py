import os
import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_live_gamersberg_stock(stock_type):
    url = "https://www.gamersberg.com/blox-fruits/stock"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"❌ Website se connect nahi ho paya. (Status: {response.status_code})"

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Website ke elements se stock items dhoondhna
        stock_items = []
        
        # Normal ya Mirage section ko target karne ke liye headings ya containers dekhenge
        for card in soup.find_all(['div', 'tr', 'li', 'span', 'p'], class_=True):
            text = card.get_text(separator=" ", strip=True)
            # Agar text ke andar fruits ya stock se judi cheezein hain aur lambai theek hai
            if any(f in text.lower() for f in ['kitsune', 'dragon', 't-rex', 'mammoth', 'dough', 'spirit', 'control', 'venom', 'shadow', 'blizzard', 'portal', 'buddha', 'phoenix', 'sound', 'pain', 'rumble', 'magma', 'ice', 'light', 'quake', 'love', 'spider']):
                if text not in stock_items and len(text) < 60:
                    stock_items.append(text)

        footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"

        if stock_items:
            # Jo items mile hain unhe list ki tarah format kar denge
            formatted_list = "\n• ".join(stock_items[:10])
            return f"🔥 *Gamersberg {stock_type} Live Stock:*\n\n• {formatted_list}{footer_text}"
        else:
            # Fallback agar direct items na milein toh page ka main text dikha denge
            return f"⚠️ {stock_type} stock abhi load ho raha hai ya website ka structure badla hai.{footer_text}"

    except Exception as e:
        footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"
        return f"❌ Error: {e}{footer_text}"

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Bot active hai! Stock check karne ke liye /stock bhejein.")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("📦 Normal Stock", callback_data="Normal"),
        InlineKeyboardButton("✨ Mirage Stock", callback_data="Mirage")
    )
    bot.reply_to(message, "👇 Kiska stock dekhna chahte hain, select karein:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    stock_type = call.data  # 'Normal' ya 'Mirage'
    bot.answer_callback_query(call.id, f"{stock_type} live stock fetch kiya ja raha hai...")
    
    stock_text = get_live_gamersberg_stock(stock_type)
    bot.send_message(call.message.chat.id, stock_text, parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
