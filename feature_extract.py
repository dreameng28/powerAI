from config import *
import pandas as pd
from util import *
from data_view import DataView


# 时间特征

# 年月特征
def year_month_day(df):
    year = df[record_date].map(lambda x: x.split('/')[0])
    year.name = 'year'
    month = df[record_date].map(lambda x: x.split('/')[1])
    month.name = 'month'
    day = df[record_date].map(lambda x: x.split('/')[2])
    day.name = 'day'
    onehot_data = [0] * 12
    onehot_datas = []
    for each in month:
        each = int(each) - 1
        onehot_data[each] = 1
        onehot_datas.append(onehot_data)
        onehot_data = [0] * 12
    frame_m = pd.DataFrame(data=onehot_datas, columns=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    return df.join(year).join(month).join(frame_m)


# 星期特征
def coupon_receive_day(df):
    data = df[record_date].map(lambda x: date2day(x))
    data.name = 'week'
    onehot_data = [0] * 7
    onehot_datas = []
    for each in data:
        each = int(each) - 1
        onehot_data[each] = 1
        onehot_datas.append(onehot_data)
        onehot_data = [0] * 7
    frame = pd.DataFrame(data=onehot_datas, columns=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    return df.join(data).join(frame)


# 是否法定节假日
def is_holiday(df):
    holiday = df[record_date].map(lambda x: 1 if x in holiday_set else 0)
    holiday.name = 'is_holiday'
    return df.join(holiday)


# 是否补班
def is_buban(df):
    buban = df[record_date].map(lambda x: 1 if x in buban_set else 0)
    buban.name = 'is_buban'
    return df.join(buban)

date_features = [year_month_day, coupon_receive_day, is_holiday, is_buban]


# 用户特征
# 用户每日用电量的平均数、中位数、方差、最大值、最小值
def user_info(df):
    grouped = df[[user_id, power_consumption]].groupby([user_id], as_index=False)
    user_power_mean = grouped.mean()
    user_power_median = grouped.median()
    user_power_var = grouped.var()
    user_power_max = grouped.max()
    user_power_min = grouped.min()
    user_power_mean = user_power_mean.rename(columns={power_consumption: 'user_power_mean'})
    user_power_median = user_power_median.rename(columns={power_consumption: 'user_power_median'})
    user_power_var = user_power_var.rename(columns={power_consumption: 'user_power_var'})
    user_power_max = user_power_max.rename(columns={power_consumption: 'user_power_max'})
    user_power_min = user_power_min.rename(columns={power_consumption: 'user_power_min'})
    return pd.merge(user_power_mean, user_power_median).merge(user_power_var).\
        merge(user_power_max).merge(user_power_min)


# 用户对应月份每日用电量的平均数、中位数、方差、最大值、最小值
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


# 用户对应星期每日用电量的平均数、中位数、方差、最大值、最小值
def user_info_w(df):
    grouped = df[[user_id, 'week', power_consumption]].groupby([user_id, 'week'], as_index=False)
    user_power_mean_w = grouped.mean()
    user_power_median_w = grouped.median()
    user_power_var_w = grouped.var()
    user_power_max_w = grouped.max()
    user_power_min_w = grouped.min()
    user_power_mean_w = user_power_mean_w.rename(columns={power_consumption: 'user_power_mean_w'})
    user_power_median_w = user_power_median_w.rename(columns={power_consumption: 'user_power_median_w'})
    user_power_var_w = user_power_var_w.rename(columns={power_consumption: 'user_power_var_w'})
    user_power_max_w = user_power_max_w.rename(columns={power_consumption: 'user_power_max_w'})
    user_power_min_w = user_power_min_w.rename(columns={power_consumption: 'user_power_min_w'})
    return pd.merge(user_power_mean_w, user_power_median_w).merge(user_power_var_w).\
        merge(user_power_max_w).merge(user_power_min_w)


# 用户对应是否节假日用电量的平均数、中位数、方差、最大值、最小值
def user_info_h(df):
    grouped = df[[user_id, 'is_holiday', power_consumption]].groupby([user_id, 'is_holiday'], as_index=False)
    user_power_mean_h = grouped.mean()
    user_power_median_h = grouped.median()
    user_power_var_h = grouped.var()
    user_power_max_h = grouped.max()
    user_power_min_h = grouped.min()
    user_power_mean_h = user_power_mean_h.rename(columns={power_consumption: 'user_power_mean_h'})
    user_power_median_h = user_power_median_h.rename(columns={power_consumption: 'user_power_median_h'})
    user_power_var_h = user_power_var_h.rename(columns={power_consumption: 'user_power_var_h'})
    user_power_max_h = user_power_max_h.rename(columns={power_consumption: 'user_power_max_h'})
    user_power_min_h = user_power_min_h.rename(columns={power_consumption: 'user_power_min_h'})
    return pd.merge(user_power_mean_h, user_power_median_h).merge(user_power_var_h).\
        merge(user_power_max_h).merge(user_power_min_h)


# 用户对应月份前一月每日用电量的平均数、中位数、方差、最大值、最小值
def user_info_m_p(df):
    date2 = df[record_date].map(lambda x: str2time(x)).max()
    date1 = datetime.datetime(date2.year, date2.month, 1).date()
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


# # 用户1-8月较15年的增长率
# def rise_rate(df):
#     df15 = DataView(tianchi_power_csv).filter_by_record_date('2015/1/1', '2015/8/31')
#     df16 = DataView(tianchi_power_csv).filter_by_record_date('2016/1/1', '2016/8/31')
#     grouped15 = df15[[user_id, power_consumption]].groupby(user_id, as_index=False).sum()
#     grouped16 = df16[[user_id, power_consumption]].groupby(user_id, as_index=False).sum()
#     user_rise_rate = pd.Series(map(lambda x, y: float(y - x) / x, grouped15[power_consumption], grouped16[power_consumption]))
#     user_rise_rate.name = 'user_rise_rate'
#     return grouped15.join(user_rise_rate).drop(power_consumption, axis=1)


user_features = [user_info, user_info_w, user_info_h, user_info_m, user_info_m_p]


def extract_features(data_path, feature_data_path):
    data_frame = pd.read_csv(data_path)
    feature_data_frame = pd.read_csv(feature_data_path)
    print('extract date features...')
    for f in date_features:
        data_frame = f(data_frame)
        feature_data_frame = f(feature_data_frame)

    print('extract user features...')
    for f in user_features:
        data_frame = data_frame.merge(f(feature_data_frame))
    data_frame.drop('week', axis=1)
    return data_frame


if __name__ == '__main__':
    for i in range(len(date_durations)):
        print('extract num{} feature'.format(str(i)))
        extract_features(data_paths.format(str(i)), feature_data_paths.format(str(i)))\
            .to_csv(feature_paths.format(str(i)), index=False)
