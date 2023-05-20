from .models import Request


# Функция созданияя заявки
def add_new_request(tg_user_id: int):
    Request(tg_user_id=tg_user_id).save()


# Функция получения заявки
def get_latest_request_by_tg_user(tg_user_id: int) -> Request:
    requsts_by_tgid = (
        Request.select()
        .where(Request.tg_user_id == tg_user_id)
        .order_by(Request.request_id.desc())
    )
    return requsts_by_tgid[0]


# Функции для обновления соответствующих полей таблицы в БД

def update_current_request_location_addr(tg_user_id: int, addr: str):
    latest_request = get_latest_request_by_tg_user(tg_user_id)
    latest_request.location_addr = addr
    latest_request.save()


def update_current_request_description(tg_user_id: int, description: str):
    latest_request = get_latest_request_by_tg_user(tg_user_id)
    latest_request.description = description
    latest_request.save()


def update_current_request_building(tg_user_id: int, building: str):
    latest_request = get_latest_request_by_tg_user(tg_user_id)
    latest_request.location_type = building
    latest_request.save()


def update_current_request_flat(tg_user_id: int, flat: str):
    latest_request = get_latest_request_by_tg_user(tg_user_id)
    latest_request.location_flat = flat
    latest_request.save()


def update_current_request_room(tg_user_id: int, room: str):
    latest_request = get_latest_request_by_tg_user(tg_user_id)
    latest_request.location_room = room
    latest_request.save()


def update_current_request_building_num(tg_user_id: int, num: str):
    latest_request = get_latest_request_by_tg_user(tg_user_id)
    latest_request.building_num = num
    latest_request.save()


def update_current_request_geolocation(
    tg_user_id: int, latitude: float, longitude: float
):
    latest_request = get_latest_request_by_tg_user(tg_user_id)
    latest_request.location_latitude = latitude
    latest_request.location_longitude = longitude
    latest_request.save()

def update_current_request_phone(tg_user_id: int, phone: str):
    latest_request = get_latest_request_by_tg_user(tg_user_id)
    latest_request.tg_user_phone = phone
    latest_request.save()
