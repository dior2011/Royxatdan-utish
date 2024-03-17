import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher,types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message,FSInputFile
from states import Form
from aiogram.fsm.context import FSMContext
import re

ADMIN = 5515940993
TOKEN = "6232855682:AAG-6BbtpsJND2WkXXGjG-UjgHNNvgU4WfY"
bot = Bot(TOKEN,parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message,state:FSMContext):
    
    await state.set_state(Form.first_name)
    await message.answer(text="Assalomu alaykum. Ro'yxatdan o'tish uchun ismingizni kiriting")
    
    
@dp.message(F.text,Form.first_name)  
async def first_name_register(message:Message,state:FSMContext):
    ism = message.text
    await state.update_data(first_name=ism)
    await state.set_state(Form.last_name)
    
    await message.answer(text="Familiyangizni kiriting")

@dp.message(F.text,Form.last_name)
async def last_name_register(message:Message,state:FSMContext):
    familiya = message.text
    await state.update_data(last_name=familiya)
    await state.set_state(Form.phone_number)
    
    await message.answer(text="Telefon nomeringizni kiriting")
    
@dp.message(F.text,Form.phone_number)
async def number_register(message:Message,state:FSMContext):
    nomer = message.text
    pattern = re.compile("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$")
    if pattern.match(nomer):
        await state.update_data(phone_number=nomer)
        await state.set_state(Form.country)
        await message.answer(text="Qaysi davlatda yashaysiz?")    
    else:
        await message.answer(text="Telefon nomeringiz noto'g'ri, qayta kiriting!")
        

 
@dp.message(F.text,Form.country)
async def last_name_register(message:Message,state:FSMContext):
    davlat = message.text
    await state.update_data(country=davlat)
    await state.set_state(Form.age)
    
    await message.answer(text="Yoshingizni kiriting!")

    
@dp.message(F.text,Form.age)
async def last_name_register(message:Message,state:FSMContext):
    try:  
        yosh = message.text
        await state.update_data(age=int(yosh))
        await state.set_state(Form.work)
        await message.answer(text="Ish joyingiz nomini kiriting!")
        
    except:
        await message.answer(text="Yosh noto'g'ri kiritilgan!")
    
@dp.message(F.text,Form.work)
async def last_name_register(message:Message,state:FSMContext):
    ish_joy = message.text
    await state.update_data(work=ish_joy)
    await state.set_state(Form.car)
    await message.answer(text="Avtomobilingiz nomini kiriting!")
    
@dp.message(F.text,Form.car)
async def last_name_register(message:Message,state:FSMContext):
    mashina = message.text
    await state.update_data(car=mashina)
    await state.set_state(Form.address)
    await message.answer(text="Davlatingizning qaysi viloyatida yashaysiz?")
    

    
    
    

@dp.message(F.text,Form.address)
async def address_register(message:Message,state:FSMContext):
    adres = message.text
    await state.update_data(address=adres)
    data = await state.get_data()
    first_name = str(data.get("first_name")).lower().capitalize()
    last_name = str(data.get("last_name")).lower().capitalize()
    phone_number = data.get("phone_number")
    country = data.get("country")
    age = data.get("age")
    car = data.get("car")
    work = data.get("work")
    address = data.get("address")
    text = f"Yangi foydalanuvchi:\nIsmi: {first_name}\nFamiliyasi: {last_name}\nYoshi: {age}\nTelefon raqami: {phone_number}\nDavlat: {country}\nViloyat: {address}\nIsh joyi: {work}\nAvtomobil: {car}"
    await bot.send_message(chat_id=ADMIN, text=text)
    
    
    await state.clear()
    
    
    
    
    await message.answer(text="Siz ro'yxatdan o'tdingiz!")


    
    
async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    
    
