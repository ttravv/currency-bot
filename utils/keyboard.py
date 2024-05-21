from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from utils.currency import valutes
from utils.callback_data import Valute
from utils.currency import cb_response

def valute_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for i in valutes:
        builder.add(
            types.InlineKeyboardButton(text=i, callback_data=Valute(valute = i).pack())
        )

    builder.adjust(3)
    
    return builder

def exchange_rate(char_code: str) -> str:
    for dct in cb_response:
        if (dct['CharCode'] == char_code):
            return dct['Value']