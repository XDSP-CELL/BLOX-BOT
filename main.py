import os
import requests
from bs4 import BeautifulSoup
import telebot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_fruityblox_stock():
    url = "https://fruityblox.com/stock"
    # Ekdum real browser jaisa User-Agent aur headers dena padta hai taaki website block na kare
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        # Agar block ho gaya ya error aaya
        if response.status_code != 200:
            return f"❌ Website ne block kar diya! (Status Code: {response.status_code})"

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Website ke text elements se fruit names dhoondhne ki koshish
        found_fruits = []
        
        # Popular fruits ki list jinko hum page par talash karenge
        target_fruits = [
            "Kitsune", "Dragon", "T-Rex", "Mammoth", "Dough", "Spirit", 
            "Venom", "Shadow", "Control", "Buddha", "Blizzard", "Portal", 
            "Lightning", "Rumble", "Sound", "Pain", "Phoenix", "Magma", "Yeti", "Gas"
        ]

        page_text = soup.get_text()
        for fruit in target_fruits:
            if fruit.lower() in page_text.lower() and fruit not in found_fruits:
                found_fruits.append(fruit)

        footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"

        if found_fruits:
            fruit_list = "\n• ".join(found_fruits[:8])
            return f"🔥 *FruityBlox Live Stock Detected:*\n\n• {fruit_list}{footer_text}"
        else:
            return f"⚠️ Site khul gayi par fruits ke naam match nahi hue. (Structure change ho sakta hai){footer_text}"

    except Exception as e:
        footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"
        return f"❌ Error: {e}{footer_text}"

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Bot active hai! Stock check karne ke liye /stock bhejein.")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    bot.reply_to(message, "⏳ FruityBlox se live stock check kiya ja raha hai...")
    stock_text = get_fruityblox_stock()
    bot.send_message(message.chat.id, stock_text, parse_mode='Markdown')

print("Telegram bot polling shuru ho rahi hai...")
bot.infinity_polling(skip_pending=True)
