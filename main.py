from aiogram import Bot, Dispatcher, types, executor
from config import TELEGRAM_TOKEN
from keboard.keyboards import get_keyboard_1, get_keyboard_2
from keboard.key_inline import get_keyboard_inline
from database.database import initialize_db, add_user, get_user

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

initialize_db()


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command='/start', description='Команда для того, что бы запустить бота'),
        types.BotCommand(command='/help', description='Команда для того, что бы узнать с чем может помочь наш бот')
  ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands= 'start')
async def start(message: types.message):
    user = get_user(message.from_user.id)
    if user is None:
        add_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
        await message.answer('Привет, я твой первый ЭХО бот', reply_markup= get_keyboard_1())
    else:
        await message.answer('Привет, я твой первый ЭХО бот', reply_markup=get_keyboard_1())

@dp.message_handler(lambda message: message.text == 'фото')
async def button_1_click(message: types.Message):
    await bot.send_photo(message.chat.id, photo= 'https://gas-kvas.com/uploads/posts/2023-02/1675446652_gas-kvas-com-p-kartinki-na-fonovii-risunok-rabochego-23.jpg', caption='фото')

@dp.message_handler(lambda message: message.text == 'клава')
async def button_2_click(message: types.Message):
    await message.answer('попроси фото собаки', reply_markup= get_keyboard_2())

@dp.message_handler(lambda message: message.text == 'фото собаки')
async def button_3_click(message: types.Message):
    await bot.send_photo(message.chat.id, photo='https://img2.joyreactor.cc/pics/post/full/%D1%81%D0%BE%D0%B1%D0%B0%D0%BA%D0%B0-%D0%BA%D0%BE%D1%80%D0%B3%D0%B8-3258704.jpeg', caption='вот собака', reply_markup= get_keyboard_inline())

@dp.message_handler(lambda message: message.text == 'назад клава')
async def button_2_click(message: types.Message):
    await message.answer('попроси фото', reply_markup= get_keyboard_1())




@dp.message_handler(commands= 'help')
async def help(message: types.message):
    await message.reply('я могу помочь тебе с ...')

@dp.message_handler()
async def echo(message: types.message):
    await message.answer(message.text)

async def on_startup(dispatcher):
    await set_commands(dispatcher.bot)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True, on_startup= on_startup)