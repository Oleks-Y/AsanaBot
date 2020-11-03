from aiogram import types
from misc import dp

@dp.message_handler(commands=['start'])
async def  command_start(message : types.Message) :
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("/createtask")
    await message.answer("Hello mazafakka", reply_markup=keyboard);
