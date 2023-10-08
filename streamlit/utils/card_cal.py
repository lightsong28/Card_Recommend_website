import pandas as pd
import numpy as np
import re



card_df = pd.read_csv('./data/card_data100.csv',encoding='cp949')

card_companies = ['신한카드','삼성카드', 'KB국민카드','롯데카드','하나카드','우리카드',
									'NH농협카드','IBK기업은행','현대카드','BC카드']

def card_benefit(card_df):
    card_df1 = card_df.drop(['카드혜택','혜택1','혜택2','혜택3'],axis=1)
    card_benefit_df = card_df1.fillna(0)
    return card_benefit_df

def card_labeling(card_df):
    card_benefit_df = card_df.copy()
    for i in range(len(card_benefit_df)):
       fee = card_benefit_df.loc[i,'연회비']
       regex = re.compile('\d*,\d*')
       annual_fee = regex.findall(fee)
       card_benefit_df.loc[i,'연회비'] = annual_fee[-1].replace(',','')
       previous_m = card_benefit_df.loc[i,'전월실적']
       
       if '없음' in previous_m:
          card_benefit_df.loc[i,'전월실적'] = 0
       else:
          regex = re.compile(r'\d\d')
          matchobj = regex.search(previous_m)
          previous_month = matchobj.group()
          card_benefit_df.loc[i,'전월실적'] = previous_month
    
    for i in range(len(card_benefit_df)):
       if card_benefit_df.loc[i,'비고'] == '할인':
          card_benefit_df.loc[i,'비고'] = 1
       else:
          card_benefit_df.loc[i,'비고'] = 0

    card_benefit_df[['연회비','전월실적','비고']] = card_benefit_df[['연회비','전월실적','비고']].astype(int)
    return card_benefit_df

def card_recommend(card_df,last_month_customer,top_category):
   card_recommend_df = card_df.copy()
   benefit_dict = {}

   total = last_month_customer[last_month_customer['category']==top_category]['amount'].sum()
   benefit_dict[top_category] = total

   card_recommend_df[top_category] = card_recommend_df[top_category].map(lambda x:round(x*benefit_dict[top_category]))
   category_top_card_df = card_recommend_df[top_category].sort_values(ascending=False)[:3]
   return (category_top_card_df,card_recommend_df)



