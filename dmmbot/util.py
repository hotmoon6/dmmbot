import re

from .api import method
from .api.type import Movie

from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
        InlineQueryResultArticle, InputTextMessageContent)

Inline_search_markup = InlineKeyboardMarkup([[InlineKeyboardButton('点击此处开始搜索', switch_inline_query_current_chat='')]])

def clean(text):
    return re.sub('\W', '_', text)

def build_inline_answer(query):
    if not query:
        results = method.random_results()
    elif re.match(r'\w+-\d+', query):
        keyword = re.sub('-', '00', re.search(r'\w+-\d+', query).group())
        results = method.search(keyword)
    else:
        results = method.search(query)
    answer = []
    for i in results[:10]:
        title = f"{i['title']}"
        if re.match('【VR】', i['title']):
            continue
        description = ' '.join(a['name'] for a in i['iteminfo'].get('actress', []))
        data = i['content_id']
        img = i['imageURL']['large']
        markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Loading...', callback_data=data)
                    ]
                ]
            )
        answer.append(InlineQueryResultArticle(title=title, description=description,
            input_message_content=InputTextMessageContent(title), reply_markup=markup, thumb_url=img, id=data))
    return answer

def build_message(cid):
    m = Movie(cid)
    keyword = re.search(r'[a-zA-Z]+\d+', cid).group()
    attribute = {
            '演员    ': ' '.join(f"#{i}" for i in m.actress),
            '系列    ': next(iter(m.series), None),
            '片长    ': f"{m.runtime} 分钟",
            '日期    ': m.date,
            '制作商': ' '.join(f"#{clean(i)}" for i in m.maker),
            '发行商': ' '.join(f"#{clean(i)}" for i in m.label),
            '类别    ': ' '.join(i for i in m.genres)
            }
    attribute = '\n'.join(f"{k} {attribute[k]}" for k in attribute if attribute[k])
    text = f"{m.name}[ㅤ]({m.poster}) [DMM链接]({m.url})\n\n{attribute}"
    javlib_url = f"https://www.javlibrary.com/cn/vl_searchbyid.php?keyword={keyword}"
    buttons = [InlineKeyboardButton('JAVLibrary', url=javlib_url)]
    if m.preview:
        buttons.insert(0, InlineKeyboardButton('预览', url=m.preview))
    markup = InlineKeyboardMarkup([buttons])
    return {'text': text, 'markup': markup}
