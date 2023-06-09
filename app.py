import pandas as pd  # pip install pandas openpyxl
import numpy as np  # pip install numpy
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu

st.set_page_config(page_title='SALES FORECAST',
                   page_icon=':bar_chart:', layout='centered')
st.markdown('## Sales Forecast')

# --- SIDE BAR ---
st.sidebar.header("Select Products")
uploaded_file = st.sidebar.file_uploader("Choose a File", type='xlsx')

# --- Navigation Menu ---
selected = option_menu(
    menu_title=None,
    options=["Data Details", "Analytics"],
    icons=["pencil-fill", "bar-chart-fill"],
    orientation="horizontal")

df_selection = None


def read_file(file):
    df = pd.DataFrame()
    if file is not None:
        df = pd.read_excel(file)
        st.markdown('### Uploaded file contents')
        st.write(f'{file.name} is uploaded!')
        st.dataframe(df)
    else:
        st.warning("you need to upload excel file.")
    return df


df = read_file(uploaded_file)
# --- new approach ---
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    selected_product = st.selectbox('Which product category are you interested in?',
                                    options=df["productName"].unique()
                                    )
    output_columns = ['quantity']
    if selected_product is not None:
        df_query = df.query("productName== @selected_product")
        product_quantity = df_query[output_columns].sum(numeric_only=True)
        st.dataframe(product_quantity)

    #  Sales trendline of the product
    product_df = df[df['productName'] == selected_product]
    rolling_mean = product_df['quantity'].rolling(window=7).mean()
    fig = px.line(product_df,
                  x='transactionDate',
                  y=rolling_mean,
                  labels={'transactionDate': 'Transaction Date',
                          'rolling_mean': 'Quantity'},
                  title=f'{selected_product} Sales Trend')
    fig.update_xaxes(dtick='M1', tickformat='%b-%y')
    st.plotly_chart(fig, use_container_width=True)

if not df.empty:
    madeby_ = st.sidebar.multiselect(
        "Select Manufacturer:",
        options=df["manufacturer"].unique(),
        default=df["manufacturer"].unique()[0]
    )

    prod_ = st.sidebar.multiselect(
        "Select Component:",
        options=df.query("manufacturer==@madeby_")["productName"].unique(),
        default=df.query("manufacturer==@madeby_")["productName"].unique()
    )
    if 'read_data' not in st.session_state:
        st.session_state["read_data"] = df.query(
            "productName==@prod_ & manufacturer== @madeby_")

if 'read_data' not in st.session_state:
    st.write('upload excel to see it here!')
elif 'read_data' in st.session_state:
    df_selection = st.session_state['read_data']

if selected == "Data Details":
    st.markdown('### Selected fields')
    if df_selection is not None:
        df_selection.index = np.arange(1, len(df_selection) + 1)
        st.dataframe(df_selection)
elif selected == "Analytics":
    # sales by category
    if df_selection is not None:
        sales_by_product_type = (
            df_selection.groupby("productName").sum(
                numeric_only=True)[["quantity"]]
        )
        fig_product_sales = px.bar(
            sales_by_product_type,
            x="quantity",
            y=sales_by_product_type.index,
            title="<b> Sales by Product</b>",
            color_discrete_sequence=["#008388"] * len(sales_by_product_type),
            template="plotly_white"
        )
        st.plotly_chart(fig_product_sales)
        #         sales trendline of the product

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)
