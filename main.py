import os
import requests
from bs4 import BeautifulSoup
import telebot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def fetch_gamersberg_stock():
    url = "https://gamersberg.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"❌ Website se connect nahi ho paya. (Status: {response.status_code})"

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Alag-alag common tags try karte hain jahan stock ya items ho sakte hain
        stock_items = []
        
        # 1. Pehle 'div' ya 'span' jinki class mein 'stock', 'product', ya 'item' ho
        for tag in soup.find_all(['div', 'span', 'h3', 'a'], class_=True):
            class_name = " ".join(tag.get('class'))
            if any(keyword in class_name.lower() for keyword in ['stock', 'product', 'item', 'fruit', 'card']):
                text = tag.text.strip()
                if text and len(text) < 50 and text not in stock_items:
                    stock_items.append(text)

        # Agar upar se kuch na mile, toh page ke saare headings (h1, h2, h3) nikal lo
        if not stock_items:
            for h in soup.find_all(['h1', 'h2', 'h3', 'strong']):
                text = h.text.strip()
                if text and len(text) < 50:
                    stock_items.append(text)

        if stock_items:
            # Sirf pehle 15-20 items dikhayein taaki message bahut lamba na ho
            formatted_stock = "\n• ".join(stock_items[:15])
            return f"🔥 *Gamersberg Live Stock (Detected):*\n\n• {formatted_stock}"
        else:
            return "⚠️ Website ka structure dynamic hai. Kripya dekhein ki kya wahan JavaScript se stock load ho raha hai."

    except Exception as e:
        return f"❌ Scraping Error: {e}"

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Bot active hai! Stock dekhne ke liye /stock bhejein.")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    bot.reply_to(message, "⏳ Gamersberg se live stock check kiya ja raha hai...")
    stock_text = fetch_gamersberg_stock()
    bot.send_message(message.chat.id, stock_text, parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
