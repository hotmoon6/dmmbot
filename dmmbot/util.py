import re
import requests

from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
        InlineQueryResultArticle, InputTextMessageContent)

Inline_search_markup = InlineKeyboardMarkup([[InlineKeyboardButton('点击此处开始搜索', switch_inline_query_current_chat='')]])

API = 'https://api.dmm.com/affiliate/'    
# http://127.0.0.1:3662/api/

def build_inline_answer(query):
    if not query:
        results = requests.get(f"{API}top").json()
    else:
        results = requests.get(f"{API}query?keyword={query}").json()

    answer = []
    for i in results[:10]:
        keyword = re.search(r'[a-z]+\d+', i['cid']).group()
        pid = re.sub("00", "-", keyword).upper()
        title = f"{pid} {i['name']}"
        data = i['cid']
        img = i['poster']
        markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Loading...', callback_data=data)
                    ]
                ]
            )
        answer.append(InlineQueryResultArticle(title=title, input_message_content=InputTextMessageContent(title), reply_markup=markup, thumb_url=img, id=data))
    return answer

def build_message(cid):
    info = requests.get(f"{API}query?cid={cid}").json()
    keyword = re.search(r'[a-z]+\d+', cid).group()
    pid = re.sub("00", "-", keyword).upper()
    attribute = {
            '演员    ': ' '.join(f"#{i}" for i in info['actress']),
            '系列    ': info['series'],
            '片长    ': f"{info['runtime']} 分钟",
            '日期    ': info['date'],
            '制作商': info['maker'],
            '发行商': info['label'],
            '类别    ': ' '.join(info['genre'])
            }
    attribute = '\n'.join(f"{k} {attribute[k]}" for k in attribute if attribute[k])
    text = f"{pid} {info['name']}[\u200b]({info['poster']})\n\n{attribute}"
    javlib_url = f"https://www.javlibrary.com/cn/vl_searchbyid.php?keyword={keyword}"
    buttons = [InlineKeyboardButton('JAVLibrary', url=javlib_url)]
    preview = requests.head(f"{API}preview?cid={cid}").headers.get('Location')
    if preview:
        buttons.insert(0, InlineKeyboardButton('预览', url=preview))
    markup = InlineKeyboardMarkup([buttons])
    return {'text': text, 'markup': markup}

def getcid(pid):
    res = requests.get(f"{API}getcid?pid={pid}")
    if res.ok:
        return res.text
