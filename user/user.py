from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from filters.users import UserPrivateFilter
from config import chenel_id, Bot_token
from buttons import *
from state import *
from config import *
from CRUD import insertkino, readkino, deleteKino
from aiogram.fsm.context import FSMContext
bot = Bot(token=Bot_token)

user_router = Router()




@user_router.message(CommandStart())
async def checksub(message:Message) -> None:
    user_id = message.from_user.id
    if user_id in admin:
        await message.answer('Sizga adminlik huquqi berilgan', reply_markup=buttom_admin)
    else:
        user_status = await bot.get_chat_member(chenel_id[0], message.from_user.id)
        if user_status.status == 'left':
            await message.answer("👇 Pastdagi kanallarga obuna bo'ling", reply_markup=tugma.as_markup())
        else:
            user_status2 = await bot.get_chat_member(chenel_id[1], message.from_user.id)
            if user_status2.status == 'left':
                await message.answer("👇 2-kanalga obuna bo'ling", reply_markup=tugma.as_markup())
            else:
                await message.answer("Botdan foydalanishingiz mumkin kino qo'dini oldiga (/) bunday belgi qoyib yuboring yuboring")

@user_router.callback_query(F.data == "tekshir")
async def tekBot(cal:CallbackQuery):
    user_status = await bot.get_chat_member(chenel_id[0], cal.from_user.id)
    if user_status.status == "left":
        await cal.message.answer(f"Barcha kanallarga obuna bo'lmadingiz", reply_markup=tugma.as_markup())
    else:
        user_status2 = await bot.get_chat_member(chenel_id[1], cal.from_user.id)
        if user_status2.status == 'left':
            await cal.message.answer("👇 2-kanalga obuna bo'ling", reply_markup=tugma.as_markup())
        else:

            await cal.message.answer("Botdan foydalanishingiz mumkin kino qo'dini oldiga (/) bunday belgi qoyib yuboring yuboring")
        


@user_router.message(Command('exit'))
async def srat(message:Message, state:FSMContext):
    await state.clear()
    await message.answer('Bosh sahifaga qaytdingiz', reply_markup=buttom_admin)




@user_router.message(F.text.startswith('/') , F.text[1:].isdigit())
async def BotStart(message: Message):
    a = ''
    user_status = await bot.get_chat_member(chenel_id[0], message.from_user.id)
    if user_status.status == "left":
        await message.answer(f"Siz barcha kanallarga obuna bo'lmagansiz", reply_markup=tugma.as_markup())
    else:
        user_status1 = await bot.get_chat_member(chenel_id[1], message.from_user.id)
        if user_status1.status == "left":
            await message.answer(f"Siz barcha kanallarga obuna bo'lmagansiz", reply_markup=tugma.as_markup())
        else:
            cnt = list(message.text)
            cnt.pop(0)
            for i in cnt:
                a += i
            for i in readkino():
                if str(i[0]) == a:
                    await bot.send_video(chat_id=message.from_user.id, video=i[1], caption=f"{i[2]}", protect_content = True)
                    return
            await message.reply('Bunday kino yoq')
            cnt.clear()



@user_router.message(F.text == 'Kino o\'chirish')
async def delet(message:Message, state:FSMContext):
    await message.answer('Kino qo\'dini oddiy ko\'rinishda yuboring')
    await state.set_state(deleteForm.delete)


cnt1 = []
@user_router.message(deleteForm.delete)
async def dele(message:Message, state:FSMContext):
    for i in readkino():
        cnt1.append(i)
    for i in cnt1:
        if str(i[0]) == str(message.text):
            deleteKino(kod=message.text)
            await message.answer("O'chirildi", reply_markup=buttom_admin)
            await state.clear()
            return
    await message.answer('Bunday kino yoq')
    






@user_router.message(F.text == "Kino qoshish")
async def addkino(message:Message, state:FSMContext):
    await message.answer("Kino faylini yuboring")
    await state.set_state(addmovieForm.kino)

