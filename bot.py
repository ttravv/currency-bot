import asyncio
import logging
import time
from dotenv import dotenv_values
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from utils.keyboard import valute_kb, exchange_rate
from utils.callback_data import Valute


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = dotenv_values(".env")
bot = Bot(token=config["BOT_TOKEN"])
dp = Dispatcher()


@dp.message(Command("start"))
async def start_button(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Узнать время"),
            types.KeyboardButton(text="Узнать курс валюты"),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите команду", reply_markup=keyboard)


@dp.message(F.text == "Узнать время")
async def timer(message: types.Message):
    valid_time = time.strftime("%m/%d/%Y, %H:%M:%S")
    await message.answer(f"Сейчас: {valid_time}")


@dp.message(F.text == "Узнать курс валюты")
async def currency_handler(message: types.Message):
    valute_keyboard = valute_kb()
    await message.answer("Выберите Валюту", reply_markup=valute_keyboard.as_markup())


@dp.callback_query(Valute.filter())
async def exchange_rate_response(callback: types.CallbackQuery, callback_data: Valute):
    valute_exchange_rate = exchange_rate(callback_data.valute)
    await callback.message.answer(
        f"Курс {callback_data.valute} к RUB: {valute_exchange_rate}"
    )
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
