import pandas as pd
import numpy as np


# reads the data from excel sheets
# creates df with proper index

def get_raw_dataframe(filename) -> pd.DataFrame:
    df = pd.concat(pd.read_excel(filename, sheet_name=None), ignore_index=True)
    df = df.set_index('Sale Date')
    df.index = pd.to_datetime(df.index, format="%d/%m/%Y")
    return df

# filters the given df by product name
# can handle filter by single or multiple products


def filter_by_product(df, product) -> pd.DataFrame:
    if isinstance(product, str):
        product = [product]
    df = df[df['Product'].isin(product)]
    return df


# filters the given df by brand name
def filter_by_brand(df, brand) -> pd.DataFrame:
    df = df[df.Product == brand]
    return df

# Creates extra features to the raw df


def create_features(df) -> pd.DataFrame:
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
