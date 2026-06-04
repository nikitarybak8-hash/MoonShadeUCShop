import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8137793242:AAEuaCQ9AujBPjn_QICW_lPNvruJWSwJ4bM"
ADMIN_ID = 8912113059

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Order(StatesGroup):
    waiting_uid = State()


prices = {
    "60 UC": "42 грн",
    "120 UC": "84 грн",
    "325 UC": "210 грн",
    "660 UC": "410 грн",
    "1800 UC": "1005 грн",
    "3850 UC": "2010 грн",
    "8100 UC": "4020 грн",
    "16200 UC": "8020 грн"
}


@dp.message(CommandStart())
async def start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="60 UC"), KeyboardButton(text="120 UC")],
            [KeyboardButton(text="325 UC"), KeyboardButton(text="660 UC")],
            [KeyboardButton(text="1800 UC"), KeyboardButton(text="3850 UC")],
            [KeyboardButton(text="8100 UC"), KeyboardButton(text="16200 UC")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🌙 MoonShade UC Shop\n\n"
        "Оберіть пакет UC:",
        reply_markup=kb
    )


@dp.message(F.text.in_(prices.keys()))
async def choose_package(message: Message, state: FSMContext):
    await state.update_data(
        package=message.text,
        price=prices[message.text]
    )

    await state.set_state(Order.waiting_uid)

    await message.answer(
        f"Обрано: {message.text}\n"
        f"Ціна: {prices[message.text]}\n\n"
        "Введіть ваш PUBG UID:"
    )


@dp.message(Order.waiting_uid)
async def get_uid(message: Message, state: FSMContext):
    uid = message.text

    data = await state.get_data()

    text = (
        "🛒 НОВЕ ЗАМОВЛЕННЯ\n\n"
        f"👤 Telegram: @{message.from_user.username}\n"
        f"🆔 UID PUBG: {uid}\n"
        f"💎 Пакет: {data['package']}\n"
        f"💰 Сума: {data['price']}"
    )

    await bot.send_message(ADMIN_ID, text)

    await message.answer(
        "✅ Заявка створена!\n\n"
        "💳 Оплата:\n"
        "4149 4990 8132 1851\n\n"
        "Після оплати очікуйте підтвердження."
    )

    await state.clear()


async def main():
    print("MoonShade UC Shop запущено")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
