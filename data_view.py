from config import *
import pandas as pd
from util import *
import numpy as np


class DataView:
    def __init__(self, data):
        if isinstance(data, str):
            self.df = pd.read_csv(data)
            self.columns = self.df.columns.tolist()
        if isinstance(data, pd.DataFrame):
            self.df = data
            self.columns = self.df.columns.tolist()

    def filter_by_record_date(self, date1, date2):
        return self.df[self.df[record_date].map(lambda x: True if str2time(date1) <= str2time(str(x))
                                                                  <= str2time(date2) else False)]

    # def filter_by_user_id(self, id1, id2):
    #     return self.df[self.df[user_id].map(lambda x: True if id1 <= x <= id2 else False)]


# 用户对应年份每日用电量的平均数、中位数、方差
def user_info_y(df):
    grouped = df[[user_id, 'year', power_consumption]].groupby([user_id, 'year'], as_index=False)
    user_power_mean_y = grouped.mean()
    user_power_median_y = grouped.median()
    user_power_var_y = grouped.var()
    user_power_mean_y = user_power_mean_y.rename(columns={power_consumption: 'user_power_mean_y'})
    user_power_median_y = user_power_median_y.rename(columns={power_consumption: 'user_power_median_y'})
    user_power_var_y = user_power_var_y.rename(columns={power_consumption: 'user_power_var_y'})
    return pd.merge(user_power_mean_y, user_power_median_y).merge(user_power_var_y)


def user_info(df):
    grouped = df[[user_id, power_consumption]].groupby(user_id, as_index=False)
    user_power_hean = grouped.mean()
    user_power_hedian = grouped.median()
    user_power_var = grouped.var()
    user_power_hean = user_power_hean.rename(columns={power_consumption: 'user_power_hean'})
    user_power_hedian = user_power_hedian.rename(columns={power_consumption: 'user_power_hedian'})
    user_power_var = user_power_var.rename(columns={power_consumption: 'user_power_var'})
    return pd.merge(user_power_hean, user_power_hedian).merge(user_power_var)


def user_info_h(df):
    grouped = df[[user_id, 'is_holiday', power_consumption]].groupby([user_id, 'is_holiday'], as_index=False)
    user_power_hean_h = grouped.mean()
    user_power_hedian_h = grouped.median()
    user_power_var_h = grouped.var()
    user_power_mean_h = user_power_hean_h.rename(columns={power_consumption: 'user_power_mean_h'})
    user_power_median_h = user_power_hedian_h.rename(columns={power_consumption: 'user_power_median_h'})
    user_power_var_h = user_power_var_h.rename(columns={power_consumption: 'user_power_var_h'})
    return pd.merge(user_power_mean_h, user_power_median_h).merge(user_power_var_h)


# 用户1-8月较15年的增长率
def rise_rate(df):
    df15 = DataView(df).filter_by_record_date('2015/1/1', '2015/8/31')
    df16 = DataView(df).filter_by_record_date('2016/1/1', '2016/8/31')
    grouped15 = df15[[user_id, power_consumption]].groupby(user_id, as_index=False).sum()
    grouped16 = df16[[user_id, power_consumption]].groupby(user_id, as_index=False).sum()
    user_rise_rate = pd.Series(map(lambda x, y: float(y - x) / x, grouped15[power_consumption], grouped16[power_consumption]))
    user_rise_rate.name = 'user_rise_rate'
    return grouped15.join(user_rise_rate).drop(power_consumption, axis=1)

if __name__ == '__main__':
    # df = pd.read_csv(tianchi_power_csv)
    # grouped = df[[user_id, 'year', power_consumption]].groupby([user_id, 'year'], as_index=False)
    # df = grouped.median()
    # df = rise_rate(df)
    # print(df)
    dates = pd.date_range('2016/9/1', '2016/9/30')
    dates = list(map(lambda x: x.strftime('%Y/%-m/%-d'), dates)) * 1454
    ids = [i + 1 for i in range(1454)]
    ids = list(map(lambda x: [x] * 30, ids))
    ids = list(np.array(ids).flatten())
    pd.DataFrame({'record_date': dates, 'user_id': ids}).to_csv(predict_data_path, index=False)

    # grouped = df[[user_id, power_consumption]].groupby(user_id, as_index=False).sum()
    # frame = grouped[power_consumption].map(lambda x: float(x) / 31)
    # frame.name = 'power_per_day'
    # grouped = grouped.join(frame)
    # print(grouped)
    # s = set()
    # df = pd.read_csv(yangzhong_heather_csv)
    # print(df[weather])
    # for each in df[weather]:
    #     s.add(each)
    # print(s)
    # print(len(s))
