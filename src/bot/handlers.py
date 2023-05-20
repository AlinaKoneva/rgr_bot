from aiogram.types import Message, CallbackQuery, ContentTypes, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import MediaGroupFilter
from aiogram_media_group import media_group_handler

from src.db.utils import (
    add_new_request,
    update_current_request_room,
    update_current_request_flat,
    get_latest_request_by_tg_user,
    update_current_request_phone,
    update_current_request_building,
    update_current_request_description,
    update_current_request_geolocation,
    update_current_request_building_num,
    update_current_request_location_addr,
)
from src.services.api import mock_send_request_to_info_system

from .base import dp, bot, States
from .utils import save_pics
from .config import MESSAGES
from .keyboards import (
    LOCATIONS,
    start_kbrd_rkm,
    add_phone_kbrd,
    add_geoloc_kbrd,
    choose_loc_type,
    choose_geoloc_kbrd,
    choose_building_num_kbrd,
)


# обработчик комманды start
@dp.message_handler(state="*", commands=["start"])
async def start_bot(message: Message, state: FSMContext):
    # меняем состояние на добавление заявки add_request
    await state.set_state(States.add_request)  # type:ignore
    # Отпавляем соощение, прикрепляем клавиатуру
    await bot.send_message(
        message.from_user.id, MESSAGES["START"], reply_markup=start_kbrd_rkm)


# обработчик нажатия кнопки добавить при состоянии add_request
@dp.message_handler(lambda m: m.text == "Добавить", state=States.add_request)
async def add_request(message: Message, state: FSMContext):
    # создаем новую завявку в бд
    add_new_request(message.from_user.id)

    # меняем состояние на добавление картинки
    await state.set_state(States.add_pic)  # type:ignore
    await bot.send_message(
        message.from_user.id, MESSAGES["ADD_PHOTO"], reply_markup=ReplyKeyboardRemove())


# Обработчик добавления нескольких картинок
@dp.message_handler(
    MediaGroupFilter(is_media_group=True),
    state=States.add_pic,
    content_types=ContentTypes.PHOTO)
@media_group_handler
async def add_pics(messages: list[Message], state: FSMContext):
    # получаем нашу заявку
    request = get_latest_request_by_tg_user(messages[-1].from_user.id)

    for message in messages:
        # сохраняем изображения
        await save_pics(message.photo, message.from_user.id, request.request_id)  # type:ignore

    # меняем состояние на добавление описания add_description
    await state.set_state(States.add_description)  # type:ignore
    await bot.send_message(
        messages[0].from_user.id,
        MESSAGES["DESCRIPTION"],
        reply_markup=start_kbrd_rkm)


# Обработчик добавления одной картинки, работает аналогичку предыдущему обработчику
@dp.message_handler(
    state=States.add_pic,
    content_types=ContentTypes.PHOTO)
async def add_pic(message: Message, state: FSMContext):
    request = get_latest_request_by_tg_user(message.from_user.id)

    await save_pics(message.photo, message.from_user.id, request.request_id)  # type:ignore
    await state.set_state(States.add_description)  # type:ignore
    await bot.send_message(
        message.from_user.id,
        MESSAGES["DESCRIPTION"],
        reply_markup=start_kbrd_rkm)


# Обработчик добавления описания add_description
@dp.message_handler(state=States.add_description)
async def add_description(message: Message, state: FSMContext):
    # добавляем описание к нашей заявке
    update_current_request_description(message.from_user.id, message.text)

    # Меняем состояние на добавление корпуса choose_building
    await state.set_state(States.choose_building)  # type:ignore
    await bot.send_message(
        message.from_user.id, MESSAGES["WHERE"], reply_markup=choose_loc_type)


# Обработчик выбора корпуса choose_building
@dp.callback_query_handler(lambda c: c.data in LOCATIONS, state=States.choose_building)
async def add_building(callback: CallbackQuery, state: FSMContext):
    # Получаем тип корпуса по нажатию кнопки
    cb_data = callback.data
    # добавляем корпус к нашей заявке
    update_current_request_building(callback.from_user.id, cb_data)

    # Если корпус учебный или общежитие. то переходим к состоянию добавления 
    # номера корпуса choose_building_num
    # Иначе - переходим к состоянию выбора локации add_point
    if cb_data != "Другое":
        await state.set_state(States.choose_building_num) # type:ignore
        await bot.send_message(
            callback.from_user.id,
            MESSAGES["ADD_BUILDING"],
            reply_markup=choose_building_num_kbrd)
    else:
        await state.set_state(States.add_point) # type:ignore
        await bot.send_message(
            callback.from_user.id, MESSAGES["CHOOSE_GEOLOC"], reply_markup=choose_geoloc_kbrd)


