from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
import re 
import config

from middlewares import middleware
from states import states
from kbs import keyboards

adminrt = Router()
adminrt.message.middleware(middleware.AdminCheckerMiddleware())
adminrt.callback_query.middleware(middleware.AdminCheckerMiddleware())

@adminrt.message(states.Admin.active, Command('admin'))
async def adminpanelhide(message: types.Message, state:FSMContext):
    await state.clear()
    await message.answer("Хорошая работа)")

@adminrt.message(Command('admin'), default_state)
async def adminpanel(message: types.Message, state:FSMContext):
    await state.set_state(states.Admin.active)
    await message.answer(f"Привет, админ {message.from_user.first_name}!\nЧтобы выйти из режима админа - пропишите /admin ещё раз\nЧто делаем?", reply_markup=keyboards.adminMarkup)

async def adminpanelcb(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(states.Admin.active)
    await callback.message.edit_text(f"Привет, админ {callback.from_user.first_name}!\nЧтобы выйти из режима админа - пропишите /admin ещё раз\nЧто делаем?", reply_markup=keyboards.adminMarkup)


#add channel
@adminrt.callback_query(states.Admin.active, F.data == "addchannel")
async def addchannel(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(states.Admin.addchan)
    await callback.answer()
    await callback.message.edit_text('Скиньте ссылку на канал вида "https://t.me/имя_канала":', reply_markup=keyboards.adminbackMarkup)
    
@adminrt.message(states.Admin.addchan)
async def setchannel(message: types.Message, state:FSMContext):
    if re.match(r"^https://t\.me/.+", message.text):
        link = message.text
        name = f"@{link[len("https://t.me/"):].rstrip('/')}"
        config.channels[name] = link
        result = config.savechannels()
        if result:
            await message.answer(f"Канал {name} был добавлен.")
            await state.set_state(states.Admin.active)
        else:
            await message.answer(f"Произошла ошибка записи, попробуйте в другой раз.")
            await state.set_state(states.Admin.active)
    else: 
        await message.answer("Ссылка некорректна.")
        
#del channel
@adminrt.callback_query(states.Admin.active, F.data == "delchannel")
async def delchannel(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(states.Admin.delchan)
    await callback.answer()
    list = ""
    for i, (key, val) in enumerate(config.channels.items(), start=0):
        list += f"\n{i}.){key}"
    await callback.message.edit_text(f"Напишите номер каналa, который нужно убрать:\n {list}", reply_markup=keyboards.adminbackMarkup)
    
@adminrt.message(states.Admin.delchan)
async def popchannel(message: types.Message, state:FSMContext):
    i = int(message.text)
    print(i)
    print(len(config.channels))
    if i >= 0 and i < len(config.channels):
        keys = list(config.channels.keys())
        channelkey = keys[i]
        config.channels.pop(channelkey)
        result = config.savechannels()
        if result:
            await message.answer(f"Канал {channelkey} был успешно убран.")
            await state.set_state(states.Admin.active)
        else:
            await message.answer(f"Произошла ошибка записи, попробуйте в другой раз.")
            await state.set_state(states.Admin.active)
    else:
        await message.answer("Введите число из списка.")

        
@adminrt.callback_query(F.data == "adminback")
async def adminback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(states.Admin.active)
    await adminpanelcb(callback, state)
    