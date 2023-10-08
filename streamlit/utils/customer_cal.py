import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta
import plotly.express as px
import altair as alt


customer_df = pd.read_csv('./data/customer_df1.csv',encoding='utf8')
customer_df = customer_df.drop('Unnamed: 0',axis=1)
customer_df['date'] = customer_df['date'].map(lambda x:datetime.strptime(x,'%Y-%m-%d'))

def get_month_(x):
    return x.month

def get_year_(x):
    return x.year

def get_customer_data(customer_code,customer_df):
    one_df = customer_df[customer_df['customer']==customer_code]
    one_df['month'] = one_df['date'].map(get_month_)
    one_df['year'] = one_df['date'].map(get_year_)
    one_df = one_df.sort_values(by='date')
    return one_df

def year_category(one_df):
    one_df_sum = one_df.groupby('category')['amount'].sum()
    year_category_df = pd.DataFrame(one_df_sum)
    return year_category_df

def last_month_category(one_df,now_month):
    last_month = now_month-1
    one_df_sum = one_df[one_df['month']==last_month].groupby('category')['amount'].sum()
    last_month_df = pd.DataFrame(one_df_sum)
    return last_month_df

def get_top3(df, index):
    top3_list = list(df[index].sort_values(ascending=False)[:3].index)
    return top3_list

def draw_yearpie(one_df):
    one_category_amount_sum = one_df.groupby('category')['amount'].sum()
    one_category_amount_sum_df = pd.DataFrame(one_category_amount_sum)

    data = one_category_amount_sum
    labels = one_category_amount_sum_df.index

    #define Seaborn color palette to use
    colors = sns.color_palette('pastel')[0:14]

    #create pie chart
    plt.pie(data, labels = labels, colors = colors, autopct='%.0f%%')
    st.pyplot(plt)

def draw_yearbar(one_df):
    st.bar_chart(one_df)

def draw_monthbar(last_month_df):
    st.bar_chart(last_month_df)

def draw_monthpie(last_month_df):
    last_month_category_amount_sum = last_month_df.groupby('category')['amount'].sum()
    last_month_category_amount_sum_df = pd.DataFrame(last_month_category_amount_sum)
    data = last_month_category_amount_sum
    labels = last_month_category_amount_sum_df.index

    #define Seaborn color palette to use
    colors = sns.color_palette('pastel')[0:14]

    #create pie chart
    plt.pie(data, labels = labels, colors = colors, autopct='%.0f%%')
    st.pyplot(plt)

def get_amount_percent(df):
    wi_list = []
    num = len(df)
    for i in range(1,num+1):
        wi_list.append(f'{i}위')
    amount_percent_df = df.copy()
    amount_percent_df = amount_percent_df.sort_values('amount',ascending=False)
    amount_percent_df['amount'] = amount_percent_df['amount'].map(lambda x:round(x,-1)).astype(int)
    total = amount_percent_df['amount'].sum()
    amount_percent_df['percent'] = amount_percent_df['amount'].map(lambda x:round((x/total)*100,2))
    amount_percent_df['순위'] = wi_list
    change_df = amount_percent_df.reset_index().set_index(keys='순위',drop=True)
    change_df['amount'] = change_df['amount'].astype(int)
    change_df['amount'] = change_df['amount'].map(lambda x:format(x,','))
    change_df.columns = ['카테고리','사용금액(원)','사용비중(%)']
    return change_df

def gender_percent(df):
    customer_list = df['customer'].unique()
    gender_list = []
    gender_count_list = []
    for i in customer_list:
        for j in range(len(df)):
            if df.loc[j,'customer'] == i:
                gender_list.append(df.loc[j,'gender'])
                break
    for i in ['M','F']:
        gender_count_list.append(gender_list.count(i))
    gender_df = pd.DataFrame({'성별':['남성','여성'],'고객수(명)':gender_count_list})
    gender_df = gender_df.set_index('성별')
    total = gender_df['고객수(명)'].sum()
    gender_df['비율(%)'] = gender_df['고객수(명)'].map(lambda x:(x/total)*100)
    return gender_df

def age_percent(df):
    customer_list = df['customer'].unique()
    age_list = []
    age_count_list = []
    for i in customer_list:
        for j in range(len(df)):
            if df.loc[j,'customer']==i:
                age_list.append(df.loc[j,'age'])
                break
    age_category = [10,20,30,40,50,60,70]
    for i in age_category:
        age_count_list.append(age_list.count(i))
    age_df = pd.DataFrame({'연령대':['10대','20대','30대','40대','50대','60대','70대'], '고객수(명)':age_count_list})
    age_df = age_df.set_index('연령대')
    total = age_df['고객수(명)'].sum()
    age_df['비율(%)'] = round(age_df['고객수(명)'].map(lambda x:(x/total)*100).astype(float),2)
    return age_df

def age_gender_df(df):
    customer_list = df['customer'].unique()
    customer_info_dict = {}
    for i in customer_list:
        for j in range(len(df)):
            customer_info_list = []
            if df.loc[j,'customer'] == i:
                customer_info_list.append(df.loc[j,['gender','age']])
                break
        customer_info_dict[i] = customer_info_list
    return customer_info_dict


def get_multigraph(df):
    # get_customer_df 함수를 거친, 즉 month, year 열을 가지는 dataframe이 필요
    date_list = df['date'].unique()
    start_date, end_date = st.select_slider(label='날짜 범위를 선택해 주세요',options=date_list,value=(min(date_list),max(date_list)))
    date_df = df[start_date<=df['date']<=end_date]
    category_data = date_df.groupby('category')['amount'].sum()
    category_data_df = pd.DataFrame(category_data)
    return category_data_df

def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
    return dates

def tab3_graph(one_df):
    one_df['date'] = one_df['date'].map(lambda x:datetime.date(x))
    date_list = one_df['date'].unique()
    start_date = min(date_list)
    end_date = max(date_list)
    start_date2, end_date2 = st.select_slider(label='날짜 범위를 선택해 주세요',options=date_list,value=(start_date,end_date))
    date_df = one_df[(one_df['date']>=start_date2)&(one_df['date']<=end_date2)]
    category_data = date_df.groupby('category')['amount'].sum()
    between_df = pd.DataFrame(category_data)
    table_df = between_df.copy()
    table_df = table_df.sort_values('amount',ascending=False)
    table_df['amount'] = table_df['amount'].map(lambda x:format(x,','))
    table_df.columns = ['사용금액(원)']
    fig3 = px.pie(between_df, values='amount', names=between_df.index)
    col1, col2 = st.columns([3, 2])
    col1.subheader(str(start_date2)+'~'+str(end_date2)+"사이의 사용 통계")
    col1.plotly_chart(fig3)

    col2.subheader('사용 통계 데이터')
    col2.table(table_df)

def tab3_monthgraph(one_df):
    tab3_df = one_df.copy()
    tab3_df['date'] = pd.to_datetime(tab3_df['date'])
    tab3_df['year_month'] = tab3_df['date'].dt.strftime('%Y.%m')
    drawbar = tab3_df.groupby('year_month').sum()
    drawbar = drawbar.sort_values('year_month')
    st.bar_chart(drawbar['amount'])