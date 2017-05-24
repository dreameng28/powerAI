from data_view import DataView
from config import *
import pandas as pd
import numpy as np


def generate_predict_data(n):
    dates = pd.date_range('2016/9/1', '2016/9/30')
    dates = list(map(lambda x: x.strftime('%Y/%-m/%-d'), dates)) * 1454
    ids = [i + 1 for i in range(1454)]
    ids = list(map(lambda x: [x] * 30, ids))
    ids = list(np.array(ids).flatten())
    pd.DataFrame({'record_date': dates, 'user_id': ids}).to_csv(data_paths.format(n), index=False)


if __name__ == '__main__':
    data_view = DataView(tianchi_power_csv)
    for i in range(len(date_durations)):
        print('generate num{} data'.format(str(i)))
        start_date, end_date = date_durations[i].split('-')
        data_view.filter_by_record_date(start_date, end_date).to_csv(data_paths.format(str(i)), index=False)
        start_date, end_date = feature_date_durations[i].split('-')
        data_view.filter_by_record_date(start_date, end_date).to_csv(feature_data_paths.format(str(i)), index=False)
    generate_predict_data(8)
