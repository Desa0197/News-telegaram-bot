from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text

from parse import parse


bot = Bot(token="token", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Последние 10 новостей")

    await message.answer("Шалом", reply_markup=keyboard)


@dp.message_handler(Text(equals='Последние 10 новостей'))
async def start(message: types.Message):
    list_matches = parse()
    for i in list_matches:
        match = f'{hbold(i["date_time"])}\n' \
                f'{hlink(i["title"], i["link"])}'
        await message.answer(match)


executor.start_polling(dp)
