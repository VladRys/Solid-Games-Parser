import logging
import html as _html
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from config import SOLID_GAMES_URL, SIDE_EMOJI

class TelegramBot:
    def __init__(self, token: str, parser):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.router = Router()
        self.parser = parser

        self._register_handlers()
        self.dp.include_router(self.router)

    def _register_handlers(self):
        @self.router.message(Command("start"))
        async def start_handler(message: Message):
            await message.answer("Бот запущен ✅")

        @self.router.message(Command("missions"))
        async def missions_handler(message: Message):
            latest = self.parser.parse_latest()
            if not latest:
                await message.answer("Анонс не найден.")
                return

            missions = latest.get("missions", [])
            if not missions:
                await message.answer("В анонсе нет миссий.")
                return

            labels = ["I", "II", "III", "IV"]
            buttons = [InlineKeyboardButton(text=lab, callback_data=f"mission:{i}") for i, lab in enumerate(labels)]
            keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons, [InlineKeyboardButton(text="Посмотреть на сайте", url=SOLID_GAMES_URL)]])

            text = self._format_mission(missions, 0, latest.get("title"))
            await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)

        @self.router.callback_query(lambda c: c.data and c.data.startswith("mission:"))
        async def mission_callback(query: CallbackQuery):
            await query.answer()
            try:
                idx = int(query.data.split(":", 1)[1])
            except Exception:
                await query.message.answer("Неверная кнопка")
                return

            latest = self.parser.parse_latest()
            if not latest:
                return

            missions = latest.get("missions", [])
            if idx < 0 or idx >= len(missions):
                await query.answer("Миссия недоступна", show_alert=True)
                return

            text = self._format_mission(missions, idx, latest.get("title"))
            labels = ["I", "II", "III", "IV"]
            buttons = [InlineKeyboardButton(text=lab, callback_data=f"mission:{i}") for i, lab in enumerate(labels)]
            keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons, [InlineKeyboardButton(text="Посмотреть на сайте", url=SOLID_GAMES_URL)]])
            

            await query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)

    def _format_mission(self, missions, idx: int, announcement_title: str | None = None) -> str:
        m = missions[idx]
        name = m.get("name", "Неизвестно")
        info = m.get("info", {})

        parts: list[str] = []

        def esc(text: str) -> str:
            return _html.escape(text or "")

        def side_emoji(side: str, default: str) -> str:
            side_l = side.lower()
            return next((e for k, e in SIDE_EMOJI.items() if k in side_l), default)

        def add_header(text: str):
            parts.append(text)

        def add_lines(lines: list[str]):
            parts.extend(lines)

        def format_sides(sides: dict[str, str]):
            for side, val in sides.items():
                emoji = side_emoji(side, "⚪")
                lines = [l.strip() for l in val.split("\n") if l.strip()]
                if not lines:
                    continue
                main = lines[0]
                if len(lines) > 1:
                    add_lines([f"{emoji}{esc(main)} — ⚔️ Атака"])
                else:
                    add_lines([f"{emoji}{esc(main)}"])

        def format_equipment(equipment: dict[str, str]):
            for side, val in equipment.items():
                emoji = side_emoji(side, "📦")
                add_lines([f"\n{emoji} <b>Техника:</b>", esc(val)])

        if announcement_title:
            add_header(f"📢 <b>{esc(announcement_title)}</b>\n")

        add_header(f"🎯 <b>Миссия:</b> {esc(name)}\n")

        if info.get("map"):
            add_header(f"🗺 <b>Карта:</b> {esc(info['map'])}")
        if info.get("time"):
            add_header(f"☁️ <b>Погода и время:</b> {esc(info['time'])}")

        if info.get("description"):
            add_header("\n📝 <b>Описание:</b>")
            add_header(esc(info["description"].get("text", "")))

        for srv in info.get("servers", []):
            add_header(f"\n🖥 <b>{esc(srv.get('name', 'Сервер'))}\n</b>")
            format_sides(srv.get("sides", {}))
            format_equipment(srv.get("equipment", {}))

        return "\n".join(parts)



    async def run(self):
        logging.basicConfig(level=logging.INFO)
        await self.dp.start_polling(self.bot)
