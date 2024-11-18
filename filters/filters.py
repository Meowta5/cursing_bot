from aiogram import Router
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher


class IsAdmin(BaseFilter):
    async def __call__(self, callback: CallbackQuery | Message, admin_id: int) -> bool:
        return callback.from_user.id == admin_id


class IsCallGroup(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        """
        Проверяет, заканчивается ли callback.data на 'callgroup'.

        :param callback: Объект CallbackQuery.
        :return: True, если callback.data заканчивается на 'callgroup', иначе False.
        """
        return callback.data.endswith('callgroup')


class IsStudent(BaseFilter):
    async def __call__(self, callback: CallbackQuery, student_groups: dict) -> bool:
        """
        Проверяет, является ли пользователь студентом.

        :param callback: Объект CallbackQuery.
        :param student_groups: Словарь групп студентов.
        :return: True, если callback.data заканчивается на 'student', иначе False.
        """
        return callback.data.endswith('student')
