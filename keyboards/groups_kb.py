from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_groups_keyboard(*args: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для групп с заданными кнопками.

    :param args: Названия кнопок для групп.
    :return: Объект InlineKeyboardMarkup с кнопками.
    """
    kb_builder = InlineKeyboardBuilder()
    
    buttons = [
        InlineKeyboardButton(
            text=button,
            callback_data=f'{button}callgroup'
        ) for button in args
    ]
    
    kb_builder.row(*buttons, width=2)
    
    return kb_builder.as_markup()
