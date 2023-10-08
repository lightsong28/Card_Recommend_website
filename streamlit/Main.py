# streamlit Main
# 메인 페이지
import streamlit as st
from PIL import Image
from datetime import datetime

st.set_page_config(
        page_title = 'Clovacash',
        page_icon='💲',
        layout='wide'
)

st.title('클로바캐시')

image = Image.open('./data/clovacash.png')
st.image(image)

if 'customer_code' not in st.session_state:
        st.session_state['customer_code'] =''
elif 'customer_password' not in st.session_state:
        st.session_state['customer_password'] = ''

customer_code = st.text_input('User ID', st.session_state['customer_code'])
                
password = st.text_input(label = 'Password', type="password")

btn_clicked = st.button('Log in',use_container_width=5)


if btn_clicked:
        st.session_state['customer_code'] = customer_code
        st.session_state['customer_password'] = password
        st.subheader(customer_code+'님이 로그인 되셨습니다.')







