# -*- coding: utf-8 -*-
import pandas as pd
from .utils import *
import jdatetime

__all__ = ['irHoliday']


class irHoliday(object):

    def _main(self, start_year, end_year=None):
        if end_year is None:
            end_year = start_year
        self.df = pd.DataFrame([], columns=['time_x', 'event_name', 'holiday', 'date'])

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                POSTstr = "Year={}&Month={}&Base1=0&Base2=1&Base3=2&Responsive=true".format(year, month)
                r = req(POSTstr)
                soup = soup_obj(r)
                temp = month_data_extractor(soup)
                temp['date'] = temp.time_x.apply(text_jalali_to_date, args=[year])
                self.df = pd.concat([self.df,temp.drop_duplicates()])
                self.df.dropna(inplace=True)

        self.df['jalali_date'] = self.df['date'].apply(lambda date: jdatetime.date.fromgregorian(date=date))

        return self.df.reset_index(drop=True)

    def to_df(self, start_year, end_year=None):
        self._main(start_year, end_year)
        return self.df

    def get_holidays(self, start_year, end_year=None):
        self._main(start_year, end_year)
        df_holiday = self.df[self.df['holiday'] == 1].reset_index()
        del df_holiday['index']
        return df_holiday

    def to_csv(self, start_year, end_year=None, path='irholidays.csv'):
        self._main(start_year, end_year)
        return self.df.to_csv(path, index=False)
