import json

def read(path: str) -> dict:
    """
    Загружает данные из JSON-файла.

    :param path: Путь к JSON-файлу.
    :return: Данные, загруженные из файла.
    """
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)
