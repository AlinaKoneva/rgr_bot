from peewee import PostgresqlDatabase, SqliteDatabase

from src.bot.config import BOT_CONFIG, PG_CONFIG


# Объект peewee для работы с БД postgresql
__pg_db = PostgresqlDatabase(
    database=PG_CONFIG.DB,
    user=PG_CONFIG.USER,
    password=PG_CONFIG.PASSWD,
    host=PG_CONFIG.HOST,
    port=PG_CONFIG.PORT,
)
# Объект peewee для работы с БД sqlite
__sl_db = SqliteDatabase(BOT_CONFIG.ROOT_FOLDER / BOT_CONFIG.DB_FILE)

# Выбираем, какой объект будем использовать в зависимости от 
# типа базы данных, указанного в конфигурационном файле
db = __sl_db if BOT_CONFIG.DB_TYPE == "sqlite" else __pg_db
