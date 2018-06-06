# -*- coding: utf-8 -*-
import pandas as pd
from convertdate import islamic
from .utils import *

class irHoliday(object):

    def to_df(self,start_year, end_year):
        self.df= pd.DataFrame([],columns=['time_x', 'event_name', 'holiday', 'date'])

        for year in range(start_year, end_year+1):
            for month in range(1, 13):
                POSTstr = "Year={}&Month={}&Base1=0&Base2=1&Base3=2&Responsive=true".format(year, month)
                r = req(POSTstr)
                soup = soup_obj(r)
                temp = month_extractor(soup)
                temp['date'] = temp.time_x.apply(text_jalali_to_date, args=[year])
                self.df = self.df.append(temp.drop_duplicates())

        self.df['jalali_date'] = self.df['date'].apply(lambda date: khayyam.JalaliDate((date)))
        self.df['hijri_date'] = self.df.apply(
            lambda df: islamic.from_gregorian(df.date.year,df.date.month,df.date.day),axis=1)
        self.df['hijri_date'] = self.df.hijri_date.apply(lambda x: khayyam.JalaliDate(x[0], x[1], x[2]))
        return self.df.reset_index(drop=True)
