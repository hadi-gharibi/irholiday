# -*- coding: utf-8 -*-
import pandas as pd
from .utils import *
__all__ = ['irHoliday']

class irHoliday(object):

    def main(self,start_year, end_year):
        self.df= pd.DataFrame([],columns=['time_x', 'event_name', 'holiday', 'date'])

        for year in range(start_year, end_year+1):
            for month in range(1, 13):
                POSTstr = "Year={}&Month={}&Base1=0&Base2=1&Base3=2&Responsive=true".format(year, month)
                r = req(POSTstr)
                soup = soup_obj(r)
                temp = month_data_extractor(soup)
                temp['date'] = temp.time_x.apply(text_jalali_to_date, args=[year])
                self.df = self.df.append(temp.drop_duplicates())

        self.df['jalali_date'] = self.df['date'].apply(lambda date: khayyam.JalaliDate((date)))

        return self.df.reset_index(drop=True)

    def to_df(self,start_year,end_year):
        self.main(start_year,end_year)
        return self.df
    def to_csv(self,start_year,end_year):
        self.main(start_year, end_year, path)
        return self.df.to_csv(path, index=False)
