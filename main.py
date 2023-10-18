import logging
from os import getenv, path

import requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand
from dotenv import load_dotenv

from data.api import UniversalAPI
from data.crud import user_create, user_statistic, user, media_statistic, find_user
from db.connection import create_db
from keyboards.admin_keyboards import admin_btn, exit_btn
from states.state import ReklamaState, FindUser

api = UniversalAPI()
load_dotenv()
logging.basicConfig(level=logging.INFO)
BASE = path.dirname(path.abspath(__file__))

TOKEN = getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_handler(msg: types.Message):
    user_create(msg)
    await bot.set_my_commands([BotCommand(command='start', description="Ishga Tushirish ♻"),
                               BotCommand(command='help', description="Yordam olish 🛠"),
                               BotCommand(command='info', description="Sizning ma'lumotlaringiz 🗂")])
    await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
    await bot.send_message(chat_id=msg.chat.id,
                           text=f"𝐀𝐬𝐬𝐚𝐥𝐨𝐦𝐮 𝐚𝐥𝐚𝐲𝐤𝐮𝐦 {msg.from_user.full_name} 🤖\n𝘉𝘶 𝘣𝘰𝘵 𝘰𝘳𝘲𝘢𝘭𝘪 𝘴𝘪𝘻 ✅\n"
                                f"— 𝙸𝚗𝚜𝚝𝚊𝚐𝚛𝚊𝚖𝚍𝚊𝚗 𝚁𝚎𝚎𝚕𝚜 𝚟𝚊 𝙿𝚘𝚜𝚝 𝚢𝚞𝚔𝚕𝚊𝚜𝚑 🗳\n"
                                f"— 𝚃𝚒𝚔𝚃𝚘𝚔𝚍𝚊𝚗 𝚅𝚒𝚍𝚎𝚘 𝚢𝚞𝚔𝚕𝚊𝚜𝚑 📥\n— 𝙻𝚒𝚔𝚎𝚎𝚍𝚊𝚗 𝚅𝚒𝚍𝚎𝚘 𝚢𝚞𝚔𝚕𝚊𝚜𝚑 📂\n"
                                f"— 𝙿𝚒𝚗𝚝𝚎𝚛𝚎𝚜𝚝𝚍𝚊𝚗 𝚅𝚒𝚍𝚎𝚘 𝚟𝚊 𝚁𝚊𝚜𝚖 𝚢𝚞𝚔𝚕𝚊𝚜𝚑 🖇\n— 𝚄𝚜𝚎𝚛 𝚖𝚊'𝚕𝚞𝚖𝚘𝚝𝚕𝚊𝚛𝚒𝚗𝚐𝚒𝚣𝚗𝚒 𝚔𝚘'𝚛𝚒𝚜𝚑 👤\n\n"
                                f"Boshlash uchun bizga xabarning URL manzilini yuboring 🔗\n\n"
                                f"🗣 𝐁𝐨𝐭 𝐨𝐫𝐪𝐚𝐥𝐢 𝐭𝐚𝐥𝐚𝐛 𝐯𝐚 𝐭𝐚𝐤𝐥𝐢𝐟𝐥𝐚𝐫 𝐮𝐜𝐡𝐮𝐧: @Rozievich")


@dp.message_handler(commands=['help'])
async def help_handler(msg: types.Message):
    await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
    await bot.send_message(chat_id=msg.chat.id,
                           text="Sizning ma'lumotlaringiz /info bunda sizga Telegram ID, Username, Ism, Familiya taqdim etamiz ✍️\n\nMavjud Url manzil kiritishingizni so'raymiz ✅\n\nBotda muammolar kuzatilsa Adminga murojat qiling! 👨🏻‍💻\n\nBiz muammolarni tez orada bartaraf etamiz! ⏳")  # noqa


@dp.message_handler(commands=['info'])
async def info_handler(msg: types.Message):
    await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
    await bot.send_message(chat_id=msg.chat.id,
                           text=f"𝐒𝐢𝐳𝐧𝐢𝐧𝐠 𝐌𝐚'𝐥𝐮𝐦𝐨𝐭𝐥𝐚𝐫𝐢𝐧𝐠𝐢𝐳 🗂\nɪᴅ: {msg.from_user.id}\nɪsᴍ: {msg.from_user.first_name}\nᴜsᴇʀɴᴀᴍᴇ: {'@' + msg.from_user.username if msg.from_user.username else '❌'}\n\n@Super_saverBot - 𝙱𝚒𝚣 𝚋𝚒𝚕𝚊𝚗 𝚑𝚊𝚖𝚖𝚊𝚜𝚒 𝚘𝚜𝚘𝚗 📥")


