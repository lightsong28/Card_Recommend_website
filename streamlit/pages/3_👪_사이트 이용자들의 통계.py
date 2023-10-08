# 전체 카드 사용 통계
import streamlit as st
from datetime import datetime
from utils import page3_desc as p3d

today_month = datetime.now().month

customer_code = st.session_state['customer_code']

if customer_code:
    st.subheader('클로바캐시에 저장된 고객들의 통계입니다.')
    customer_num = p3d.storage_info()
    st.subheader(f'총 {customer_num}명이 이용하고 있어요!')
    p3d.desc(customer_code,today_month)
else:
    customer_num = p3d.storage_info()
    st.subheader(f'사이트 이용자는 총 {customer_num}명 입니다.')
    st.subheader('더 자세한 정보를 볼려면 로그인 해주세요!')