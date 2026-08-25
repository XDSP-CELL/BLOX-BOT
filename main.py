import os
import requests
from bs4 import BeautifulSoup
import telebot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def fetch_gamersberg_stock():
    url = "https://www.gamersberg.com/blox-fruits/stock"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"❌ Website se connect nahi ho paya. (Status: {response.status_code})"

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Page ke sabhi text elements ya cards nikalna
        elements = soup.find_all(['div', 'span', 'p', 'h3', 'strong'])
        
        stock_list = []
        for el in elements:
            text = el.get_text(strip=True)
            # Agar text mein fruits ya stock se judi cheezein hain
            if text and len(text) < 40:
                if any(keyword in text.lower() for keyword in ['dragon', 'kitsune', 'dough', 't-rex', 'mammoth', 'venom', 'spirit', 'control', 'shadow', 'blizzard', 'sound', 'pain', 'gravity', 'phoenix', 'portal', 'rumble', 'magma', 'stock', 'level', 'in stock', 'out of stock']):
                    if text not in stock_list:
                        stock_list.append(text)

        if stock_list:
            formatted_stock = "\n• ".join(stock_list[:15])
            return f"🔥 *Gamersberg Blox Fruits Stock:*\n\n• {formatted_stock}"
        else:
            # Agar direct tags na milein, toh page ka sara visible text check kar lenge
            body_text = soup.get_text(separator="\n", strip=True)
            lines = [line for line in body_text.split("\n") if len(line) < 30 and line.strip()]
            return f"📌 *Page Content Detected:*\n\n" + "\n".join(lines[:15])

    except Exception as e:
        return f"❌ Scraping Error: {e}"

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Bot active hai! Stock dekhne ke liye /stock bhejein.")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    bot.reply_to(message, "⏳ Gamersberg se live stock check kiya ja raha है...")
    stock_text = fetch_gamersberg_stock()
    bot.send_message(message.chat.id, stock_text, parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
