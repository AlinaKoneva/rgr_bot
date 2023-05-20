from aiogram.types import reply_keyboard, inline_keyboard


# fmt:off

# Альясы для удобочитаемости клавиатур
IKM = inline_keyboard.InlineKeyboardMarkup
IKButton = inline_keyboard.InlineKeyboardButton

RKM = reply_keyboard.ReplyKeyboardMarkup
RKButton = reply_keyboard.KeyboardButton

LOCATIONS = ["Учебный корпус", "Общежитие", "Другое"]


# Клавиатуры на добавление заявки
start_kbrd_rkm = RKM(
    keyboard=[
        [RKButton(text="Добавить")]],
    resize_keyboard=True
)


start_kbrd = IKM(
    inline_keyboard=[[
        IKButton(text="Добавить", callback_data="add_request")
    ]]
)


# Клавиатура на добавлние адреса другого корпуса
choose_geoloc_kbrd = IKM(
    inline_keyboard=[
        [IKButton(text="Координаты", callback_data="by_coords", request_location=True)],
        [IKButton(text="Адрес", callback_data="by_text")],
    ]
)

# Клавиатура запроса гелолокации
add_geoloc_kbrd = RKM(
    keyboard=[[
        RKButton("Добавить геолокацию", request_location=True, callback_data="add_geoloc")
    ]],
    resize_keyboard=True,
)

# Клавиатура выбора типа корпуса
choose_loc_type = IKM(
    inline_keyboard=[
        [IKButton(text=loc, callback_data=loc)] for loc in LOCATIONS
    ]
)

# Клавиатура выбора номера корпуса
choose_building_num_kbrd = IKM(
    inline_keyboard=[[IKButton(text=str(i), callback_data=str(i))] for i in range(1, 9)]
)


add_phone_kbrd = RKM(
    keyboard=[[
        RKButton("Добавить номер телефона", request_contact=True, callback_data="add_phone")
    ]],
    resize_keyboard=True,
)
