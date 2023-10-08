# 카드 추천 시스템
# 3개의 카드를 1 : 1년간 사용한 카테고리중 top1의 카테고리의 할인율,적립률이 가장 큰 카드 추천
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random
from utils import card_cal as cac
from utils import customer_cal as cuc
from datetime import datetime
from PIL import Image
import re



card_df = pd.read_csv('./data/card_data100.csv',encoding='cp949')

card_companies = ['신한카드','삼성카드', 'KB국민카드','롯데카드','하나카드','우리카드',
									'NH농협카드','IBK기업은행','현대카드','BC카드']

def desc(customer_code, today_month):
    
    card_df = pd.read_csv('./data/card_data100.csv',encoding='cp949')
    card_benefit_df = cac.card_benefit(card_df)
    card_labeling_df = cac.card_labeling(card_benefit_df)

    
    customer_df = pd.read_csv('./data/customer_df1.csv',encoding='utf8')
    customer_df = customer_df.drop('Unnamed: 0',axis=1)
    customer_df['date'] = customer_df['date'].map(lambda x:datetime.strptime(x,'%Y-%m-%d'))

    one_df = cuc.get_customer_data(customer_code,customer_df)
    last_month = today_month-1
    last_month_df = one_df[one_df['month']==last_month]
    year_category_df = cuc.year_category(one_df)
    data = cuc.last_month_category(one_df,today_month)
    data2 = cuc.get_amount_percent(data)

    top_category = data2['카테고리'][0]
    (category_top_card_df,card_recommend_df) = cac.card_recommend(card_labeling_df, last_month_df,top_category)

    for i in category_top_card_df.index:
        card_name = card_labeling_df.loc[i,'카드이름']
        card_company = card_labeling_df.loc[i,'카드회사']
        card_benefit = format(round(card_recommend_df.loc[i,top_category],-1),',')
        benefit_type = card_recommend_df.loc[i,'비고']
        col1, col2 = st.columns([1, 1], gap='small')
        
        col1.subheader(card_name)
        col1.write(card_company)
        
        image = Image.open(f'./data/card_Top10/{card_name}.png')
        col1.image(image, caption=card_name)
        
        col2.write('이 카드는 고객님의 소비 패턴 중')
        col2.write(f'**{top_category}**에서 기존 카드보다')
        if benefit_type == 0:
            col2.subheader(f'{card_benefit}원 만큼 적립이 됩니다!')
        else:
            col2.subheader(f'{card_benefit}원 만큼 할인이 됩니다!')
        card_transpose = np.transpose(card_df[card_df['카드이름']==card_name][['혜택1','혜택2','혜택3']])
        card_transpose.columns = [card_name]
        col2.table(card_transpose)

        
        st.write('\n')
        st.write('***')


        