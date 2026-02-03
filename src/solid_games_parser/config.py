import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SOLID_GAMES_URL = "https://sg.zone/"
FEED_ITEM_PARSE_LIMIT = 10
ALLOWED_TITLES = (
    "Анонс игр",
    "СЕРЬЕЗНЫЕ МЕЙСЫ",
    "Games announcement"
)

SIDE_EMOJI = {
    "red": "🔴",
    "blue": "🔵",
    "yellow": "🟡",
    "green": "🟢",
    }

SELECTORS = {
    "feed_item": ".feed-item",
    "section_header_title": ".section-header-title",
    "tabs_container": ".row.tabs",
    "tab_button": ".btn-tab",
    "mission_block": ".feed-padding",
    "mission_desc_item": ".mission-desc-item",
    "preview_spoiler": ".preview-spoiler-body",
    "desktop_tab_name": ".desktop-item",
    "map": ".sg-map",
    "time": ".sg-clock, .sg-cloud",
    "users": ".sg-users",
    "equipment": ".sg-car"
}