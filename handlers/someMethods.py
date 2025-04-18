from aiogram import types, F
from aiogram.fsm.context import FSMContext
from config import channels
from aiogram.types import FSInputFile
from bot import bot
import re 

from data import data
from kbs import keyboards

YTPAT = r"^https://www\.youtube\.com/watch\?v=.+"
YTPAT2 = r"https://youtu\.be/.+"
YSPAT = r"^https://www\.youtube\.com/shorts/.+"
YSPAT2 = r"https://youtube\.com/shorts/.+"
TTPAT = r"^https://vm\.tiktok\.com/.+"

async def memberanddb(message: types.Message, state: FSMContext):
    member = await checkMembership(message.from_user.id)
    if member:
        await checkUserandAdd(message, state)
    else:
        await message.answer(f"⚠Для пользования ботом вы должны подписаться на все предложенные каналы:", reply_markup=await keyboards.channelkbbuilder())

async def checkMembership(userid):
    for key, val in channels.items():
        member = await bot.get_chat_member(key, userid)
        if member.status in ("creator", "administrator", "member"):
            print("one mship checked")
        else:
            print("one mship failed")
            return False 
    return True   

async def checkLink(link:str):
    if link:
        if "https://" in link:
            if re.match(YTPAT, link):
                return "yt"
            elif re.match(YTPAT2, link):
                return "yt"
            if re.match(YSPAT, link):
                return "ys"
            elif re.match(YSPAT2, link):
                return "ys"
            if re.match(TTPAT, link):
                return "tt"
            return "und"
    else:
        return False

async def checkUserandAdd(message: types.Message, state: FSMContext):
    if await data.checkUser(userid=message.from_user.id):
        await data.checkVids(userid=message.from_user.id)
        vids = await data.getVids(userid=message.from_user.id)
        await mainmenu(message, state, vids=vids)
    else:
        result = await data.addUser(userid=message.from_user.id)
        if result:
            await mainmenu(message, state, vids=await data.getVids(userid=message.from_user.id))
        else:
            await message.answer("⚠Ошибка базы, приходите позже⚠")

async def mainmenu(message: types.Message, state: FSMContext, vids):
    await state.clear()
    if vids:
        await message.answer(f"👋Приветствую {message.from_user.first_name}!👋\n🤖Я помогу вам скачать любое видео из Youtube и tiktok.\n⬇Скачиваний осталось: {vids}⬇\nПросто пришлите мне URL-адресс интересующего вас видео:")
    else:
        await message.answer(f"👋Приветствую {message.from_user.first_name}!👋\n🤖Я помогу вам скачать любое видео из Youtube и tiktok.\n⚠Однако у вас не осталось скачиваний на сегодня, приходите завтра.")
    
async def mainmenucb(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    vids = await data.getVids(callback.from_user.id)
    if vids:
        await callback.message.edit_text(f"👋Приветствую {callback.from_user.first_name}!👋\n🤖Я помогу вам скачать любое видео из Youtube и tiktok.\n⬇Скачиваний осталось: {vids}⬇\nПросто пришлите мне URL-адресс интересующего вас видео:")
    else:
        await callback.message.edit_text(f"👋Приветствую {callback.from_user.first_name}!👋\n🤖Я помогу вам скачать любое видео из Youtube и tiktok.\n⚠Однако у вас не осталось скачиваний на сегодня, приходите завтра.")
