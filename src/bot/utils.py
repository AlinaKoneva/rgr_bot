import os

from aiogram.types.photo_size import PhotoSize

from .config import BOT_CONFIG


# Функция сохранения изображений от пользователя
async def save_pics(photos: list[PhotoSize], uid: int, request_id: int):
    # Формируем папку, в котороую будем сохранять изображения
    f_dest = BOT_CONFIG.STATIC_FOLDER / str(uid) / str(request_id)

    if not os.path.exists(f_dest):
        os.makedirs(f_dest)

    await photos[-1].download(destination_file=f_dest/photos[-1].file_unique_id)


# Функция создания папки для картинок
def create_static_folder():
    if not os.path.exists(BOT_CONFIG.STATIC_FOLDER):
        os.makedirs(BOT_CONFIG.STATIC_FOLDER)
