import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
import xgboost as xgb
from sklearn.metrics import mean_squared_error


class Analytics:
    def __init__(self) -> None:
        pass
    FEATURES = ['dayofweek', 'quarter', 'month',
                'dayofyear', 'year', 'Special Day']
    # def load_model():
    #     # To load the trained model from local..
    #     reg_v2 = xgb.XGBRFRegressor()
    #     reg_v2.load_model('xg_model_v2.json')

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

    def predict_data(df, start_date, end_date) -> pd.DataFrame:
        # Create future dataframe
        future = pd.date_range(start=start_date, end=end_date, freq='1d')
        future_df = pd.DataFrame(index=future)
        future_df['isFuture'] = True
        df['isFuture'] = False
        df_and_future = pd.concat([df, future_df])
        df_and_future = Analytics.create_features(df_and_future)
        # df_and_future = add_lags(df_and_future)
        future_w_features = df_and_future.query('isFuture').copy()
        reg = xgb.XGBRFRegressor()
        reg.load_model('models/xg_model_v3.json')
        future_w_features['pred'] = reg.predict(
            future_w_features[Analytics.FEATURES])

        return future_w_features
