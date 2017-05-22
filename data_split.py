from data_view import DataView
from config import *

if __name__ == '__main__':
    data_view = DataView(tianchi_power_csv)

    train_data_set = data_view.filter_by_record_date(train_start_date, train_end_date)
    validate_data_set = data_view.filter_by_record_date(validate_start_date, validate_end_date)
    train_data_set.to_csv(train_data_path, index=False)
    validate_data_set.to_csv(validate_data_path, index=False)

    train_feature_data_set = data_view.filter_by_record_date(train_feature_start_date, train_feature_end_date)
    validate_feature_data_set = data_view.filter_by_record_date(validate_feature_start_date, validate_feature_end_date)
    predict_feature_data_set = data_view.filter_by_record_date(predict_feature_start_date, predict_feature_end_date)
    train_feature_data_set.to_csv(train_feature_data_path, index=False)
    validate_feature_data_set.to_csv(validate_feature_data_path, index=False)
    predict_feature_data_set.to_csv(predict_feature_data_path, index=False)
