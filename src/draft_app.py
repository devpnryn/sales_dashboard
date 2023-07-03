import pandas as pd  # pip install pandas openpyxl
import numpy as np  # pip install numpy
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from streamlit_lottie import st_lottie
from streamlit_extras.app_logo import add_logo
from streamlit_option_menu import option_menu
import plotly.figure_factory as ff
import os
import datetime

import streamlit_authenticator as stauth

import base64
import json
import yaml
from yaml.loader import SafeLoader

# local imports
import dataprocessor
from analytics import Analytics


# setting favicon and browser tab title
st.set_page_config(page_title='Retail Forecast',
                   page_icon=':bar_chart:', layout='centered')


@st.cache_data
def load_logo(file_name):
    with open(file_name, "r") as f:
        data = json.load(f)
        return data


def draw_forecast(data, product_name, start_date, end_date):
    data = data.loc[(data.index > start_date) & (data.index < end_date)]
    # st.write(data)
    fig = px.line(data, y='pred',
                  title=f'{product_name} forecast', labels={"index": 'Monthly', "pred": 'Quantity'})
    st.plotly_chart(fig)


def draw_piechart(data):

    # Group the data by product and calculate the total sales
    sales_data = data.groupby('Product')['Quantity'].sum().reset_index()

    # Create a pie chart using plotly.express
    fig = px.pie(sales_data, values='Quantity',
                 names='Product')

    # Display the chart using Streamlit
    st.plotly_chart(fig)


