import asyncio
import json
from bot import TelegramBot
from config import TELEGRAM_TOKEN
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from parser import SolidGamesParser

if __name__ == "__main__":
    options = Options()
    options.add_argument("--lang=ru-RU")
    options.add_argument("--start-maximized")
    options.add_experimental_option(
        "prefs", {"intl.accept_languages": "ru,ru-RU"}
    )

    driver = Chrome(options=options)

    parser = SolidGamesParser(driver)
    parser.load_page()

    bot = TelegramBot(TELEGRAM_TOKEN, parser)
    asyncio.run(bot.run())

