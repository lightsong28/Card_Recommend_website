import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(layout="wide")

def desc():
        
        data = pd.read_csv('./data/card_data.csv', encoding='cp949')
        

        # 카드 이름 리스트
        card_names = data['카드이름']
        options = st.multiselect('카드 3개를 골라주세요',card_names,['신한카드 Mr.Life'])

        if len(options)<3:
                st.write('3개를 선택해 주세요')
        elif len(options)>3:
                st.write('3개를 초과해서 선택하셨습니다.')
        else:
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                with col1:
                        image = Image.open(f'./data/card_Top10/{options[0]}.png')
                        st.image(image,caption=options[0])
                with col2:
                        st.table(data[data['카드이름']==options[0]][['카드이름','연회비','전월실적','혜택1','혜택2','혜택3']].transpose())
                with col3:
                        image = Image.open(f'./data/card_Top10/{options[1]}.png')
                        st.image(image,caption=options[1])
                with col4:
                        st.table(data[data['카드이름']==options[1]][['카드이름','연회비','전월실적','혜택1','혜택2','혜택3']].transpose())
                with col5:
                        image = Image.open(f'./data/card_Top10/{options[2]}.png')
                        st.image(image,caption=options[2])
                with col6:
                        st.table(data[data['카드이름']==options[2]][['카드이름','연회비','전월실적','혜택1','혜택2','혜택3']].transpose())