from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

# from bot.state import Register
import bot.keyboards as kb
# import bot.database.request as rq
from bot.database.request import get_item,set_user
from bot.state import Register

router = Router()

@router.message(CommandStart())
@router.callback_query(F.data == 'to_main')
async def cmd_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await set_user(message.from_user.id)
        await message.answer('Welcome to the Eva_Margo store !',reply_markup=kb.main)
    else:
        await message.message.edit_text('Welcome to the Eva_Margo store !',reply_markup=kb.main)

@router.message(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Select product category', reply_markup= await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback:CallbackQuery):
    await callback.answer('You have selected a category')
    await callback.message.answer('Select product by category ',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_data = await get_item(callback.data.split('_')[1])
    await callback.answer('You have selected a product')
    await callback.message.edit_text(f'Product name: {item_data.name}\nDescription: {item_data.description}\nPrice: {item_data.price}$',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Enter your name')

@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Enter your age')

@router.message(Register.age)
async def register_age(message: Message, state:FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.number)
    await message.answer('Enter your number', reply_markup= kb.get_number)

@router.message(Register.number,F.contact)
async def register_number(message: Message, state:FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Your name: {data['name']}\nYour age: {data['age']}\nYour number: {data['number']}')
    await state.clear()



