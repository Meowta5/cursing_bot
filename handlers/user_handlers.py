from copy import deepcopy
import asyncio
from random import choice
from pprint import pprint

from aiogram import F, Router, Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from filters.filters import IsCallGroup, IsStudent, IsAdmin
from keyboards.groups_kb import create_groups_keyboard
from keyboards.student_kb import create_students_keyboard
from lexicon.lexicon import LEXICON

router = Router()
router.message.filter(IsAdmin())

# -------------------------------------------------------------------------------------------------
# Дальше Бога нет...
# -------------------------------------------------------------------------------------------------

# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    await message.answer(LEXICON['/start'])


# Этот хэндлер будет срабатывать на команду "/help"
@router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    await message.answer(LEXICON['/help'])


# Этот хэндлер будет срабатывать на команду "/restart"
@router.message(Command(commands='restart'))
async def process_restart_command(message: Message, student_groups: dict, 
                                    dispatcher: Dispatcher) -> None:
    await message.answer(
        LEXICON['/restart'], 
        reply_markup=create_groups_keyboard(*(list(student_groups.keys())))
    )
    dispatcher['current_group'] = []
    dispatcher['full_current_group'] = []


# Этот хэндлер будет срабатывать на команду "/play"
@router.message(Command(commands='play'))
async def process_play_command(message: Message, dispatcher: Dispatcher, 
                                curses: list) -> None:
    if not dispatcher['current_group']:
        if dispatcher['full_current_group']:
            dispatcher['current_group'] = deepcopy(dispatcher['full_current_group'])
        else:
            await message.answer(LEXICON['play_error'])
            return

    curse = choice(curses)
    student = choice(dispatcher['current_group'])
    dispatcher['current_group'].remove(student)

    await message.answer(
        text=(
            f"{LEXICON['curse_part_one']}{student}{LEXICON['curse_part_two']}\n"
            f"{LEXICON['curse_part_three']}{curse}{LEXICON['curse_part_four']}"
        )
    )


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с названием группы
@router.callback_query(IsCallGroup())
async def process_group_press(callback: CallbackQuery, dispatcher: Dispatcher, 
                               student_groups: dict, bot: Bot) -> None:
    group_name = callback.data[:-9]
    dispatcher['current_group'] = student_groups[group_name].copy()
    dispatcher['full_current_group'] = student_groups[group_name].copy()

    await bot.send_message(
        callback.from_user.id,
        LEXICON['group'],
        reply_markup=create_students_keyboard(
            *dispatcher['full_current_group'], last_btn=LEXICON['done']
        )
    )
    
    await bot.delete_message(chat_id=callback.from_user.id, 
                              message_id=callback.message.message_id)


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с именем пользователя
@router.callback_query(IsStudent())
async def process_students_press(callback: CallbackQuery, bot: Bot, 
                                  dispatcher: Dispatcher) -> None:
    student_name = callback.data[:-7]
    
    # Удаляем ученика из full_current_group
    dispatcher['full_current_group'] = [
        text for text in dispatcher['full_current_group'] if text != student_name
    ]
    
    if callback.data != f"{LEXICON['done']}student":
        inline_kb = create_students_keyboard(
            *dispatcher['full_current_group'], last_btn=LEXICON['done']
        )
        
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=inline_kb
        )
        await callback.answer()
    else:
        dispatcher['current_group'] = deepcopy(dispatcher['full_current_group'])

        await bot.send_message(callback.from_user.id, LEXICON['student_curse'])
        await bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id
        )
