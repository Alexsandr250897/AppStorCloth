from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.database.request import get_categories, get_category_item
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Catalog", callback_data='catalog')],
    [InlineKeyboardButton(text="Basket", callback_data='mybasket')],
    [InlineKeyboardButton(text="Contact", callback_data='contacts'),
    InlineKeyboardButton(text="About Us", callback_data='about')]
])

to_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Home',callback_data='to_main')]
])

async def delete_from_basket(order_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Remove from basket',callback_data=f'delete_{order_id}'))
    return keyboard.adjust(2).as_markup()
async def basket(order_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Checkot', callback_data=f'order_{order_id}'))
    keyboard.add(InlineKeyboardButton(text='Back', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

# registration = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Registration')]],resize_keyboard=True)
#
#
# catalog = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Hoodi',callback_data='hoodi')],
#     [InlineKeyboardButton(text='Trousers',callback_data='trousers')],
#     [InlineKeyboardButton(text='Sports suit', callback_data='sport_suit')]])
#
# get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Send phone numder', request_contact=True)]],
#                                  resize_keyboard=True)

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name,
                                          callback_data=f'category_{category.id}'))
    keyboard.add(InlineKeyboardButton(text='Back', callback_data = 'to_main'))
    return keyboard.adjust(2).as_markup()


async def items(category_id:int):
    items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in items:
        keyboard.add(InlineKeyboardButton(text=item.name,
                                          callback_data= f'item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='Back', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()