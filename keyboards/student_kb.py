from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_students_keyboard(*args: str, last_btn: str | None = None) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для студентов с заданными кнопками.

    :param args: Названия кнопок для студентов.
    :param last_btn: Название последней кнопки (если есть).
    :return: Объект InlineKeyboardMarkup с кнопками.
    """
    kb_builder = InlineKeyboardBuilder()
    
    buttons = [
        InlineKeyboardButton(
            text=button,
            callback_data=f'{button}student'
        ) for button in args
    ]
    
    kb_builder.row(*buttons, width=3)
    
    if last_btn:
        kb_builder.row(
            InlineKeyboardButton(
                text=last_btn,
                callback_data=f'{last_btn}student'
            )
        )
        
    return kb_builder.as_markup()
