import streamlit as st
import pandas as pd

pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.max_colwidth',None)

df = pd.read_csv('startup_funding.csv1')
df['date']= pd.to_datetime(df['date'],errors= 'coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

st.title('Startup Dasboard')
def load_invertor_detail(investor):
    st.title(investor)
    #load recent 5 investment of the investor
    last5_df = df[df['investors name'].str.contains(investor)][
        ['date', 'startup', 'vertical', 'city', 'type', 'amount']].head()
    st.subheader('Most Recent Investmens')
    st.dataframe(last5_df)
    # biggest_investmens
    bigg_ser = df[df['investors name'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
        ascending=False)
    st.subheader('Biggest Investments')
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(bigg_ser.head())
        st.bar_chart(bigg_ser)
    with col2:
        bigg_data = df[df['investors name'].str.contains(investor)].groupby('vertical')['amount'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(bigg_data, labels=bigg_data.index, autopct='%1.1f%%')
        ax1.axis('equal')

        st.pyplot(fig1)
    col3, col4 = st.columns(2)
    with col3:
        bigg_data_1 = df[df['investors name'].str.contains(investor)].groupby('type')['amount'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(bigg_data_1, labels=bigg_data_1.index, autopct='%1.1f%%')
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)
    with col4:
        bigg_data_2 = df[df['investors name'].str.contains(investor)].groupby('city')['amount'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(bigg_data_2, labels=bigg_data_2.index, autopct='%1.1f%%')
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig1)
    df['year'] = df['date'].dt.year
    year_sr = df[df['investors name'].str.contains(investor)].groupby('year')['amount'].sum()
    st.dataframe(year_sr)
    fig1, ax1 = plt.subplots()
    ax1.plot(year_sr.index,year_sr.values)
    st.pyplot(fig1)

def load_overall_analysis():
    st.title("Over_All_Analysis")
    total = round(df['amount'].sum())
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    ave = round(df.groupby('startup')['amount'].sum().mean())
    tot_funded_startup = df['startup'].nunique()
    col1, col2 , col3, col4 = st.columns(4)
    with col1:
        st.metric('Total amount', str(total) + 'cr')
    with col2:
        st.metric('max_funding',str(max_funding) + 'cr')
    with col3:
        st.metric('Avg',str(ave) + 'cr')
    with col4:
        st.metric('Total Funded Startup',str(tot_funded_startup) + 'cr')
    col5, col6 = st.columns(2)
    with col5:
        st.header('Month wise Analysis')
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        temp_df[['amount', 'x_axis']]
    with col6:
        st.header('Year wise Analysis')
        temp_df = df.groupby('year')['amount'].sum().reset_index()
        st.dataframe(temp_df)
        fig1, ax1 = plt.subplots()
        ax1.plot(temp_df['year'], temp_df['amount'])
        st.pyplot(fig1)
    col7, col8 = st.columns(2)
    with col7:
        # sectro Analysis table
        st.header("Sectro Analysis table")
        temp_df1 = df.groupby('vertical')['amount'].sum().reset_index().sort_values(by = 'amount',ascending = False).reset_index()
        st.dataframe(temp_df1)
    with col8:
        #City wise funding
        st.header("City wise Funding")
        temp_df2 = df.groupby('city')['amount'].sum().reset_index().sort_values(by='amount', ascending=False).reset_index()
        st.dataframe(temp_df2)

    st.header("Type wise Funding")
    temp_df2 = df.groupby('type')['amount'].sum().reset_index().sort_values(by='amount', ascending=False)
    temp_df2 = temp_df2.set_index('type')
    st.dataframe(temp_df2)

    col9 , col10 = st.columns(2)
    with col9:
        st.header("Year wise top startup")
        temp_df3 = df.groupby(['year', 'startup'])['amount'].sum().reset_index().sort_values(by='year',
                                                                                             ascending=False)
        temp_df3 = temp_df3.set_index('year')
        st.dataframe(temp_df3)
    with col10:
        st.header("Overall top startup")
        temp_df4 = df.groupby('startup')['amount'].sum().reset_index().sort_values(by='amount', ascending=False)
        temp_df4 = temp_df4.set_index('startup')
        st.dataframe(temp_df4)
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select one', ['Overall Analysis', 'Startup', 'Investor'])
if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'Startup':
    st.sidebar.selectbox('Select Startup', set(df['startup'].str.split(',').sum()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Investor', set(df['investors name'].str.split(',').sum()))
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_invertor_detail(selected_investor)
