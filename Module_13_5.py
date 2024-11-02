from aiogram import Bot, Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = "7712368295:AAFD63GdJ-gjE5DZQxokyVu9M6VSzSCidTE"
bot = Bot(token= api)
dp = Dispatcher(bot, storage= MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text= 'Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.row(button,button2)


@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет, я бот, помогающий твоему здоровью!',
                         reply_markup = kb) # после этого появится клавиатура)

@dp.message_handler(text = "Рассчитать")
async def set_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async  def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161
    # (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A
    colories = round(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    #colories = round(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'Ваша норма каллорий: {colories}')
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)