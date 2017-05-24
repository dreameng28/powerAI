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

    def filter_by_record_date2(self, date1, date2):
        return self.df[self.df[record_date].map(lambda x: True if date1 <= str2time(str(x)) <= date2 else False)]

    # def filter_by_user_id(self, id1, id2):
    #     return self.df[self.df[user_id].map(lambda x: True if id1 <= x <= id2 else False)]


# 用户1-8月较15年的增长率
def rise_rate(df):
    df15 = DataView(df).filter_by_record_date('2015/1/1', '2015/8/31')
    df16 = DataView(df).filter_by_record_date('2016/1/1', '2016/8/31')
    grouped15 = df15[[user_id, power_consumption]].groupby(user_id, as_index=False).sum()
    grouped16 = df16[[user_id, power_consumption]].groupby(user_id, as_index=False).sum()
    user_rise_rate = pd.Series(map(lambda x, y: float(y - x) / x, grouped15[power_consumption], grouped16[power_consumption]))
    user_rise_rate.name = 'user_rise_rate'
    return grouped15.join(user_rise_rate).drop(power_consumption, axis=1)


# 用户对应星期每日用电量的平均数、中位数、方差、最大值、最小值
def user_info_m(df):
    grouped = df[[user_id, 'month', power_consumption]].groupby([user_id, 'month'], as_index=False)
    user_power_mean_m = grouped.mean()
    user_power_median_m = grouped.median()
    user_power_var_m = grouped.var()
    user_power_max_m = grouped.max()
    user_power_min_m = grouped.min()
    user_power_mean_m = user_power_mean_m.rename(columns={power_consumption: 'user_power_mean_m'})
    user_power_median_m = user_power_median_m.rename(columns={power_consumption: 'user_power_median_m'})
    user_power_var_m = user_power_var_m.rename(columns={power_consumption: 'user_power_var_m'})
    user_power_max_m = user_power_max_m.rename(columns={power_consumption: 'user_power_max_m'})
    user_power_min_m = user_power_min_m.rename(columns={power_consumption: 'user_power_min_m'})
    return pd.merge(user_power_mean_m, user_power_median_m).merge(user_power_var_m).\
        merge(user_power_max_m).merge(user_power_min_m)


# 用户对应月份前一月每日用电量的平均数、中位数、方差、最大值、最小值
def user_info_m_p(df):
    date2 = df[record_date].map(lambda x: str2time(x)).max()
    date1 = datetime.datetime(date2.year, date2.month, 1).date()
    print(date1, date2)
    grouped = DataView(df).filter_by_record_date2(date1, date2)[[user_id, 'month', power_consumption]].groupby([user_id, 'month'], as_index=False)
    user_power_mean_m = grouped.mean()
    user_power_median_m = grouped.median()
    user_power_var_m = grouped.var()
    user_power_max_m = grouped.max()
    user_power_min_m = grouped.min()
    user_power_mean_m = user_power_mean_m.rename(columns={power_consumption: 'user_power_mean_m_p'})
    user_power_median_m = user_power_median_m.rename(columns={power_consumption: 'user_power_median_m_p'})
    user_power_var_m = user_power_var_m.rename(columns={power_consumption: 'user_power_var_m_p'})
    user_power_max_m = user_power_max_m.rename(columns={power_consumption: 'user_power_max_m_p'})
    user_power_min_m = user_power_min_m.rename(columns={power_consumption: 'user_power_min_m_p'})
    return pd.merge(user_power_mean_m, user_power_median_m).merge(user_power_var_m).\
        merge(user_power_max_m).merge(user_power_min_m).drop('month', axis=1)

if __name__ == '__main__':
    df1 = pd.read_csv(feature_paths.format(str(0)))
    df2 = pd.read_csv(feature_paths.format(str(1)))
    print(len(df1), len(df2))
    df = pd.DataFrame(pd.concat([df1, df2], axis=0)).reset_index().drop('index', axis=1)
    print(df)