cwd = os.getcwd()
with open(cwd+'/src/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login('Login', 'main')


if authentication_status == False:
    st.error("Username or Password is Incorrect")
    data = load_logo("/assets/hello.json")
    st_lottie(data)
    # st_lottie(
    #     "https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

if authentication_status == None:
    st.warning("Please enter your username and password")
    st_lottie(
        "https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

if authentication_status:
    # setting up Page Title
    st.markdown('## Retail Forecast')
    with st.sidebar:
        st_lottie(load_logo("assets/hello.json"))
        # st_lottie(
        #     "https://assets5.lottiefiles.com/packages/lf20_V9t630.json")
    # --- VARIABLES ---

    nav_menu = st.container()
    st.session_state["selected_products"] = None
    # --- UTILITIES ---

    #  To set background image

    @st.cache_data
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    # To set the background image for the app.

    def set_png_as_page_bg(png_file):
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = '''
        <style>
        .stApp{
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        }
        </style>
        ''' % bin_str

        st.markdown(page_bg_img, unsafe_allow_html=True)
        return

    #  To read excel file

    @st.cache_data
    def get_data(filepath) -> pd.DataFrame:
        df = pd.read_excel(filepath)
        return df

    # TODO: set the background image without effecting the darkmode

    def draw_scatter_plot(df):
        df = df.copy()
        df['Date'] = pd.to_datetime(df['year'])
        df['Year'] = df['Date'].dt.year
        df['Quarter'] = df['Date'].dt.quarter
        # st.write(df.groupby(['Year', 'Brand', 'Product']).agg(
        #     {'Total Price': 'sum', 'Quantity': 'sum'}))

        # Convert the 'Year' column to datetime and extract year and quarter
        df['Year'] = pd.to_datetime(df['Year'], format='%Y')
        df['Year'] = df['Year'].dt.year

        # Group by Year, Brand, and Product and calculate the sum of Total Price and Quantity
        df_grouped = df.groupby(['Year', 'Brand', 'Product']).agg(
            {'Total Price': 'sum', 'Quantity': 'sum'}).reset_index()

        # Pivot the DataFrame to have 'Year' as columns
        pivot_df = df_grouped.pivot(
            index=['Brand', 'Product'], columns='Year', values='Total Price').reset_index()

        # Melt the pivoted DataFrame to long format
        df_melted = pivot_df.melt(
            id_vars=['Brand', 'Product'], var_name='Year', value_name='Total Price')

        # Plotting the stacked bar chart using Plotly Express
        fig = px.bar(df_melted, x='Year', y='Total Price',
                     color='Brand', barmode='stack')

        # Update the layout
        fig.update_layout(
            title='Total Sales by Brand and Product per Year',
            xaxis_title='Year',
            yaxis_title='Total Price'
        )

        # Display the chart using Streamlit
        st.plotly_chart(fig, use_container_width=True)

    def draw_trend_line_chart(df, product_column, date_column, quantity_column):
        fig = px.line(df, x=df.index.year, y=df[quantity_column].rolling(200).mean(), color=product_column,
                      labels={date_column: 'Sale Date',
                              quantity_column: 'Quantity'},
                      title='Quantity Trend by Product')

        fig.update_xaxes(dtick='M1', tickformat='%b-%y')
        st.plotly_chart(fig, use_container_width=True)

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}!")

    # --- SIDE BAR ---
    # st_lottie(
    #     "https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

    def add_logo(logo_file):
        bin_str = get_base64_of_bin_file(logo_file)
        page_bg_img = '''
        <style>
                [data-testid="stSidebar"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    padding-top: 120px;
                    background-position: 20px 20px;
                }
                [data-testid="stSidebar"]::before {
                    content: "";
                    margin-left: 20px;
                    margin-top: 20px;
                    font-size: 30px;
                    position: relative;
                    top: 100px;
                }
            </style>
        ''' % bin_str

        st.markdown(page_bg_img, unsafe_allow_html=True)
        return
    # add_logo("assets/money-bag.gif")

    uploaded_file = st.sidebar.file_uploader(
        "Choose a File", type='xlsx')

    if uploaded_file is None:
        st.write('upload excel file to see the insights')

    if uploaded_file:
        # df = get_data(uploaded_file)
        df = dataprocessor.get_raw_dataframe(uploaded_file)

        # -- store the dataframe in session for the future workflow..
        if 'df_excel' not in st.session_state:
            st.session_state['df_excel'] = df

        # --- Navigation Menu ---
        with nav_menu:
            selected = option_menu(
                menu_title=None,
                options=["Key Insights", "Forecasting"],
                icons=["pencil-fill", "bar-chart-fill"],
                orientation="horizontal")
            st.session_state['current_tab'] = selected

            # --- UI under Key insights Tab --- #
            if st.session_state['current_tab'] == "Key Insights":
                st.markdown('### Key Metrics')
            # --- Three widgets: 1. Total sales 2. Unique Prodcuts 3.Best Year of Sales  --- #

            # creating a single-element container
                # create three columns
                kpi1, kpi2, kpi3 = st.columns(3)

                # fill in those three columns with respective KPIs
                # KPI-1: Total sales so far
                total = df['Quantity'].sum()
                kpi1.metric(
                    label="Total Sales ⏳",
                    value=total,
                    delta=300,
                )

                # KPI-2: No.of unique products sold
                products = df['Product'].unique()
                if 'unique_products' not in st.session_state:
                    st.session_state['unique_products'] = products
                kpi2.metric(
                    label="Products 🎳",
                    value=products.size,
                    delta=-10 + products.size,
                )

                # KPI-3: Best year so far in terms of sales
                grouped_df = df.groupby(df.index.year)['Quantity'].sum()
                kpi3.metric(
                    label="Best Year 🎉",
                    value=grouped_df.idxmax(),
                    delta='49%',
                )

                # styling the kpis
                with open("src/styles/style.css")as f:
                    st.markdown(f"<style> {f.read()}</style>",
                                unsafe_allow_html=True)

                st.markdown("<hr/>", unsafe_allow_html=True)

                # Selection box with product names, by default shows two products
                st.subheader("Sales Trends of the products")
                if st.session_state["selected_products"] is None:
                    options = st.multiselect(
                        label='', options=products, default=products[:2])

                    st.session_state["selected_products"] = options

                df = dataprocessor.filter_by_product(
                    df, st.session_state["selected_products"])

                # creating new feature(Year) on dataframe
                df['year'] = pd.to_datetime(df.index, format="%Y")

                # create two tabs for charts

                tab1, tab2 = st.tabs(
                    ["Sales volume by Price", "Sales by Products"])
                st.session_state["insights_df"] = df

                # --- Tab 1. Scatter plot to show the distribution
                with tab1:
                    # TODO: this has to draw scatter plot of different product sales in every year
                    if st.session_state["insights_df"] is None:
                        draw_scatter_plot(df)
                    else:
                        draw_scatter_plot(
                            st.session_state["insights_df"])

                # --- Tab 2. Trend line to show the YoY growth
                with tab2:
                    # TODO: this has to be rolling mean of each selected product with different color on same plot
                    if st.session_state["insights_df"] is None:
                        draw_trend_line_chart(
                            df, 'Product', 'Sale Date', 'Quantity')
                    else:
                        draw_trend_line_chart(
                            st.session_state["insights_df"], 'Product', 'Sale Date', 'Quantity')

                # ----2. Fast selling products

                st.subheader('Product-wise Sales')
                draw_piechart(st.session_state['df_excel'])

            # --- UI under Analytics Tab --- #
            # predictions shown here
            elif st.session_state['current_tab'] == "Forecasting":
                st.markdown('### Get Forecast')

                product, date = st.columns(2)
                with product:
                    chosen_product = st.selectbox('Select Prodcut',
                                                  options=st.session_state['unique_products'])
                with date:
                    start_date = st.date_input(
                        'select start date', min_value=datetime.date(2023, 7, 3), max_value=datetime.date(2023, 12, 30), value=datetime.date(2023, 7, 4)).strftime("%Y-%m-%d")

                predictions = Analytics.predict_data(
                    st.session_state['df_excel'], chosen_product, start_date, '2023-12-30')
                st.write(predictions)

                if 'predictions' not in st.session_state:
                    st.session_state['predictions'] = predictions
                # st.write('chosen product', chosen_product)
                draw_forecast(
                    data=st.session_state['predictions'], product_name=chosen_product, start_date=start_date, end_date='2023-12-30')

    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    # st.markdown(hide_st_style, unsafe_allow_html=True)