# Обработчик выбора номера корпуса choose_building_num
@dp.callback_query_handler(state=States.choose_building_num)
async def choose_building_num(callback: CallbackQuery, state: FSMContext):
    # Получаем айди пользователя
    uid = callback.message.chat.id
    # Получаем номер корпуса
    num = callback.data
    # Добавляем номер корпуса
    update_current_request_building_num(uid, num)

    # Меняем состояние на добавление этажа add_flat
    await state.set_state(States.add_flat)  # type:ignore
    await bot.send_message(
        callback.from_user.id,
        MESSAGES["ADD_FLAT"])


# Обработчик нажатия Координаты на клавиатуре 
@dp.callback_query_handler(lambda c: c.data == "by_coords", state=States.add_point)
async def choose_coords_by_geoloc(callback: CallbackQuery, state: FSMContext):
    # Отправляем клавиатуру для добавления геолокации, меняем состояние на add_geoloc
    await state.set_state(States.add_geoloc)  # type:ignore
    await bot.send_message(
        callback.from_user.id, MESSAGES["ADD_GEOLOC"], reply_markup=add_geoloc_kbrd)


# Обработчик геолокации
@dp.message_handler(state=States.add_geoloc, content_types=ContentTypes.LOCATION)
async def get_addr_geolocation(message: Message, state: FSMContext):
    # Добавляем геолокацию
    update_current_request_geolocation(
        message.from_user.id, message.location.latitude, message.location.longitude)

    # Переходим на состояние добавления этажа
    await state.set_state(States.add_flat)  # type:ignore
    await bot.send_message(
        message.from_user.id,
        MESSAGES["ADD_FLAT"])


# Обработчик добавления адреса здания текстом
@dp.callback_query_handler(lambda c: c.data == "by_text", state=States.add_point)
async def choose_coords_by_text(callback: CallbackQuery, state: FSMContext):
    # Отправляем сообшение для запроса адреса здания
    await state.set_state(States.add_addr)  # type:ignore
    await bot.send_message(callback.from_user.id, MESSAGES["ADD_ADDR"])


# ОБработчик добавления адреса здания
@dp.message_handler(state=States.add_addr, content_types=ContentTypes.TEXT)
async def get_addr_text(message: Message, state: FSMContext):
    # Добавляем адрес
    update_current_request_location_addr(message.from_user.id, message.text)

    # Переходим на состояние добавления этажа add_flat
    await state.set_state(States.add_flat) # type:ignore
    await bot.send_message(message.from_user.id, MESSAGES["ADD_FLAT"])


# ОБработчик добавления этажа
@dp.message_handler(state=States.add_flat)
async def add_flat(message: Message, state: FSMContext):
    uid = message.from_user.id
    # Добавляем этаж к нашей заявке
    update_current_request_flat(uid, message.text)
    
    # Переходим к состоянию добавления комнаты add_room
    await state.set_state(States.add_room)  # type:ignore
    await bot.send_message(uid, MESSAGES["ADD_ROOM"])


# Обработчик добавления комнаты и отправки запроса в информационную среду НГТУ
@dp.message_handler(state=States.add_room)
async def add_room(message: Message, state: FSMContext):
    # Добавляем комнату
    update_current_request_room(message.from_user.id, message.text)
    
    await state.set_state(States.add_phone)  # type:ignore
    await bot.send_message(message.from_user.id, MESSAGES["ADD_PHONE"], reply_markup=add_phone_kbrd)


@dp.message_handler(state=States.add_phone, content_types=ContentTypes.CONTACT)
async def add_phone_num(message: Message, state: FSMContext):
    uid = message.from_user.id
    request = get_latest_request_by_tg_user(uid)
    update_current_request_phone(uid, str(message.contact.phone_number))

    try:
        # Пытаемся делать запрос в информационную среду, если происходит ошибка - сообщаем пользователю
        __response = mock_send_request_to_info_system(request)
        response_message = MESSAGES["SUCCESS"](request.request_id)
    except:
        response_message = MESSAGES["ERROR"](request.request_id)

    # Меняем состояние на добавление еще одной заявки(т.е. переходим в начало)
    await state.set_state(States.add_request)  # type:ignore
    await bot.send_message(uid, response_message, reply_markup=start_kbrd_rkm)

