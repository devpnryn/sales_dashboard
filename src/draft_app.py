import pandas as pd  # pip install pandas openpyxl
import numpy as np  # pip install numpy
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu
import base64


# local python imports
# import image_loader as iml


st.set_page_config(page_title='Retail Forecast',
                   page_icon=':bar_chart:', layout='centered')
st.markdown('## Retail Forecast')

# --- VARIABLES ---
# css_file = './styles/style.css'
# --- UTILITIES ---

#  To set background image


@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


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
# set_png_as_page_bg('assets/Jan-Business_report_1.jpg')
# set_png_as_page_bg('assets/analytics-svgrepo-com.svg')


# --- SIDE BAR ---
st.sidebar.header("Select Products")
uploaded_file = st.sidebar.file_uploader("Choose a File", type='xlsx')


if uploaded_file is None:
    st.write('upload excel file to see the insights')

if uploaded_file:
    df = get_data(uploaded_file)

    # -- store the dataframe in session for the future workflow..
    if 'df_excel' not in st.session_state:
        st.session_state['df_excel'] = df

    #  display dataframe to the screen
    # st.session_state['df_excel']

    # --- Navigation Menu ---
    selected = option_menu(
        menu_title=None,
        options=["Key Insights", "More Analytics"],
        icons=["pencil-fill", "bar-chart-fill"],
        orientation="horizontal")
    # -- store the dataframe in session for the future workflow..
    # if 'current_tab' not in st.session_state:
    #     st.session_state['current_tab'] = selected
    st.session_state['current_tab'] = selected


if uploaded_file:

    # --- UI under Key insights Tab --- #
    if st.session_state['current_tab'] == "Key Insights":
        st.markdown('### insights')
    # --- Three widgets: 1. Total sales 2. Unique Prodcuts 3.YoY Sales Trend --- #

    # creating a single-element container
        widgets = st.empty()
        with widgets.container():

            # create three columns
            kpi1, kpi2, kpi3 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs
            kpi1.metric(
                label="Total Sales ⏳",
                value=25000,
                delta=30,
            )

            kpi2.metric(
                label="Products 🎳",
                value=328,
                delta=-10 + 32,
            )

            kpi3.metric(
                label="Best Year 🎉",
                value=2020,
                delta=49,
            )
            # LINK TO THE CSS FILE
            with open("src/styles/style.css")as f:
                st.markdown(f"<style> {f.read()}</style>",
                            unsafe_allow_html=True)

            st.markdown("<hr/>", unsafe_allow_html=True)

            #  display dataframe to the screen
            st.session_state['df_excel']

            #  --- some trend charts --- #
            # create two columns for charts
            # --- 1. YoY sales growth trend
            # ----2. Fast selling products

    # --- UI under Analytics Tab --- #
    elif st.session_state['current_tab'] == "More Analytics":
        st.markdown('### analytics')
    #  --- Filters with options --- #


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
