# Streamlit Util 모음
# page3_desc.py 파일
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils import card_cal as cac
from utils import customer_cal as cuc
from datetime import datetime
import plotly.express as px

def desc(customer_code,today_month):
    
    customer_df = pd.read_csv('./data/customer_df1.csv',encoding='utf8')
    customer_df = customer_df.drop('Unnamed: 0',axis=1)
    customer_df['date'] = customer_df['date'].map(lambda x:datetime.strptime(x,'%Y-%m-%d'))
    
    all_df = customer_df.copy()
    all_df['month'] = all_df['date'].map(get_month_)
    all_df['year'] = all_df['date'].map(get_year_)
    all_df = all_df.sort_values(by='date')

    last_month_df = cuc.last_month_category(all_df,today_month)
    
    tab1, tab2, tab3 = st.tabs(["저장된 고객 통계","1년간 사용한 카테고리", "지난달 사용 금액"])

    with tab1:
        st.subheader('클로바 캐시에 저장된 고객들의 통계입니다.')

        col1, col2 = st.columns([3, 2])
        data = cuc.gender_percent(all_df)
        data2 = data['고객수(명)']
        fig1 = px.pie(data2,values='고객수(명)',names=data2.index)

        col1.subheader('성별 사용 통계')
        col1.plotly_chart(fig1)

        col2.subheader('성별 사용 통계 데이터')
        col2.table(data)

        col1, col2 = st.columns([3, 2])
        data = cuc.age_percent(all_df)
        data2 = data['고객수(명)']
        fig2 = px.pie(data2,values='고객수(명)',names=data2.index)

        col1.subheader('연령 분포 통계')
        col1.plotly_chart(fig2)

        col2.subheader('연령 분포 통계 데이터')
        col2.table(data)


    with tab2:
        st.subheader('1년간 총 사용한 카테고리: ('+str(all_df['date'].min().date())+' ~ '+str(all_df['date'].max().date())+')')
        year_category_df = cuc.year_category(all_df)

        col1, col2 = st.columns([3, 2])
        data = year_category_df
        data2 = cuc.get_amount_percent(data)
        fig3 = px.pie(year_category_df, values='amount', names=year_category_df.index)

        col1.subheader("사용 통계")
        col1.plotly_chart(fig3)

        col2.subheader("사용 통계 데이터")
        col2.write(data2)
        
        st.subheader('가장 많이 사용한 3가지 카테고리는 다음과 같습니다.')
        st.table(data2[:3])

    with tab3:
        st.subheader('지난달 사용한 카테고리: '+str(today_month-1)+'월')

        col1, col2 = st.columns([3, 2])
        data = last_month_df
        data2 = cuc.get_amount_percent(data)
        fig4 = px.pie(data, values='amount', names=data.index)

        col1.subheader("사용 통계")
        col1.plotly_chart(fig4)

        col2.subheader("사용 통계 데이터")
        col2.write(data2)

        st.subheader('지난달 많이 사용한 카테고리는 다음과 같습니다.')
        st.table(data2[:3])
    

def get_cardname(customer_code):
    
    customer_df = pd.read_csv('./data/customer_df1.csv',encoding='utf8')
    customer_df = customer_df.drop('Unnamed: 0',axis=1)
    customer_df['date'] = customer_df['date'].map(lambda x:datetime.strptime(x,'%Y-%m-%d'))

    all_df = cuc.get_customer_data(customer_code,customer_df)
    all_df = customer_df[customer_df['customer']==customer_code]
    using_card = all_df['card_name'].unique()
    return using_card

def storage_info():
    
    customer_df = pd.read_csv('./data/customer_df1.csv',encoding='utf8')
    customer_df = customer_df.drop('Unnamed: 0',axis=1)
    customer_df['date'] = customer_df['date'].map(lambda x:datetime.strptime(x,'%Y-%m-%d'))

    all_df = customer_df.copy()
    customer_num = len(all_df['customer'].unique())
    return customer_num

def get_month_(x):
    return x.month

def get_year_(x):
    return x.year