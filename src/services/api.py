from src.db.models import Request
from src.bot.base import bot


# Заглушка запроса в информационную систему
def mock_send_request_to_info_system(request: Request):
    pass


# Заглушка отправки сообшения пользователю о состоянии обработки его заявки
async def send_reply_from_info_system(tg_user_id: int, reply_text: str):
    await bot.send_message(tg_user_id, reply_text)

