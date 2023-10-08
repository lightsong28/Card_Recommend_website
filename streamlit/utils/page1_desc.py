# Streamlit Util 모음
# page1_desc.py 파일
import streamlit as st
import pandas as pd
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

    one_df = cuc.get_customer_data(customer_code,customer_df)
    last_month_df = cuc.last_month_category(one_df,today_month)
    
    tab1, tab2, tab3 = st.tabs(["1년간 사용한 카테고리", "지난달 사용 금액", "나만의 통계표"])

    
    with tab1:
        st.subheader('1년간 총 사용한 카테고리: ('+str(one_df['date'].min().date())+' ~ '+str(one_df['date'].max().date())+')')
        year_category_df = cuc.year_category(one_df)

        fig1 = px.pie(year_category_df, values='amount', names=year_category_df.index)

        col1, col2 = st.columns([3, 2])
        data = year_category_df
        data2 = cuc.get_amount_percent(data)
        

        col1.subheader("사용 통계")
        col1.plotly_chart(fig1)

        col2.subheader("사용 통계 데이터")
        col2.write(data2)
        
        st.subheader('가장 많이 사용한 3가지 카테고리는 다음과 같습니다.')
        st.table(data2[:3])

    with tab2:
        st.subheader('지난달 사용한 카테고리: '+str(today_month-1)+'월')
        
        fig2 = px.pie(last_month_df, values='amount', names=last_month_df.index)
        col1, col2 = st.columns([3, 2])
        data = last_month_df
        data2 = cuc.get_amount_percent(data)

        col1.subheader("사용 통계")
        col1.plotly_chart(fig2)

        col2.subheader("사용 통계 데이터")
        col2.write(data2)

        st.subheader('지난달 많이 사용한 카테고리는 다음과 같습니다.')
        st.table(data2[:3])

        total = last_month_df['amount'].sum()
        total = format(round(total,-1),',')
        st.write('\n')
        st.subheader(f'지난달 총 사용 금액은 : {total}원 입니다.')

    with tab3:
        cuc.tab3_graph(one_df)
        st.subheader('월별 카드 총 사용량(원)')
        cuc.tab3_monthgraph(one_df)



def get_cardname(customer_code):
    
    customer_df = pd.read_csv('./data/customer_df1.csv',encoding='utf8')
    customer_df = customer_df.drop('Unnamed: 0',axis=1)
    customer_df['date'] = customer_df['date'].map(lambda x:datetime.strptime(x,'%Y-%m-%d'))

    one_df = cuc.get_customer_data(customer_code,customer_df)
    one_df = customer_df[customer_df['customer']==customer_code]
    using_card = one_df['card_name'].unique()
    return using_card


