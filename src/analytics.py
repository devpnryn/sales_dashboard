import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import os


class Analytics:
    def __init__(self) -> None:
        pass
    FEATURES = ['dayofweek', 'quarter', 'month',
                'dayofyear', 'year', 'Special Day']

    def create_features(df):
        """
        Create time series features based on time series index 
        """
        df = df.copy()
        df['dayofweek'] = df.index.day_of_week
        df['quarter'] = df.index.quarter
        df['month'] = df.index.month
        df['dayofyear'] = df.index.day_of_year
        df['year'] = df.index.year
        return df

    def predict_data(df, selected_product, start_date, end_date) -> pd.DataFrame:
        # Create future dataframe
        future = pd.date_range(start=start_date, end=end_date, freq='D')
        future_df = pd.DataFrame(index=future)
        future_df['isFuture'] = True

        # filter the data by product name
        df = df[df.Product == selected_product]
        # print(df)
        df['isFuture'] = False
        df_and_future = pd.concat([df, future_df])
        df_and_future['Special Day'] = df_and_future['Special Day'].astype(
            'boolean')
        df_and_future = Analytics.create_features(df_and_future)
        future_w_features = df_and_future.query('isFuture').copy()
        reg = xgb.XGBRegressor(enable_categorical=True)
        cwd = os.getcwd()
        model_name = f'models/xg_model_{selected_product}.json'
        # reg.load_model(model_name)
        if os.path.exists(model_name):
            reg.load_model(model_name)
            print(f'found model at {model_name}')
        else:
            reg.load_model('models/xg_model_v2.json')
        tobe_predicted_on = future_w_features[Analytics.FEATURES]
        tobe_predicted_on['pred'] = reg.predict(tobe_predicted_on)

        # return future_w_features
        tobe_predicted_on['pred'] = tobe_predicted_on['pred'].apply(np.int64)
        return tobe_predicted_on
