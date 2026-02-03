


<img src="https://sg.zone/img/solidgames.jpg">
<h1 align=center>Solid Games Announcements Parser </h1>

<p align=center><a href="https://sg.zone/">Solid Games</a> is a large Arma 3 gaming community and project specializing in large-scale tactical missions.</p>
<p align=center>A Python parser for extracting mission in announcements from official SG site.</p>

## Features

- **Web Scraping**: Extracts game announcements using Selenium + BeautifulSoup
- **Structured Parsing**: Parses missions with per-server sides, vehicles, maps, weathers(time), and descriptions
- **Latest Announcement**: Quick access to the newest game announcement
- **Telegram Bot**: Interactive `/missions` command with inline keyboard navigation (4 buttons)
- **Backwards Compatible**: Supports both per-server structure and flat vehicles format

## Installation

### Prerequisites

- Python 3.13+
- Poetry (for dependency management)
- Telegram bot token (from [@BotFather](https://t.me/botfather))

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd SolidGamesParser
```

2. Install dependencies using Poetry:

```bash
poetry install
```

3. Create a `.env` file in `src/solid_games_parser/`:

```env
TELEGRAM_TOKEN=your_bot_token_here
```


## Dependencies

- **selenium** ≥4.40.0 — Web browser automation
- **aiogram** ≥3.24.0 — Telegram bot framework
- **beautifulsoup4** — HTML parsing
- **python-dotenv** — Environment variable loading

Optional:

- **webdriver-manager** — Auto-download compatible ChromeDriver
- **pytest** — Testing framework

## Testing

Run tests using pytest:

```bash
poetry run pytest tests/ -q
poetry run pytest tests/test_run.py -v
```

Tests use a `DummyDriver` mock to avoid real Selenium/browser requirements.

## License

MIT
