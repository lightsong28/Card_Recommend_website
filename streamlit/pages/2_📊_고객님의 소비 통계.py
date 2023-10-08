# 특정인 카드 사용 통계
import streamlit as st
from datetime import datetime
from utils import page1_desc as p1d

today_month = datetime.now().month
customer_code = st.session_state['customer_code']

if customer_code:
    st.subheader('현재 사용하시는 카드는 다음과 같습니다.')
    card_using = p1d.get_cardname(customer_code)
    st.subheader(card_using[0])
    #for i in range(len(card_using)):
    #   st.subheader(f'{i+1}: '+card_using[i])

    p1d.desc(customer_code,today_month)
else:
    st.subheader('로그인 해주세요!')