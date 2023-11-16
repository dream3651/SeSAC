from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import konlpy
import matplotlib.pyplot as plt
import seaborn as sns

driver=webdriver.Chrome()
# 검색어는 '쓰레기'
url="https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%93%B0%EB%A0%88%EA%B8%B0"
driver.get(url)

html=driver.page_source
soup=BeautifulSoup(html,'html.parser')

page_count=50  # 50 page만 추출
naver_news=[]
for _ in range(page_count):
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    
    news_list=soup.select('ul.list_news > li')
    
    for news in news_list:
        brief_news=news.select('a.api_txt_lines.dsc_txt_wrap')[0].text.strip()
        naver_news.append(brief_news)
    
    next_btn=driver.find_elements('css selector', 'a.btn_next')[0]
    next_btn.click()
    print(naver_news)

    text="\n".join(naver_news)
okt=konlpy.tag.Okt()
words=okt.pos(text)

df2 = pd.DataFrame({'word' : words})
kor2=df2['word'].apply(lambda x:x[0])
kor_type2=df2['word'].apply(lambda x:x[1])

df2['key_word']=kor2
df2['kor_type']=kor_type2

df2=df2[df2['kor_type']=='Noun']

df2['count']=df2['key_word'].str.len()
df2=df2.query('count>=2')

df2=df2.groupby('key_word', as_index=False).agg(n=('key_word','count')).sort_values('n', ascending=False)

top_20=df2.head(20)
# 위해 삭제
# df2[df2['key_word']=="위해"]
df2=df2.drop([1991],axis=0)

font="C:\Windows\Fonts\HMFMPYUN.TTF"
plt.rcParams.update({'font.family'    : 'Malgun Gothic', 'figure.dpi' : '120',  'figure.figsize' : [6.5, 6]})        
sns.barplot(data = top_20, y = 'key_word', x = 'n')



