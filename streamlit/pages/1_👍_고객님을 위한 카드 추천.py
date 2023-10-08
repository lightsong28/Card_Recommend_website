# 카드 추천
import streamlit as st
from datetime import datetime
from utils import page5_desc as p5d

today_month = datetime.now().month
customer_code = st.session_state['customer_code']

if customer_code:
    st.subheader('추천 카드')
    st.write('\n')
    st.subheader('고객님의 최근 3개월 소비 패턴을 바탕으로')
    st.subheader('앞으로 쓰기 적절한 카드입니다.')
    st.write('\n')
    p5d.desc(customer_code,today_month)
else:
    st.subheader('로그인 해주세요!')
