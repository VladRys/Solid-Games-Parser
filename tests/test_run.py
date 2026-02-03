from pathlib import Path
from solid_games_parser.parser import SolidGamesParser

class DummyDriver:
    def __init__(self, html: str):
        self.page_source = html


def test_parse_latest_from_local_html():
    root = Path(__file__).parent
    html_path = root / "test.html"
    html = html_path.read_text(encoding="utf-8")

    driver = DummyDriver(html)
    parser = SolidGamesParser(driver)
    latest = parser.parse_latest()

    assert latest is not None
    assert "title" in latest
    assert "missions" in latest
    assert isinstance(latest["missions"], list)
    assert len(latest["missions"]) > 0


if __name__ == '__main__':
    test_parse_latest_from_local_html()
