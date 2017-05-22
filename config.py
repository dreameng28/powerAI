tianchi_power_csv = '/Users/dreameng/Downloads/Tianchi_power.csv'
yangzhong_weather_csv = '/Users/dreameng/Downloads/yangzhong_weather.csv'
record_date = 'record_date'
user_id = 'user_id'
power_consumption = 'power_consumption'
highest_temperature = 'highest_temperature'
lowest_temperature = 'lowest_temperature'
weather = 'weather'
wind_direction = 'wind_direction'
wind_power = 'wind_power'

# train_start_id = 1
# train_end_id = 1000
# validate_start_id = 1001
# validate_end_id = 1454
# predict_start_id = 1
# predict_end_id = 1454


train_feature_start_date = '2015/1/1'
train_feature_end_date = '2016/6/30'

validate_feature_start_date = '2015/1/1'
validate_feature_end_date = '2016/7/31'

predict_feature_start_date = '2015/1/1'
predict_feature_end_date = '2016/8/31'

train_start_date = '2016/1/1'
train_end_date = '2016/7/31'

validate_start_date = '2016/8/1'
validate_end_date = '2016/8/31'

predict_start_date = '2016/9/1'
predict_end_date = '2016/9/30'

train_data_path = 'data/data_path/train_data.csv'
validate_data_path = 'data/data_path/validate_data.csv'
predict_data_path = 'data/data_path/predict_data.csv'

train_feature_data_path = 'data/feature_data_path/train_feature_data.csv'
validate_feature_data_path = 'data/feature_data_path/validate_feature_data.csv'
predict_feature_data_path = 'data/feature_data_path/predict_feature_data.csv'

train_feature_path = 'data/feature_path/train_features.csv'
validate_feature_path = 'data/feature_path/validate_features.csv'
predict_feature_path = 'data/feature_path/predict_features.csv'

holiday_set = {
    # 2015年份
    # 元旦
    '2015/1/1',
    '2015/1/2',
    '2015/1/3',
    # 春节
    '2015/2/18',
    '2015/2/19',
    '2015/2/20',
    '2015/2/21',
    '2015/2/22',
    '2015/2/23',
    '2015/2/24'
    # 清明
    '2015/4/4',
    '2015/4/5',
    '2015/4/6',
    # 五一
    '2015/5/1',
    '2015/5/2',
    '2015/5/3',
    # 端午
    '2015/6/20',
    '2015/6/21',
    '2015/6/22',
    # 胜利日
    '2015/9/3',
    '2015/9/4',
    '2015/9/5',
    # 中秋
    '2015/9/27',
    # 国庆
    '2015/10/1',
    '2015/10/2',
    '2015/10/3',
    '2015/10/4',
    '2015/10/5',
    '2015/10/6',
    '2015/10/7',

    # 2016年份
    # 元旦
    '2016/1/1',
    '2016/1/2',
    '2016/1/3',
    # 春节
    '2016/2/7',
    '2016/2/8',
    '2016/2/9',
    '2016/2/10',
    '2016/2/11',
    '2016/2/12',
    '2016/2/13',
    # 清明
    '2016/4/4',
    '2016/4/3',
    '2016/4/2',
    # 五一
    '2016/4/30'
    '2016/5/1',
    '2016/5/2',
    # 端午
    '2016/6/9',
    '2016/6/10',
    '2016/6/11',
    # 中秋
    '2016/9/15',
    '2016/9/16',
    '2016/9/17',
}

buban_set = {
    # 2015年份
    # 元旦
    '2015/1/4',
    # 春节
    '2015/2/15',
    '2015/2/28',
    # 胜利日
    '2015/9/6',
    # 国庆
    '2015/10/10',

    # 2016年份
    # 春节
    '2016/2/14',
    # 端午
    '2016/6/12',
    # 中秋
    '2016/9/18',
}
