from peewee import Model, CharField, FloatField, IntegerField, TextField

from .base import db


# Базовая модель
class Base(Model):
    class Meta:
        database = db


# Модель запроса
class Request(Base):
    request_id = IntegerField(primary_key=True)

    tg_user_id = IntegerField()
    tg_user_phone = CharField(default="-")

    location_addr = CharField(default="-")
    location_longitude = FloatField(default=0)
    location_latitude = FloatField(default=0)
    location_type = CharField(default="-")
    location_flat = CharField(default="-")
    location_room = CharField(default="-")
    building_num = CharField(default="-")

    description = TextField(default="-")


# Функция создания таблиц
def create_tables():
    db.create_tables([Request])
