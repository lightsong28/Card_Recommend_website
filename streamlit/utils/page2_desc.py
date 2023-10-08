# Streamlit Util 모음
# page2_desc.py 파일
import streamlit as st
import pandas as pd
from PIL import Image


def desc():
    
    data = pd.read_csv('./data/card_data.csv', encoding='cp949')

    # 카드 이름 리스트
    card_names = data['카드이름']
    # 카드 이름 선택 박스 생성
    selected_card = st.selectbox('카드 선택', card_names)
    # 선택한 카드에 해당하는 이미지 파일 열기

        
        
    for card_name in card_names:
            if selected_card == card_name:
                image = Image.open(f'./data/card_Top10/{card_name}.png')
                st.image(image, caption=selected_card)
                        
                st.table(data[data['카드이름']==card_name][['혜택1','혜택2','혜택3']])