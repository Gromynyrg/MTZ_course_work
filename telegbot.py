import MTZ_V
from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '5807405189:AAF2R27fx9qqsjnWVrNOHio1BpJvcH0WCMY'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


kb = [
    [
        types.KeyboardButton(text="Хочу отправить данные для визуализации"),
        types.KeyboardButton(text="Помощь"),
        types.KeyboardButton(text="Я хочу сам ввести данные для визуализации")
    ],
]
keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)

@dp.message_handler(commands=['start']) # Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message):
    user_name = message.from_user.username
    await message.reply(f"Привет, {user_name}! 👋 \nЯ Бот для визуализации задач МТЗ!\nНажмите на кнопки ниже для получения желаемых результатов.", reply_markup=keyboard) # Так как код работает асинхронно, то обязательно пишем await.

@dp.message_handler(text="Хочу отправить данные для визуализации")
async def send_reply(message: types.Message):
    await message.reply("Вам нужно загрузить файл формата '.txt','.csv' или '.xlsx'")
    @dp.message_handler(content_types=['document'])
    async def send_file(message: types.Message):
        if (message.document.mime_type == 'text/csv' or  message.document.mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or message.document.mime_type =='text/plain' ):
            file_name = message.document.file_name
            await message.document.download(destination_file=file_name)
            photo1 = MTZ_V.mtz_sol(file_name)
            photoq1 = open(photo1, 'rb')
            photoq2 = open('visual_ro.png', 'rb')
            photoq3 = open('visual_ro2.png', 'rb')
            photoq4 = open('visual_phi.png', 'rb')
            photoq5 = open('visual_phi2.png', 'rb')
            await message.reply("Визуализация данных")
            await bot.send_photo(chat_id=message.chat.id, photo=photoq1)
            await message.reply("Визуализация кривых ρ кажущегося")
            await bot.send_photo(chat_id=message.chat.id, photo=photoq2)
            await message.reply("Визуализация ρ кажущегося")
            await bot.send_photo(chat_id=message.chat.id, photo=photoq3)
            await message.reply("Визуализация кривых φ ")
            await bot.send_photo(chat_id=message.chat.id, photo=photoq4)
            await message.reply("Визуализация φ ")
            await bot.send_photo(chat_id=message.chat.id, photo=photoq5)
        else:
            await message.reply("Неверный формат файла, пожалуйста загрузите файл формата: '.txt', '.csv' или '.xlsx'")


@dp.message_handler(text="Я хочу сам ввести данные для визуализации")
async def send_reply(message: types.Message):
    await message.reply("Хорошо, для начала укажите два числа через пробел - размеры ")



@dp.message_handler(text="Помощь")
async def send_help(message: types.Message):
    await message.reply("Для того чтобы воспользоваться ботом нажмите на кнопку")



if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)

