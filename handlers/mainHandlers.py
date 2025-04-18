from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.fsm.state import default_state
import os

from middlewares import middleware
from data import data
from . import someMethods
from downloaders import downloader
from states import states

mainrt = Router()
mainrt.message.middleware(middleware.SpamMiddleware())

@mainrt.message(Command('start'), default_state)
async def start(message: types.Message, state:FSMContext):
    await someMethods.memberanddb(message, state)
   
@mainrt.callback_query(F.data == "check")
async def check(callback: types.CallbackQuery, state: FSMContext):
    member = await someMethods.checkMembership(callback.from_user.id)
    if member:
        if await data.checkUser(userid=callback.from_user.id):
            await someMethods.mainmenucb(callback, state)
        else:
            result = await data.addUser(userid=callback.from_user.id)
            if result:
                await someMethods.mainmenu(callback, state, vids=await data.getVids(userid=callback.from_user.id))
            else:
                await callback.message.answer("⚠Ошибка⚠")
    else:
        await callback.answer("⚠Пожалуйста, подпишитесь на все каналы⚠")

     
@mainrt.message(default_state)
async def linkmessage(message: types.Message, state:FSMContext):
    member = await someMethods.checkMembership(message.from_user.id)
    if member and await data.checkUser(userid=message.from_user.id):
        if await data.checkVids(userid=message.from_user.id):
            status = await someMethods.checkLink(message.text)
            print(status)
            if status and status != "und":
                await state.set_state(states.InProcessBlocker.blockmessages)
                loading = await message.answer("⌛В процессе...")
                result = await downloader.downloadVideo(message.text)
                if result:
                    try:
                        print(os.path.getsize(result))
                        videofile = FSInputFile(result)
                        await message.answer_video(video=videofile)
                        await data.decrVideos(userid=message.from_user.id)
                        vids = await data.getVids(userid=message.from_user.id)
                        if vids:
                            await message.answer(f"✅Ваше видео готово!✅\n⬇Скачиваний осталось: {vids}⬇\nЧто-нибудь ещё?")
                        else:
                            await message.answer(f"✅Ваше видео готово!✅\n⚠Скачиваний не осталось! Приходите завтра.\n /start - информация о доступных скачиваниях.")
                    finally:
                        os.remove(result)
                        await loading.delete()
                        await state.clear()
                else:
                    await loading.delete()
                    await message.answer("❌Ваше видео слишком объёмное.❌")
            elif status == "und":
                await message.answer("❌Ссылка на данный ресурс не поддерживается.❌")
        else:
            await message.answer("❌У вас не осталось скачиваний, приходите завтра.❌")
    else:
        await someMethods.memberanddb(message, state)