import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
import sys
from config import *


def x_label(feature_path, pred=False):
    X_list = []
    for each in feature_path:
        X = pd.read_csv(feature_paths.format(str(each)))
        X_list.append(X)
    X = pd.DataFrame(pd.concat(X_list, axis=0)).reset_index().drop('index', axis=1)
    # print(X)
    if not pred:
        y = X[power_consumption].tolist()
        X = X.drop([record_date, user_id, power_consumption], axis=1)
        columns = X.columns
        X = X.values
        return X, y, columns
    else:
        X = X.drop([record_date, user_id], axis=1)
        columns = X.columns
        X = X.values
        return X, columns


def predict(dmatrix, data_path, save_path, save_path2):
    preds = bst.predict(dmatrix, ntree_limit=bst.best_ntree_limit)
    print(preds)
    preds = pd.Series(preds)
    preds.name = 'predict_power_consumption'
    preds_df = pd.read_csv(data_path).join(preds)
    preds_df.to_csv(save_path, index=False)
    preds_df = preds_df.drop(user_id, axis=1).groupby(record_date, as_index=False).sum()
    preds_df = preds_df.rename(columns={record_date: 'predict_date'})
    preds_df['predict_power_consumption'] = preds_df['predict_power_consumption'].astype(int)
    preds_df.to_csv(save_path2, index=False)

save_stdout = sys.stdout
X_train, y_train, train_columns = x_label([1, 2, 3, 5, 7, 6, 0])
X_validate, y_validate, validate_columns = x_label([4])
X_predict, predict_columns = x_label([8], pred=True)

dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=train_columns)
dvalidate = xgb.DMatrix(X_validate, label=y_validate, feature_names=validate_columns)
dpredict = xgb.DMatrix(X_predict, feature_names=predict_columns)

param = {'max_depth': 6, 'eta': 0.1, 'silent': 0}
num_round = 500
watchlist = [(dtrain, 'train'), (dvalidate, 'eval')]
with open('log', 'w+') as outf:
    sys.stdout = outf
    bst = xgb.train(param, dtrain, num_round, evals=watchlist, early_stopping_rounds=100)
xgb.plot_importance(bst)
plt.gcf().set_size_inches(20, 16)
plt.gcf().set_tight_layout(True)
plt.gcf().savefig('feature_importance.png')
plt.close()

sys.stdout = save_stdout

predict(dvalidate, data_paths.format(str(4)), 'validate.csv', 'Tianchi_power_predict_table_v.csv')
predict(dpredict, data_paths.format(str(8)), 'predict.csv', 'Tianchi_power_predict_table.csv')
