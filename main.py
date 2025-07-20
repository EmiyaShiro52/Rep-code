import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("API_TOKEN")
CHANNEL_ID = '@robloxskuf'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

rep_count = 0

def get_rep_button():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text=f"⭐ +rep | {rep_count} 👍",
            callback_data="add_rep"
        )
    )

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def forward_text_to_channel(message: types.Message):
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=message.text,
        reply_markup=get_rep_button()
    )
    await message.answer("✅ Сообщение отправлено в канал с кнопкой!")

@dp.callback_query_handler(lambda c: c.data == 'add_rep')
async def process_callback(callback_query: types.CallbackQuery):
    global rep_count
    rep_count += 1

    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=get_rep_button()
    )

    await bot.answer_callback_query(callback_query.id, text="Спасибо за +rep! 👍")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
