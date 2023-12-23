
# run :-   streamlit run 3.\ project.py


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Startup Analysis')

df=pd.read_csv('cleaned_data.csv')





def load_overall_analysis():
    # total invested amount
    total = df['amount'].sum()
    # max amount invested in a company
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    #  average money invested in the starups
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    #  total no of startups that have been funded
    num_startup = df['startup'].nunique()


    col1,col2,col3,col4 = st.columns(4)
    with col1:
            st.metric("total money invested by all the startups",str(total)+' USD')
    with col2:
            st.metric("Max funding in a startup",str(max_funding)+' USD')
    with col3:
            st.metric("Average investment",str(round(avg_funding))+' USD')
    with col4:
         st.metric("Total no of funded startups",num_startup)
         

    st.header("Month on Month Graph") 
    selected_option = st.selectbox("Select Type",['Total Amount Invested','Total no of Startups Funded'])

    if selected_option == 'Total Amount Invested':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)

        fig3,ax3 = plt.subplots()
        ax3.plot(temp_df['x_axis'],temp_df['amount'])
        st.pyplot(fig3)

    else:
        temp_df = df.groupby(['year','month'])['startup'].count().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)

        fig4,ax4 = plt.subplots()
        ax4.plot(temp_df['x_axis'],temp_df['startup'])
        st.pyplot(fig4)
        





def load_investor_details(investor):
    st.title(investor)

    # load the recent 5 investment of the investor
    last5_df = df[df['investors'].str.contains(investor)][['date','startup','vertical','city','round','amount']].head()
    st.subheader("Recent 5 investment")
    st.dataframe(last5_df)

    # biggest investment
    big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
    st.subheader("Biggest investment")
    st.dataframe(big_series)

    col1,col2 = st.columns(2)

    with col1:    
        st.subheader("Biggest investment plot")
        fig,ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader("Sectors Invested")
        fig1,ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct='%0.01f')
        st.pyplot(fig1)


    # df['year']=df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader("Year on Year Investment")
    fig2,ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)
    st.pyplot(fig2)






st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    st.title('Overall Analysis')
    load_overall_analysis()
    # btn0 = st.sidebar.button('Show Overall Analysis')
    # if btn0:
    #     load_overall_analysis()


elif option == 'Startup':
    st.title('Startup Analysis')
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')

else:
    st.title('Investor Analysis')
    selected_investor = st.sidebar.selectbox('Select Investors',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)


























