@user_router.message(addmovieForm.kino)
async def addkimo2(message:Message, state:FSMContext):
    if message.video:
        video = message.video.file_id
        await state.update_data({'kino': video})
        await message.answer("Izoh qo'shish")
        await state.set_state(addmovieForm.izox)
    else:
        await message.answer("Siz yuborgan file video emas")

@user_router.message(addmovieForm.izox)
async def izox(message:Message, state:FSMContext):
    await state.update_data({'izoh' : message.text})
    await message.answer("Kod yuboring")
    await state.set_state(addmovieForm.kod)
    
cnt = []
@user_router.message(addmovieForm.kod)
async def addkod(message:Message, state:FSMContext):
    data = await state.get_data()
    kino_id = message.text
    print(kino_id)
    for i in readkino():
        cnt.append(i[0])
    for i in cnt:
        if int(i) == int(kino_id):
            await message.answer('Bunday kod band')
            await state.set_state(addmovieForm.kod)
            return
    await state.update_data({'kod': kino_id})
    await bot.send_video(chat_id=message.from_user.id, video=data.get('kino'), caption=data.get('izoh'))
    await message.answer(f"Kodi {kino_id}\nTasdiqlaysizmi", reply_markup=Buttom_tekshir)
    await state.set_state(addmovieForm.final)
    cnt.clear()

@user_router.callback_query(addmovieForm.final)
async def tekshir(call:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    xabat = call.data
    if xabat == 'ha':
        kino = data.get('kino')
        izoh = data.get('izoh')
        kod = data.get('kod')
        insertkino(id1=kod, kino=kino, izoh=izoh)
        await call.message.answer("Kino muaffaqiyatli yuklandi", reply_markup=buttom_admin)
    else:
        await call.message.answer('Muaffaqiyatli bekor qilindi', reply_markup=buttom_admin)





@user_router.message(F.text)
async def kek(message:Message):
    await message.reply('Bunday buyruq mavjud emas')

@user_router.message(F.video)
async def kek(message:Message):
    await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAELaTZnfONefsFU_w3EgFgRoS5gdsNxngACpAEAAhZCawozOoCXqc8vXDYE')
    await message.reply('Botga media file yuborish mumkin emas')

@user_router.message(F.photo)
async def kek(message:Message):
    await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAELaTZnfONefsFU_w3EgFgRoS5gdsNxngACpAEAAhZCawozOoCXqc8vXDYE')
    await message.reply('Botga media file yuborish mumkin emas')

@user_router.message(F.sticker)
async def stikker(message:Message):
    await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAELaTZnfONefsFU_w3EgFgRoS5gdsNxngACpAEAAhZCawozOoCXqc8vXDYE')
    await message.reply('Botga stikker tashlash mimkin emas')

@user_router.message(F.voice)
async def stikker(message:Message):
    await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAELaTZnfONefsFU_w3EgFgRoS5gdsNxngACpAEAAhZCawozOoCXqc8vXDYE')
    await message.reply('Botga musiqa, tarona, va boshqa audio fayllarni yuborish mimkin emas')

@user_router.message(F.audio)
async def stikker(message:Message):
    await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAELaTZnfONefsFU_w3EgFgRoS5gdsNxngACpAEAAhZCawozOoCXqc8vXDYE')
    await message.reply('Botga musiqa, tarona, va boshqa audio fayllarni yuborish mimkin emas')

@user_router.message(F.video_note)
async def stikker(message:Message):
    await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAELaTZnfONefsFU_w3EgFgRoS5gdsNxngACpAEAAhZCawozOoCXqc8vXDYE')
    await message.reply('Botga media file yuborish mumkin emas')
    
@user_router.message(F.animation)
async def stikker(message:Message):
    await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAELaTZnfONefsFU_w3EgFgRoS5gdsNxngACpAEAAhZCawozOoCXqc8vXDYE')
    await message.reply('Botga media file yuborish mumkin emas')


