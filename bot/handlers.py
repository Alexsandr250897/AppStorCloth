from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext


# from bot.state import Register
import bot.keyboards as kb
from bot.database.request import get_item, set_user, set_basket,get_basket, delete_basket
from bot.state import Register

router = Router()

@router.message(CommandStart())
@router.callback_query(F.data == 'to_main')
async def cmd_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await set_user(message.from_user.id)
        await message.answer('Welcome to the Eva_Margo store !',reply_markup=kb.main)
    else:
        await message.answer('You are back to home')
        await message.message.answer('Welcome to the Eva_Margo store !',reply_markup=kb.main)

@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Select product category',
                                     reply_markup= await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback:CallbackQuery):
    await callback.answer('You have selected a category')
    await callback.message.edit_text('Select product by category ',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item = await get_item(callback.data.split('_')[1])
    await callback.answer('')
    await callback.message.answer_photo(photo= item.photo, caption=f' {item.name}\n\n {item.description}\n\n {item.price} $',
                                  reply_markup= await kb.basket(item.id))

@router.callback_query(F.data.startswith('order_'))
async def basket(callback: CallbackQuery):
    await set_basket(callback.from_user.id, callback.data.split('_')[1])
    await callback.answer('Item added to basket')

@router.callback_query(F.data == 'mybasket')
async def mybasket(callback: CallbackQuery):
    await callback.answer('')
    basket = await get_basket(callback.from_user.id)
    counter = 0
    for item_info in basket:
        item = await get_item(item_info.item)
        await callback.message.answer_photo(photo=item.photo, caption=f' {item.name}\n\n {item.description}\n\n{item.price}',
                                        reply_markup=await kb.delete_from_basket(item.id))
        counter += 1
    await callback.message.answer('Your basket is  empty') if counter == 0 else await callback.answer('')

@router.callback_query(F.data.startswith('delete_'))
async def delete_from_bascek(callback: CallbackQuery):
    await callback.answer('')
    await delete_basket(callback.from_user.id, callback.data.split('_')[1])
    await callback.message.delete()
    await callback.message.answer('You have removed an item from your cart')






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



