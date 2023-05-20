from pathlib import Path
from pydantic import BaseSettings


# Сообщения для бота
MESSAGES = {
    "START": (
        'Привет!\n'
        'Я - бот для формирования заявок о неисправностях в НГТУ. '
        'Чтобы добавить заявку - нажми на кнопку "Добавить".'
    ),
    "DESCRIPTION": "Опишите проблему",
    "CHOOSE_GEOLOC": "Опишите место происшествия (Адрес или геолокация)",
    "ADD_GEOLOC": "Добавьте геолокацию",
    "ADD_PHONE": "Добавьте номер телефона для связи",
    "WHERE": "Выберите, где обнаружена неисправность",
    "ADD_ADDR": "Введите адрес здания",
    "ADD_FLAT": "Введите номер этажа",
    "ADD_ROOM": "Введите номер комнаты или кабинета",
    "ADD_PHOTO": "Прикрепите фото неисправности",
    "ADD_BUILDING": "Выберите номер корпуса",
    "SUCCESS": lambda num: (
        f"Ваша заявка успешно отправлена! Номер заявки: {num}. Ждите результата."
    ),
    "ERROR": lambda num: (
        "При отправке заявки произошла ошибка. "
        f"Номер заявки: {num}. Для уточнения проблемы обратитесь к администратору."
    ),
}


class BotConfig(BaseSettings):
    # Токен для бота от BotFather
    TOKEN: str
    # Корневая папка проекта
    ROOT_FOLDER: Path = Path(__file__).parents[2].absolute()
    # Папка для хранения изображений
    STATIC_FOLDER: Path = ROOT_FOLDER / "static/"
    # Тип базы данных (sqlite, postgresql, ...). Необходим для src/db/base.py
    DB_TYPE: str = "sqlite"
    # Название файла базы данных
    DB_FILE: str = "db.sqlite"

    class Config:
        # Название файла конфигураций
        env_file = ".env"


class PostgresConfig(BaseSettings):
    # Конфигурация БД postgresql
    DB: str = "ngtu_db"
    USER: str = "ngtu_user"
    PASSWD: str = "passwd"
    HOST: str = "localhost"
    PORT: int = 5432


# Создание экземпляров классов конфигураций
BOT_CONFIG = BotConfig()  # type:ignore
PG_CONFIG = PostgresConfig()  # type:ignore