@dp.message_handler(commands=['panel'])
async def admin_panel(msg: types.Message):
    if msg.from_user.id == int(getenv("ADMIN")):
        await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
        await bot.send_message(chat_id=msg.chat.id,
                               text=f"𝐀𝐬𝐬𝐚𝐥𝐨𝐦𝐮 𝐚𝐥𝐚𝐲𝐤𝐮𝐦 {msg.from_user.full_name} 🤖\n𝙰𝚍𝚖𝚒𝚗 𝚜𝚊𝚑𝚒𝚏𝚊𝚐𝚊 𝚡𝚞𝚜𝚑 𝚔𝚎𝚕𝚒𝚋𝚜𝚒𝚣 🖇👤",
                               reply_markup=admin_btn())


@dp.message_handler(Text("📊 Statistics"))
async def user_statistic_handler(msg: types.Message):
    if msg.from_user.id == int(getenv("ADMIN")):
        data = user_statistic()
        await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
        await bot.send_message(chat_id=msg.chat.id, text=data)
    else:
        await bot.send_message(chat_id=msg.chat.id, text="𝗦𝗶𝘇 𝗮𝗱𝗺𝗶𝗻 𝗲𝗺𝗮𝘀𝘀𝗶𝘇 👨🏻‍💻❌",
                               reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text("🗣 Reklama"))
async def reklama_handler(msg: types.Message):
    if msg.from_user.id == int(getenv("ADMIN")):
        await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
        await ReklamaState.rek.set()
        await bot.send_message(chat_id=msg.chat.id, text="𝐑𝐞𝐤𝐥𝐚𝐦𝐚 𝐓𝐚𝐫𝐪𝐚𝐭𝐢𝐬𝐡 𝐛𝐨'𝐥𝐢𝐦𝐢 🤖", reply_markup=exit_btn())
    else:
        await bot.send_message(chat_id=msg.chat.id, text="𝗦𝗶𝘇 𝗮𝗱𝗺𝗶𝗻 𝗲𝗺𝗮𝘀𝘀𝗶𝘇 👨🏻‍💻❌",
                               reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=ReklamaState.rek, content_types=types.ContentType.ANY)
