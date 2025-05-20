import requests
from bs4 import BeautifulSoup
from telegram import Bot

# === Config ===
BOT_TOKEN = "7723643158:AAExHhBvnRmF3t97mKIP0se7LzOPkgVNjoM"
CHANNEL_ID = -1001234567890  # Replace with your channel ID
MOVIE_URL = "https://hdhub4u.football/once-upon-a-time-in-madras-2024-uncut-hindi-webrip-full-movie/"

# === Telegram Bot ===
bot = Bot(token=BOT_TOKEN)

# === Scraper Function ===
def scrape_hdhub4u(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title
    title_tag = soup.find("h1", class_="entry-title")
    title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

    # Try to find any DDL links (.mkv or .r2.dev)
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.endswith(".mkv") or "r2.dev" in href:
            links.append(href)

    # Fallback: show any Google Drive style /hub links
    if not links:
        for a in soup.find_all("a", href=True):
            if "hub" in a["href"] or "file" in a["href"]:
                links.append(a["href"])

    return title, links

# === Main Function ===
def main():
    title, ddl_links = scrape_hdhub4u(MOVIE_URL)
    if not ddl_links:
        print("No DDL links found.")
        return

    message = f"🎬 <b>{title}</b>\n\n"
    message += "📦 <b>DDL Links:</b>\n"
    for link in ddl_links:
        message += f"<code>{link}</code>\n"

    bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
    print("Posted to Telegram successfully!")

if __name__ == "__main__":
    main()
