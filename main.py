import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")  # <-- исправлено
CHANNEL_ID = '@robloxskuf'
DATA_FILE = "rep_data.json"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Загружаем данные из файла
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Сохраняем данные в файл
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

rep_data = load_data()

# Кнопка с репутацией
def get_rep_button(count: int):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text=f"⭐ +rep | {count} 👍",
            callback_data="add_rep"
        )
    )

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def forward_text_to_channel(message: types.Message):
    sent = await bot.send_message(
        chat_id=CHANNEL_ID,
        text=message.text,
        reply_markup=get_rep_button(0)
    )
    
    rep_data[str(sent.message_id)] = {
        "count": 0,
        "users": []
    }
    save_data(rep_data)

    await message.answer("✅ Сообщение отправлено в канал с кнопкой!")

@dp.callback_query_handler(lambda c: c.data == 'add_rep')
async def process_callback(callback_query: types.CallbackQuery):
    msg_id = str(callback_query.message.message_id)
    user_id = str(callback_query.from_user.id)

    if msg_id not in rep_data:
        rep_data[msg_id] = {"count": 0, "users": []}

    if user_id in rep_data[msg_id]["users"]:
        await callback_query.answer("Вы уже поставили репутацию 👍", show_alert=True)
    else:
        rep_data[msg_id]["users"].append(user_id)
        rep_data[msg_id]["count"] += 1
        save_data(rep_data)

        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=int(msg_id),
            reply_markup=get_rep_button(rep_data[msg_id]["count"])
        )
        await callback_query.answer("Спасибо за +rep! 👍")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
