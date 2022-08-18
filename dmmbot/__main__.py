from .client import client

from .handler import inline_handler, start_handler, inline_result_handler, callback_handler

from pyrogram import filters

bot = client()

@bot.on_inline_query()
async def inline_query(client, inline_query):
    await inline_handler(inline_query)

@bot.on_message(filters.command('start'))
async def start(client, message):
    await start_handler(message, bot)

@bot.on_chosen_inline_result()
async def edit_inline_result(client, result):
    await inline_result_handler(result, bot)

@bot.on_callback_query()
async def force_edit_inline_result(client, callback):
    await callback_handler(callback)

bot.run()
