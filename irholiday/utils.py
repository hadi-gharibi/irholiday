import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
import convert_numbers
import jdatetime

month_list = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'اَمرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
              'اسفند']

def holiday_correction(df):
    indexes = df.index[df['time_x'] == 0].tolist()
    for index in indexes:
        correct_value = df.iloc[index]['time_y'].strip('\n')
        wrong_value = df.iloc[index]['time_x']
        df["time_x"].replace({wrong_value: correct_value}, inplace=True)


def req(POSTstr):
    url = 'https://www.time.ir'
    r = requests.post(url=url+'?'+POSTstr)
    return r


def soup_obj(r):
    soup_obj = BeautifulSoup(r.text, 'html.parser')
    return soup_obj


def month_data_extractor(soup):
    events = soup.find('ul', attrs={'class': 'list-unstyled'})
    a1 = df_maker(events_month_seprator(events))
    holi = holiday_extractor(events)
    holi = '\n\n\n'.join(x.text for x in holi)
    a2 = df_maker(pd.DataFrame(events_month_seprator(holi)))
    if a2.iloc[0]['event_name'] is None:
        df = a1.copy()
        df['time_y'] = 0
        df.rename(columns={'time': 'time_x'}, inplace=True)
    else:
        df = a1.merge(a2, how='outer', on='event_name').fillna(0)
        holiday_correction(df)
    df.loc[df.time_y != 0, 'time_y'] = 1
    df.rename(columns={'time_y': 'holiday'}, inplace=True)
    return df


def df_maker(df):
    df = pd.DataFrame(df)
    df.columns = df.iloc[0]
    return df.reindex(df.index.drop(0))


def holiday_extractor(events):
    return events.find_all('li', attrs={'class': 'eventHoliday'})


def text_jalali_to_date(text, year):
    text = text.split(' ')
    day = int(convert_numbers.persian_to_english(text[0]))
    month = text[1]
    month = month_list.index(month) + 1
    try:
        return jdatetime.date(year, month,day).togregorian()
    except:
        return None


def events_month_seprator(events):
    try:
        events = events.text
    except:
        pass
    events_list = re.sub(' +', ' ', events.strip()).split('\n\n\n')
    events_list = [event.split('\r\n', maxsplit=1) for event in events_list]
    for i, event in enumerate(events_list):
        for j, x in enumerate(event):
            events_list[i][j] = x.replace('\r\n', '').replace('\n\n\n', '')
            if j == 1: events_list[i][j] = events_list[i][j][1:]
    return [['time', 'event_name']] + events_list

