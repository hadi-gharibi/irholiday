import requests
from bs4 import BeautifulSoup
import khayyam
import json
import pandas as pd
import re

def req(POSTstr):

    headers={'Host': 'www.time.ir',
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.time.ir/',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '57',
    'Connection': 'keep-alive'
    }

    url='http://www.time.ir'
    r = requests.post(url=url,data=json.dumps(POSTstr),headers=headers)
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
    df = a1.merge(a2,how='left',on='event_name').fillna(0)
    df.ix[df.time_y != 0 ,'time_y'] = 1
    df.rename(columns={'time_y':'holiday'},inplace=True)
    return df


def df_maker(df):
    df = pd.DataFrame(df)
    df.columns = df.iloc[0]
    return df.reindex(df.index.drop(0))


def holiday_extractor(events):
    return events.find_all('li',attrs={'class': 'eventHoliday'})


def text_jalali_to_date(text, year):
    translation_dest = '0123456789'
    translation_src = '۰۱۲۳۴۵۶۷۸۹'
    translations = maketrans(translation_src, translation_dest)
    text = text.split(' ')
    day = int(text[0].translate(translations))
    month = text[1]
    month_list = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    month = month_list.index(month) + 1
    return khayyam.jalali_date.JalaliDate(year, month, day).todate()

def events_month_seprator(events):
    try:
        events = events.text
    except:
        pass
    events_list =  re.sub(' +',' ',events.strip()).split('\n\n\n')
    events_list = [event.split('\r\n',maxsplit=1) for event in events_list]
    for i,event in enumerate(events_list):
        for j,x in enumerate(event):
            events_list[i][j] = x.replace('\r\n' ,'').replace('\n\n\n','')
            if j == 1: events_list[i][j] = events_list[i][j][1:]
    return [['time','event_name']]+events_list

maketrans = lambda A, B: dict((ord(a), b) for a, b in zip(A, B))

