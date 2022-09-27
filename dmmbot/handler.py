import re

from .util import build_inline_answer, build_message

from pyrogram import enums

async def inline_handler(inline_query):
    query = inline_query.query
    answer = build_inline_answer(query)
    await inline_query.answer(answer, cache_time=0)

async def inline_result_handler(result, bot):
    cid = result.result_id
    msg = build_message(cid)
    await bot.edit_inline_text(result.inline_message_id, msg['text'], reply_markup=msg['markup'])

async def callback_handler(callback):
    await callback.answer("wait")
    cid = callback.data
    msg = build_message(cid)
    await callback.edit_message_text(msg['text'], reply_markup=msg['markup'])

async def video_id_handler(message):
    await message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
    cid = re.sub('-', '00', re.search(r'\w+-\d+', message.text).group())
    try:
        msg = build_message(cid.lower())
    except:
        await message.reply_text("🈚️")
        return None
    await message.reply_text(msg['text'], reply_markup=msg['markup'])