async def rek_state(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
        await bot.send_message(chat_id=msg.chat.id, text="𝐑𝐞𝐤𝐥𝐚𝐦𝐚 𝐲𝐮𝐛𝐨𝐫𝐢𝐬𝐡 𝐛𝐞𝐤𝐨𝐫 𝐪𝐢𝐥𝐢𝐧𝐝𝐢 🤖❌", reply_markup=admin_btn())
        await state.finish()
    else:
        await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
        await bot.send_message(chat_id=msg.chat.id, text="𝐑𝐞𝐤𝐥𝐚𝐦𝐚 𝐲𝐮𝐛𝐨𝐫𝐢𝐬𝐡 𝐛𝐨𝐬𝐡𝐚𝐧𝐝𝐢 🤖✅")
        summa = 0
        for i in user.get_medias():
            if int(i[1]) != int(getenv("ADMIN")):
                try:
                    await msg.copy_to(int(i[1]), caption=msg.caption, caption_entities=msg.caption_entities,
                                      reply_markup=msg.reply_markup)
                except:  # noqa
                    summa += 1
        await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
        await bot.send_message(int(getenv("ADMIN")), text=f"𝐁𝐨𝐭𝐧𝐢 𝐁𝐥𝐨𝐤𝐥𝐚𝐠𝐚𝐧 𝐮𝐬𝐞𝐫𝐥𝐚𝐫 𝐬𝐨𝐧𝐢: {summa}",
                               reply_markup=admin_btn())
        await state.finish()


@dp.message_handler(Text("📈 Media Statistics"))
async def media_statistic_handler(msg: types.Message):
    if msg.from_user.id == int(getenv("ADMIN")):
        data = media_statistic()
        await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
        await bot.send_message(chat_id=msg.chat.id, text=data)
    else:
        await bot.send_message(chat_id=msg.chat.id, text="𝗦𝗶𝘇 𝗮𝗱𝗺𝗶𝗻 𝗲𝗺𝗮𝘀𝘀𝗶𝘇 👨🏻‍💻❌",
                               reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text("👤 Find User"))
async def find_user_handler(msg: types.Message):
    if msg.from_user.id == int(getenv("ADMIN")):
        await FindUser.user_id.set()
        await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
        await bot.send_message(chat_id=msg.chat.id,
                               text="𝚀𝚒𝚍𝚒𝚛𝚕𝚊𝚢𝚘𝚝𝚐𝚊𝚗 𝚞𝚜𝚎𝚛𝚐𝚊 𝚝𝚎𝚐𝚒𝚜𝚑𝚕𝚒 𝚃𝚎𝚕𝚎𝚐𝚛𝚊𝚖 𝙸𝙳 𝚔𝚒𝚛𝚒𝚝𝚒𝚗𝚐 🔎🤖", reply_markup=exit_btn())
    else:
        await bot.send_message(chat_id=msg.chat.id, text="𝗦𝗶𝘇 𝗮𝗱𝗺𝗶𝗻 𝗲𝗺𝗮𝘀𝘀𝗶𝘇 👨🏻‍💻❌",
                               reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=FindUser.user_id)
async def find_user_result_handler(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await bot.send_message(chat_id=msg.chat.id, text="𝐔𝐬𝐞𝐫 𝐪𝐢𝐝𝐢𝐫𝐮𝐯𝐢 𝐛𝐞𝐤𝐨𝐫 𝐪𝐢𝐥𝐢𝐧𝐝𝐢 🔎🤖", reply_markup=admin_btn())
        await state.finish()
    else:
        data = find_user(msg.text)
        await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
        await bot.send_message(chat_id=msg.chat.id, text=data, reply_markup=admin_btn())
        await state.finish()


@dp.message_handler()
async def result_handler(msg: types.Message):
    await bot.send_chat_action(msg.chat.id, types.ChatActions.CHOOSE_STICKER)
    msg_sticer = await bot.send_sticker(chat_id=msg.chat.id, sticker=open(BASE + '/media/sticer.tgs', 'rb'))
    data = api.get_media(msg.text)
    if data and data['type'] == 'insta' and not data.get('post', False):
        await bot.send_chat_action(msg.chat.id, types.ChatActions.UPLOAD_VIDEO)
        try:
            await bot.send_video(chat_id=msg.chat.id, video=data['data'],
                                 caption=f"@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥")
            await msg_sticer.delete()
        except:
            await bot.send_video(chat_id=msg.chat.id, video=requests.get(data['data']).content,
                                 caption=f"@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥")
            await msg_sticer.delete()
    elif data and data['type'] == 'insta' and data.get('post', False):
        await bot.send_chat_action(msg.chat.id, types.ChatActions.UPLOAD_VIDEO)
        try:
            await bot.send_media_group(chat_id=msg.chat.id, media=data['data'])
            await msg_sticer.delete()
        except:
            await bot.send_media_group(chat_id=msg.chat.id, media=requests.get(data['data']).content)
            await msg_sticer.delete()
    elif data and data['type'] == 'likee':
        await bot.send_chat_action(msg.chat.id, types.ChatActions.UPLOAD_VIDEO)
        await bot.send_video(chat_id=msg.chat.id, video=requests.get(url=data['data']).content,
                            caption=f"@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥")
        await msg_sticer.delete()
    elif data and data['type'] == 'tiktok':
        await bot.send_chat_action(msg.chat.id, types.ChatActions.UPLOAD_VIDEO)
        await bot.send_video(chat_id=msg.chat.id, video=requests.get(url=data['data']).content,
                             caption=f"@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥")
        await msg_sticer.delete()
    elif data and data['type'] == 'pin':
        if data['post'] == 'gif':
            await bot.send_chat_action(msg.chat.id, types.ChatActions.UPLOAD_PHOTO)
            try:
                await bot.send_animation(chat_id=msg.chat.id, animation=data['data'],
                                        caption=f"@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥")
                await msg_sticer.delete()
            except:
                await bot.send_animation(chat_id=msg.chat.id, animation=requests.get(url=data['data']).content,
                                caption=f"@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥")
                await msg_sticer.delete()
        elif data['post'] == 'image':
            await bot.send_chat_action(msg.chat.id, types.ChatActions.UPLOAD_PHOTO)
            try:
                await bot.send_photo(chat_id=msg.chat.id, photo=data['data'],
                                    caption=f"@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥")
                await msg_sticer.delete()
            except:
                await bot.send_photo(chat_id=msg.chat.id, photo=requests.get(data['data']).content,
                                 caption=f"@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥")
                await msg_sticer.delete()
        elif data['post'] == 'video':
            await bot.send_chat_action(msg.chat.id, types.ChatActions.UPLOAD_VIDEO)
            try:
                await bot.send_video(chat_id=msg.chat.id, video=data['data'],
                                    caption=f"@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥")
                await msg_sticer.delete()
            except:
                await bot.send_video(chat_id=msg.chat.id, video=requests.get(data['data']).content,
                                    caption=f"@super_saverbot - 𝐎𝐫𝐪𝐚𝐥𝐢 𝐲𝐮𝐤𝐥𝐚𝐛 𝐨𝐥𝐢𝐧𝐝𝐢 📥")
                await msg_sticer.delete()
    else:
        await bot.send_chat_action(msg.chat.id, types.ChatActions.TYPING)
        await bot.send_message(chat_id=msg.chat.id,
                               text="𝐁𝐮𝐧𝐝𝐚𝐲 𝐔𝐑𝐋 𝐦𝐚𝐧𝐳𝐢𝐥 𝐦𝐚𝐯𝐣𝐮𝐝 𝐞𝐦𝐚𝐬 𝐢𝐥𝐭𝐢𝐦𝐨𝐬 𝐭𝐞𝐤𝐬𝐡𝐢𝐫𝐢𝐛 𝐪𝐚𝐲𝐭𝐚𝐝𝐚𝐧 𝐲𝐮𝐛𝐨𝐫𝐢𝐧𝐠 🔎📂❌")
        await msg_sticer.delete()


async def startup(dp):
    create_db()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=startup, skip_updates=True)
