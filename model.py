import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
import sys
from config import *


def x_label(feature_path, pred=False):
    if not pred:
        X = pd.read_csv(feature_path)
        y = X[power_consumption].tolist()
        X = X.drop([record_date, user_id, power_consumption], axis=1)
        columns = X.columns
        X = X.values
        return X, y, columns
    else:
        X = pd.read_csv(feature_path)
        X = X.drop([record_date, user_id], axis=1)
        columns = X.columns
        X = X.values
        return X, columns


def predict(dmatrix, data_path, save_path, save_path2):
    preds = bst.predict(dmatrix, ntree_limit=bst.best_ntree_limit)
    print(preds)
    preds = pd.Series(preds)
    preds = preds.map(lambda x: int(x))
    preds.name = 'predict_power_consumption'
    preds_df = pd.read_csv(data_path).join(preds)
    preds_df.to_csv(save_path, index=False)
    preds_df = preds_df.drop(user_id, axis=1).groupby(record_date, as_index=False).sum()
    preds_df = preds_df.rename(columns={record_date: 'predict_date'})
    preds_df.to_csv(save_path2, index=False)

save_stdout = sys.stdout
X_train, y_train, train_columns = x_label(train_feature_path)
X_validate, y_validate, validate_columns = x_label(validate_feature_path)
X_predict, predict_columns = x_label(predict_feature_path, pred=True)

dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=train_columns)
dvalidate = xgb.DMatrix(X_validate, label=y_validate, feature_names=validate_columns)
dpredict = xgb.DMatrix(X_predict, feature_names=predict_columns)

param = {'max_depth': 5, 'eta': 0.1, 'silent': 0}
num_round = 500
watchlist = [(dtrain, 'train'), (dvalidate, 'eval')]
with open('log', 'w+') as outf:
    sys.stdout = outf
    bst = xgb.train(param, dtrain, num_round, evals=watchlist, early_stopping_rounds=100)
xgb.plot_importance(bst)
plt.gcf().savefig('feature_importance.png')
plt.close()

sys.stdout = save_stdout

predict(dvalidate, validate_data_path, 'validate.csv', 'Tianchi_power_predict_table_v.csv')
predict(dpredict, predict_data_path, 'predict.csv', 'Tianchi_power_predict_table.csv')
