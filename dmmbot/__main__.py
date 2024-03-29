import re

from . import bot
from .util import Inline_search_markup
from .handler import inline_handler, inline_result_handler, callback_handler, video_id_handler

from pyrogram import filters, enums

async def group_filter(_, __, message):
    me = await bot.get_me()
    return message.chat.type == enums.ChatType.PRIVATE or re.search(me.username, message.text)

group_filter = filters.create(group_filter)

@bot.on_inline_query()
async def inline_query(client, inline_query):
    await inline_handler(inline_query)

@bot.on_message(filters.command('start') & group_filter)
async def start(client, message):
    await message.reply_text("FANZA（原DMM.R18）影片检索", reply_markup=Inline_search_markup)

@bot.on_chosen_inline_result()
async def edit_inline_result(client, result):
    await inline_result_handler(result, bot)

@bot.on_callback_query()
async def force_edit_inline_result(client, callback):
    await callback_handler(callback)

@bot.on_message(filters.regex('^[a-zA-Z][a-zA-Z]+-\d+$'))
async def reply_video_id(clinet, message):
    await video_id_handler(message)

bot.run()
