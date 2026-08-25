import os
import requests
from bs4 import BeautifulSoup
import telebot
from keep_alive import keep_alive
import threading

# Telegram Bot Token (Agar Render environment variable me set hai toh wahan se uthayega)
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
        items = soup.find_all('div', class_='stock-item')
        
        stock_list = []
        for item in items:
            stock_list.append(item.text.strip())
            
        if stock_list:
            formatted_stock = "\n• ".join(stock_list)
            return f"🔥 *Gamersberg Live Stock:*\n\n• {formatted_stock}"
        else:
            return "⚠️ Website khul gayi hai, par stock items ke tags nahi mile (Dynamic content ho sakta hai)."

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

# Flask web server ko background thread mein chalana
keep_alive()

# Telegram bot ko polling par shuru karna
print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
        
        stock_list = []
        for item in items:
            stock_list.append(item.text.strip())
            
        if stock_list:
            formatted_stock = "\n• ".join(stock_list)
            return f"🔥 *Gamersberg Live Stock:*\n\n• {formatted_stock}"
        else:
            return "⚠️ Website khul gayi hai, par stock items ke tags nahi mile (Dynamic JS content ho sakta hai)."

    except Exception as e:
        return f"❌ Scraping Error: {e}"

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Gamersberg Stock Bot Render par live ho gaya hai!\n\nStock dekhne ke liye /stock bhejein.")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    bot.reply_to(message, "⏳ Gamersberg se live stock check kiya ja raha hai...")
    stock_text = fetch_gamersberg_stock()
    bot.send_message(message.chat.id, stock_text, parse_mode='Markdown')

# Web server start karein taaki Render service active rahe
keep_alive()

bot.infinity_polling()
