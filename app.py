import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Sales Dashboard",page_icon=":bar_chart:",layout="wide")

def get_DataFrom_Excel():
    df = pd.read_excel(io='supermarkt_sales.xlsx',engine='openpyxl',sheet_name= 'Sales', skiprows=3,usecols= 'B:R',nrows=1000)
    #print(df)

    ## ADD "hour" column to this dataframe
    df["hour"] = pd.to_datetime(df["Time"],format ="%H:%M:%S").dt.hour
    return df
df = get_DataFrom_Excel()

#st.dataframe(df)


############ SIDEBAR##########
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)


customer_type = st.sidebar.multiselect(
    "Select the Customer_type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

#### To filter dataframe use quary
df_select = df.query(
    "City==@city & Customer_type==@customer_type & Gender==@gender"
)



##st.dataframe(df)


##########   MAINPAGE  ##########  
st.title(":chart_with_upwards_trend: Shales DashBoard")
st.markdown("##")

### Top KPI's   ###
total_sales = int(df_select["Total"].sum())
average_rating = round(df_select["Rating"].mean(), 1)
star_rating = "star:" * int(round(average_rating , 0))
average_sale_by_transaction = round(df_select["Total"].mean(),2)


left_column, middle_column, right_column = st.columns(3)
with left_column :
    st.subheader("Tolal Sales :")
    st.subheader(f"INR \u20B9  {total_sales:,}")
with middle_column :
    st.subheader("Average Rating :")
    st.subheader(f"{average_rating} {star_rating}")
with right_column :
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"INR \u20B9  {average_sale_by_transaction}")

st.markdown("---")

# SALES BY PRODUCT LINE [BAR CHQART]
desired = df_select.select_dtypes(['int16', 'int32', 'int64', 'float16', 'float32', 'float64']).columns
sales_by_product_line = df_select.groupby(by=["Product line"])[desired].sum()[["Total"]].sort_values(by="Total")

fig_product_sales =px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<i><b>SALES BY PRODUCT LINE</b></i>",
    color_discrete_sequence=["#900FEE"] * len(sales_by_product_line),
    template="plotly_dark",
)
fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid = False))
)
###st.plotly_chart(fig_product_sales)



# sales by hours[BAR CHART]
desired_d = df_select.select_dtypes(['int16', 'int32', 'int64', 'float16', 'float32', 'float64']).columns
sales_by_hour = df_select.groupby(by=["hour"])[desired_d].sum()[["Total"]]
fig_hourly_sales =px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    orientation="v",
    title="<i><b>SALES BY HOUR</b></i>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = dict(tickmode = "linear"),
    yaxis = (dict(showgrid = False)),
)
###st.plotly_chart(fig_hourly_sales)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width= True)
right_column.plotly_chart(fig_product_sales, use_container_width= True)






# Uncomment to display the filtered dataframe
#st.dataframe(df_select)
