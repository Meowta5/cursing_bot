from dataclasses import dataclass
from os.path import dirname, join
from environs import Env

import utils.json_function as js_func


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_id: int  # id администратора бота


@dataclass
class Config:
    tg_bot: TgBot
    student_groups: dict[str, list[str]]
    curses: list[str]


def load_config(path: str | None = None) -> Config:
    """
    Читает файл .env и возвращает экземпляр класса Config с заполненными полями token и admin_ids.
    """
    env = Env()
    env.read_env(path)
    
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_id=int(env('ADMIN_ID'))
        ),
        student_groups=js_func.read(join(dirname(__file__), 'student_groups.json')),
        curses=js_func.read(join(dirname(__file__), 'curses.json'))
    )
