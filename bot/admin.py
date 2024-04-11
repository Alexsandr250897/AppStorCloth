from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


import bot.keyboards as kb
from bot.database.request import get_users, set_item

admin = Router()

class Newsletter(StatesGroup):
    message = State()

class AddItem(StatesGroup):
    name = State()
    category = State()
    description = State()
    photo = State()
    price = State()


class AdminProject(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [1923494772]


@admin.message(AdminProject(), Command('admin'))
async def admin_panel(message: Message):
    await message.answer('Possible commands:/newsletter\n/add_product')

@admin.message(AdminProject(), Command('newsletter'))
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(Newsletter.message)
    await message.answer('Send the message you want to send out')


@admin.message(AdminProject(), Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    await message.answer('Wait, mailing is in progress...')
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.tg_id)
        except:
            pass
    await message.answer('Mailing completed successfully')
    await state.clear()


@admin.message(AdminProject(),Command('add_product'))
async def add_item(message:Message, state:FSMContext):
    await state.set_state(AddItem.name)
    await message.answer('Enter the product name')


@admin.message(AdminProject(), AddItem.name)
async def add_item_name(message:Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddItem.category)
    await message.answer('Select product category', reply_markup= await kb.categories())

@admin.callback_query(AdminProject(),AddItem.category)
async def add_item_category(callback: CallbackQuery, state:FSMContext):
    await state.update_data(category= callback.data.split('_')[1])
    await state.set_state(AddItem.description)
    await callback.answer('')
    await callback.message.answer('Enter product description')

@admin.message(AdminProject(), AddItem.description)
async def add_item_description(message: Message, state: FSMContext):
    await state.update_data(description= message.text)
    await state.set_state(AddItem.photo)
    await message.answer('Send a photo product')

@admin.message(AdminProject(), AddItem.photo, F.photo)
async def add_item_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(AddItem.price)
    await message.answer('Enter the price of the product')


@admin.message(AdminProject(), AddItem.price)
async def add_item_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await set_item(data)
    await message.answer('Product added successfully')
    await state.clear()