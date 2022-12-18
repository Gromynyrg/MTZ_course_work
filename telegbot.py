import MTZ_V
import data_creation
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


class UserStates(StatesGroup):
    init = State()  # Состояние когда пользователь готовится вводить данные
    sizes = State()  # Состояние когда пользователь ввел размеры матрицы
    rectangles = State()  # Состояние когда пользователь ввел кол-во прямоугольников
    common = State()    # Обычное состояние


API_TOKEN = '5807405189:AAF2R27fx9qqsjnWVrNOHio1BpJvcH0WCMY'
bot = Bot(token=API_TOKEN)  # Подключаем бота к его токену
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

i = 0
k = 0
mas = []
x_size = 0
y_size = 0

kb = [
    [
        types.KeyboardButton(text="Хочу отправить данные для визуализации"),
        types.KeyboardButton(text="Помощь"),
        types.KeyboardButton(text="Я хочу сам ввести данные для визуализации")
    ],
]  # Задаём кнопки для бота
keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)

@dp.message_handler(commands=['start'], state='*')  # Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message):
    user_name = message.from_user.username
    await message.reply(
        f"Привет, {user_name}! 👋 \nЯ Бот для визуализации задач МТЗ!\nНажмите на кнопки ниже для получения желаемых результатов.",
        reply_markup=keyboard)  # Так как код работает асинхронно, то обязательно пишем await.
    await UserStates.common.set()


@dp.message_handler(text="Хочу отправить данные для визуализации", state=UserStates.common)
async def send_reply(message: types.Message):
    await message.reply("Вам нужно загрузить файл формата '.txt','.csv' или '.xlsx'")

    @dp.message_handler(content_types=['document'], state=UserStates.common)  # Бот ожидает от пользователя файл
    async def send_file(message: types.Message):
        if (message.document.mime_type == 'text/csv' or message.document.mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or message.document.mime_type == 'text/plain'):
            await message.answer_chat_action(action=types.ChatActions.TYPING)
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


@dp.message_handler(text="Я хочу сам ввести данные для визуализации", state=UserStates.common)
async def send_reply(message: types.Message):
    await message.answer("Хорошо, для начала укажите три числа через пробел - размеры и значение среды ")
    await UserStates.init.set()


@dp.message_handler(state=UserStates.init)
async def get_size(message: types.Message):
    sizes = []
    def isint():
        try:
            sizes = [int(x) for x in message.text.split()]
            return True
        except ValueError:
            return False
    b = isint()
    if b:
        sizes = [int(x) for x in message.text.split()]
    if ((len(sizes) == 3)and b):
        await message.answer("Хорошо, Теперь укажите число прямоугольников - одно целое число")
        data_creation.init_file(id_user=message.from_user.id, column=sizes[0], row=sizes[1], field_density=sizes[2])
        global mas,x_size,y_size
        mas = []
        x_size = sizes[0]
        y_size = sizes[1]
        for u in range(sizes[0]):
            lst = []
            for j in range(sizes[1]):
                lst.append(100)

            mas.append(lst)

        await UserStates.sizes.set()

    else:
        await message.answer("Что-то пошло не так, введите данные в правильном виде")


@dp.message_handler(state=UserStates.sizes)
async def get_count_rec(message: types.Message):
    def isint2():
        try:
            rect_count = int(message.text)
            return True
        except ValueError:
            return False
    b = isint2()
    if b:
        rect_count = int(message.text)
        await message.answer(
            "Хорошо, Теперь укажите начальные координаты для прямоугольников и их размеры и плотность - 5 чисел через пробел")
        await UserStates.rectangles.set()
        global i
        i = 0
        i = rect_count
    else:
        await message.answer("Что-то пошло не так, введите данные в правильном виде")


@dp.message_handler(state=UserStates.rectangles)
async def get_rect(message: types.Message):
    global i, k, mas

    if (i > k+1):
        rect = [int(x) for x in message.text.split()]
        if (len(rect) == 5):
            k += 1
            for _ in range(rect[0] - 1, rect[2] + rect[0] - 1):
                for __ in range(rect[1] - 1, rect[3] + rect[1] - 1):
                    mas[_][__] = rect[4]
            await message.answer(f"{k + 1} Прямоугольник - ")
        else:
            await message.answer("Что-то пошло не так, попробуйте ввести значения прямоугольника еще раз ")
    else:
        rect = [int(x) for x in message.text.split()]
        if (len(rect) == 5):
            k += 1
            for _ in range(rect[0] - 1, rect[2] + rect[0] - 1):
                for __ in range(rect[1] - 1, rect[3] + rect[1] - 1):
                    mas[_][__] = rect[4]
        await message.answer("Всё готово, ожидайте результатов")
        await message.answer_chat_action(action=types.ChatActions.TYPING)
        data_creation.fill_in(id_user=message.from_user.id, mas=mas, x_size=x_size, y_size=y_size)
        k = 0
        file_name = f'{message.from_user.id}.txt'
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
        await UserStates.common.set()



@dp.message_handler(text="Помощь",state=UserStates.common)
async def send_help(message: types.Message):
    await message.reply("Для того чтобы воспользоваться ботом нажмите на кнопки")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
