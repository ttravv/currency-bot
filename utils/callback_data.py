from aiogram.filters.callback_data import CallbackData


class Valute(CallbackData, prefix="valute"):
    valute: str

