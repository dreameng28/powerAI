from config import *
import pandas as pd
from util import *
from data_view import DataView


# 时间特征

# 年月日特征
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
    onehot_data = [0] * 31
    onehot_datas = []
    for each in day:
        each = int(each) - 1
        onehot_data[each] = 1
        onehot_datas.append(onehot_data)
        onehot_data = [0] * 31
    frame_d = pd.DataFrame(data=onehot_datas, columns=['day' + str(i) for i in range(1, 32)])
    return df.join(year).join(month).join(day).join(frame_m).join(frame_d)


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
    unique_users_info = df[[user_id]].drop_duplicates()
    for i in range(1, 13):
        unique_users_info = unique_users_info.merge(
            pd.merge(user_power_mean_m, user_power_median_m).merge(user_power_var_m). \
                merge(user_power_max_m).merge(user_power_min_m)[user_power_median_m['month'] == str(i)].drop('month', axis=1) \
                .rename(columns={
                'user_power_mean_m': 'user_power_mean_m' + str(i),
                'user_power_median_m': 'user_power_median_m' + str(i),
                'user_power_var_m': 'user_power_var_m' + str(i),
                'user_power_max_m': 'user_power_max_m' + str(i),
                'user_power_min_m': 'user_power_min_m' + str(i)
            }))
    return unique_users_info


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
    unique_users_info = df[[user_id]].drop_duplicates()
    for i in range(1, 8):
        unique_users_info = unique_users_info.merge(pd.merge(user_power_mean_w, user_power_median_w).merge(user_power_var_w). \
            merge(user_power_max_w).merge(user_power_min_w)[user_power_median_w['week'] == i].drop('week', axis=1)\
            .rename(columns={
            'user_power_mean_w': 'user_power_mean_w' + str(i),
            'user_power_median_w': 'user_power_median_w' + str(i),
            'user_power_var_w': 'user_power_var_w' + str(i),
            'user_power_max_w': 'user_power_max_w' + str(i),
            'user_power_min_w':'user_power_min_w' + str(i)
        }))
    return unique_users_info


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
    unique_users_info = df[[user_id]].drop_duplicates()
    for i in range(0, 2):
        unique_users_info = unique_users_info.merge(
            pd.merge(user_power_mean_h, user_power_median_h).merge(user_power_var_h). \
                merge(user_power_max_h).merge(user_power_min_h)[user_power_median_h['is_holiday'] == i].drop('is_holiday', axis=1) \
                .rename(columns={
                'user_power_mean_h': 'user_power_mean_h' + str(i),
                'user_power_median_h': 'user_power_median_h' + str(i),
                'user_power_var_h': 'user_power_var_h' + str(i),
                'user_power_max_h': 'user_power_max_h' + str(i),
                'user_power_min_h': 'user_power_min_h' + str(i)
            }))
    return unique_users_info


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


# 企业是否正常运转
def is_alive(df):
    date2 = df[record_date].map(lambda x: str2time(x)).max()
    date1 = datetime.datetime(date2.year, date2.month, 1).date()
    from dateutil.relativedelta import relativedelta
    date1 -= relativedelta(months=+2)
    grouped = DataView(df).filter_by_record_date2(date1, date2)[[user_id, power_consumption]].groupby([user_id], as_index=False).mean()
    alive = grouped[power_consumption].map(lambda x: 0 if x < 10 else 1)
    alive.name = 'is_alive'
    return grouped.join(alive).drop(power_consumption, axis=1)


# 用户上月较上上月的增长率
def rise_rate(df):
    date1_2 = df[record_date].map(lambda x: str2time(x)).max()
    date1_1 = datetime.datetime(date1_2.year, date1_2.month, 1).date()
    grouped1 = DataView(df).filter_by_record_date2(date1_1, date1_2)[[user_id, power_consumption]].groupby([user_id], as_index=False).mean()
    from dateutil.relativedelta import relativedelta
    date2_1 = date1_1 - relativedelta(months=+1)
    date2_2 = date1_2 - relativedelta(months=+1)
    grouped2 = DataView(df).filter_by_record_date2(date2_1, date2_2)[[user_id, power_consumption]].groupby([user_id], as_index=False).mean()
    user_rise_rate = pd.Series(map(lambda x, y: float(x - y) / y, grouped1[power_consumption], grouped2[power_consumption]))
    user_rise_rate.name = 'user_rise_rate'
    return grouped1[[user_id]].join(user_rise_rate)


user_features = [user_info, user_info_w, user_info_h, user_info_m, user_info_m_p, is_alive, rise_rate]


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
