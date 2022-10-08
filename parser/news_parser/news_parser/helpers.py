import re

MONTH_DICT = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12',
}

def get_date_from_url(url, mode='eng'):
    pattern = r'(/\d+/\d+/\d+/)'
    match = re.search(pattern, url)
    date = match.group(1)
    if not match:
        return None
    if mode == 'eng':
        date = f'{date[1:5]}-{date[6:8]}-{date[9:11]}'
    else:
        date = f'{date[7:11]}-{date[4:6]}-{date[1:3]}'
    return date


def get_date_from_text(text):
    if text == '1 день назад':
        return '2022-10-07'
    elif text == '2 дня назад':
        return '2022-10-06'
    elif text == '3 дня назад':
        return '2022-10-05'

    day = text[:2]
    year = text[-4:]
    month_name = re.search(r'\s(\w+)\s', text).group(1)
    month = MONTH_DICT[month_name]
    return f'{year}-{month}-{day}'
