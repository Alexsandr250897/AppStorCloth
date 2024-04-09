from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


import bot.keyboards as kb
from bot.database.request import get_users

admin = Router()

class Newsletter(StatesGroup):
    message = State()
    # confirm = State()

class AdminProject(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [1923494772]


@admin.message(AdminProject(), Command('admin_panel'))
async def admin_panel(message: Message):
    await message.answer('Possible commands:/newsletter')

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


