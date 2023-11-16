import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import seaborn as sns

waste_day=pd.read_csv("waste/0_1_waste_01_21.csv", encoding='cp949')
waste_day=waste_day.transpose()

waste_day.rename(columns=waste_day.iloc[0],inplace=True)
waste_day=waste_day.drop(waste_day.index[0])

waste_day[['전체','생활계폐기물','사업장배출시설계폐기물및건설폐기물','지정폐기물']]=waste_day[['전체','생활계폐기물','사업장배출시설계폐기물및건설폐기물','지정폐기물']].astype(float)
waste_day=waste_day.reset_index()
waste_day=waste_day.rename(columns={'index':'년도','사업장배출시설계폐기물및건설폐기물':'사업장_건설폐기물','지정폐기물발생량':'지정폐기물'})

waste_day['total_pct']=waste_day['전체'].pct_change()*100
waste_day['domestic_pct']=waste_day['생활계폐기물'].pct_change()*100
waste_day['biz_pct']=waste_day['사업장_건설폐기물'].pct_change()*100
waste_day['designated_pct']=waste_day['지정폐기물'].pct_change()*100
waste_day['전체'].max()


plt.figure(figsize=(10, 8))
plt.plot(waste_day.loc[1:]['년도'], waste_day.loc[1:]['total_pct'], marker='o')
plt.plot(waste_day.loc[1:]['년도'], waste_day.loc[1:]['domestic_pct'], marker='o')
plt.plot(waste_day.loc[1:]['년도'], waste_day.loc[1:]['biz_pct'], marker='o')
plt.plot(waste_day.loc[1:]['년도'], waste_day.loc[1:]['designated_pct'], marker='o')
plt.legend(['전체', '생활계폐기물', '사업장_건설폐기물','지정폐기물'])
plt.xlabel('년도')
plt.ylabel('변동률(%)')
plt.title('연간 폐기물의 증감률')
plt.grid(False)
plt.show()


plt.figure(figsize=(10, 8))
plt.plot(waste_day.loc[1:]['년도'], waste_day.loc[1:]['total_pct'], marker='o', color='#FF0060')
plt.xlabel('년도')
plt.ylabel('변동률(%)')
plt.title('연간 폐기물의 증감률(2001~2021년)')
plt.grid(False)
plt.show()


# 총인구 기준
population=pd.read_csv("waste/8_population_01_21.csv", encoding='cp949')
population=population.transpose()
population.rename(columns=population.iloc[0],inplace=True)
population=population.drop(population.index[0])
population[['총인구','인구성장률','자연증가']]=population[['총인구','인구성장률','자연증가']].astype(float)
population=population.reset_index()

waste_day=pd.merge(waste_day, population, how='left', on='년도')

#폐기물 배출량과 총인구의 상관계수
waste_day[['전체','총인구']].corr()

#폐기물 배출량과 총인구의 유의확률.
#유의확률이 0.05 미만이므로 두 변수의 상관관계가 통계적으로 유의함
ss.pearsonr(waste_day['전체'], waste_day['총인구'])

growth=pd.read_csv("waste/12_economic_growth_rate_01_21.csv", encoding='cp949')
growth=growth.transpose()
growth=growth.iloc[1:]
growth=growth.rename(columns={0:'경제성장률'})
growth=growth.reset_index(drop=False)
growth=growth.rename(columns={'index':'년도'})

waste_day=pd.merge(waste_day, growth, how='left', on='년도')

#폐기물 배출량과 경제성장률의 유의확률.
#유의확률이 0.05 미만이므로 두 변수의 상관관계가 통계적으로 유의함
ss.pearsonr(waste_day['전체'], waste_day['경제성장률'])

import matplotlib
from matplotlib import font_manager, rc
import platform


if platform.system()=="Windows":
    font_name=font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus']=False
import warnings
warnings.filterwarnings("ignore")


## 폐기물 종류별 연간 폐기물량
plt.figure(figsize=(10, 7))
plt.bar(waste_day['년도'],waste_day['사업장_건설폐기물'],label='사업장_건설폐기물', color="#435334")
plt.bar(waste_day['년도'],waste_day['생활계폐기물'], bottom=waste_day['사업장_건설폐기물'], label='생활계폐기물', color="#9EB384")
plt.bar(waste_day['년도'],waste_day['지정폐기물'], bottom=waste_day['생활계폐기물']+waste_day['사업장_건설폐기물'], label='지정폐기물', color="#CEDEBD")
plt.xlabel('년도')
plt.ylabel('폐기물량(톤/일)')
plt.legend()
plt.title('폐기물 발생량(2001~2021)')
plt.show()

waste_day.iloc[20, 2:]

## 2021년 폐기물의 종류
labels = ['생활계폐기물','사업장_건설폐기물','지정폐기물'] ## 라벨
waste_2021 = waste_day.iloc[20, 2:5].to_list() ## 데이터


fig = plt.figure(figsize=(5,5)) ## 캔버스 생성
fig.set_facecolor('white') ## 캔버스 배경색을 하얀색으로 설정
ax = fig.add_subplot() ## 프레임 생성 
pie = ax.pie(waste_2021, ## 파이차트 출력
       startangle=90, ## 시작점을 90도(degree)로 지정
       counterclock=False, ## 시계 방향으로 그린다.
       autopct=lambda p : '{:.1f}%'.format(p), ## 퍼센티지 출력
       wedgeprops=dict(width=0.6), ## 중간의 반지름 0.5만큼 구멍을 뚫어준다.
       pctdistance=0.7,  ## 퍼센트 위치지정
       colors=['#FFDBAA','#96C291','#FFB7B7']
        )
plt.legend(pie[0],labels) ## 범례 표시
ax.set_title("2021년 폐기물의 종류")
plt.show()


disposal=pd.read_csv("waste/0_2_waste_disposal_01_21.csv", encoding='cp949')


# 폐기물 발생량 및 처리현황(2001~2021년)
plt.figure(figsize=(8, 5))
plt.bar(disposal['년도'],disposal['처리_재활용'],label='재활용', color="#618264")
plt.bar(disposal['년도'],disposal['처리_매립'], bottom=disposal['처리_재활용'], label='매립', color="#79AC78")
plt.bar(disposal['년도'],disposal['처리_소각'], bottom=disposal['처리_매립']+disposal['처리_재활용'], label='소각', color="#B0D9B1")
plt.bar(disposal['년도'],disposal['처리_기타'], bottom=disposal['처리_소각']+disposal['처리_매립']+disposal['처리_재활용'], label='기타', color="#D0E7D2")
plt.xlabel('년도')
plt.ylabel('폐기물처리량(톤/일)')
plt.legend()
plt.title('폐기물 처리량(2001~2021)')
plt.show()


disposal['년도']=disposal['년도'].astype(object)
disposal.iloc[0, 6:].to_list

## 2001년 폐기물의 처리 현황(종합)
labels = ['매립','소각','재활용','기타'] ## 라벨
disposal_2001 = disposal.iloc[0, 6:].to_list() ## 데이터


fig = plt.figure(figsize=(5,5)) ## 캔버스 생성
fig.set_facecolor('white') ## 캔버스 배경색을 하얀색으로 설정
ax = fig.add_subplot() ## 프레임 생성
pie = ax.pie(disposal_2001, ## 파이차트 출력
       startangle=90, ## 시작점을 90도(degree)로 지정
       counterclock=False, ## 시계 방향으로 그린다.
       autopct=lambda p : '{:.1f}%'.format(p), ## 퍼센티지 출력
       wedgeprops=dict(width=0.6), ## 중간의 반지름 0.5만큼 구멍을 뚫어준다.
       pctdistance=0.7,  ## 퍼센트 위치지정
       colors=['#FFB7B7','#FFDBAA','#96C291','#F4EEEE']
        )
plt.legend(pie[0],labels) ## 범례 표시
ax.set_title("2001년 폐기물 처리 현황")
plt.show()


disposal.iloc[20, 6:]


## 2021년 폐기물의 처리 현황(종합)
labels = ['매립','소각','재활용','기타'] ## 라벨
disposal_2021 = disposal.iloc[20, 6:].to_list() ## 데이터


fig = plt.figure(figsize=(5,5)) ## 캔버스 생성
fig.set_facecolor('white') ## 캔버스 배경색을 하얀색으로 설정
ax = fig.add_subplot() ## 프레임 생성
pie = ax.pie(disposal_2021, ## 파이차트 출력
       startangle=90, ## 시작점을 90도(degree)로 지정
       counterclock=False, ## 시계 방향으로 그린다.
       autopct=lambda p : '{:.1f}%'.format(p), ## 퍼센티지 출력
       wedgeprops=dict(width=0.6), ## 중간의 반지름 0.5만큼 구멍을 뚫어준다.
       pctdistance=0.7,  ## 퍼센트 위치지정
       colors=['#FFB7B7','#FFDBAA','#96C291','#F4EEEE']
        )
plt.legend(pie[0],labels) ## 범례 표시
ax.set_title("2021년 폐기물 처리 현황")
plt.show()


disposal_type=pd.read_csv("waste/16_type_of_disposal_21.csv", encoding='cp949')

## 2021년 생활계폐기물 처리 현황
labels = ['재활용','소각','매립','기타'] ## 라벨
type1 = disposal_type.iloc[0, 3:].to_list() ## 데이터


fig = plt.figure(figsize=(5,5)) ## 캔버스 생성
fig.set_facecolor('white') ## 캔버스 배경색을 하얀색으로 설정
ax = fig.add_subplot() ## 프레임 생성
pie = ax.pie(type1, ## 파이차트 출력
       startangle=90, ## 시작점을 90도(degree)로 지정
       counterclock=False, ## 시계 방향으로 그린다.
       autopct=lambda p : '{:.1f}%'.format(p), ## 퍼센티지 출력
       wedgeprops=dict(width=0.6), ## 중간의 반지름 0.5만큼 구멍을 뚫어준다.
       pctdistance=0.7,  ## 퍼센트 위치지정
       colors=['#7EAA92','#9ED2BE','#C8E4B2','#FFD9B7']
        )
plt.legend(pie[0],labels) ## 범례 표시
ax.set_title("2021년 생활계폐기물 처리 현황")
plt.show()


## 2021년 사업장_건설폐기물 처리 현황
labels = ['재활용','소각','매립','기타'] ## 라벨
type2 = disposal_type.iloc[1, 3:].to_list() ## 데이터


fig = plt.figure(figsize=(5,5)) ## 캔버스 생성
fig.set_facecolor('white') ## 캔버스 배경색을 하얀색으로 설정
ax = fig.add_subplot() ## 프레임 생성
explode = [0,0,0.1,0]
pie = ax.pie(type2, ## 파이차트 출력
       startangle=90, ## 시작점을 90도(degree)로 지정
       counterclock=False, ## 시계 방향으로 그린다.
       autopct=lambda p : '{:.1f}%'.format(p), ## 퍼센티지 출력
       wedgeprops=dict(width=0.6), ## 중간의 반지름 0.5만큼 구멍을 뚫어준다.
       pctdistance=0.7,  ## 퍼센트 위치지정
       explode=explode,
       colors=['#7EAA92','#9ED2BE','#C8E4B2','#FFD9B7']
        )
plt.legend(pie[0],labels) ## 범례 표시
ax.set_title("2021년 사업장_건설폐기물 처리 현황")
plt.show()


## 2021년 사업자지정폐기물 처리 현황
labels = ['재활용','소각','매립','기타'] ## 라벨
type3 = disposal_type.iloc[2, 3:].to_list() ## 데이터


fig = plt.figure(figsize=(5,5)) ## 캔버스 생성
fig.set_facecolor('white') ## 캔버스 배경색을 하얀색으로 설정
ax = fig.add_subplot() ## 프레임 생성
pie = ax.pie(type3, ## 파이차트 출력
       startangle=90, ## 시작점을 90도(degree)로 지정
       counterclock=False, ## 시계 방향으로 그린다.
       autopct=lambda p : '{:.1f}%'.format(p), ## 퍼센티지 출력
       wedgeprops=dict(width=0.6), ## 중간의 반지름 0.5만큼 구멍을 뚫어준다.
       pctdistance=0.7,  ## 퍼센트 위치지정
       colors=['#7EAA92','#9ED2BE','#C8E4B2','#FFD9B7']
        )
plt.legend(pie[0],labels) ## 범례 표시
ax.set_title("2021년 사업장지정폐기물 처리 현황")
plt.show()


# 2021년 지역별 생활계폐기물 발생량 및 처리 현황
area_2021=pd.read_csv("waste/17_domestic_by_region_21.csv", encoding='cp949')

recycle=area_2021.groupby('시도').agg(waste_sum=('2021발생량(톤/년)','sum'),recycle_sum=('재활용','sum'))
recycle_area=recycle.assign(recycle_rate=recycle['recycle_sum']/recycle['waste_sum']*100)
recycle_area=recycle_area.sort_values('waste_sum', ascending=False)

pop_2021=pd.read_csv("waste/18_district_population_21.csv", encoding='cp949')
pop_area=pop_2021.groupby('시도').agg(population=('인구(명)','sum'),household=('세대수(가구)','sum'))

area_all=pd.merge(recycle_area,pop_area, how='left',on='시도')
area_all=area_all.reset_index()
area_all=area_all.sort_values('waste_sum', ascending=False)

## 2021년 지역별 생활계 폐기물 발생량과 재활용 처리 비율
# 데이터 준비
x = area_all['시도']
y1 = area_all['recycle_rate']
y2 = area_all['waste_sum']/1000000


# 그래프 그리기
fig, ax1 = plt.subplots()
ax1.plot(x, y1, '-s', color='#191D88', markersize=3, linewidth=2, alpha=0.7, label='rate')
ax1.set_ylim([0, 100])
ax1.set_xlabel('시도')
ax1.set_ylabel('recycle rate(%)')
ax1.tick_params(axis='both', direction='in')

for i in range(len(x)):
    height = y1[i]
    plt.text(x[i], height + 1, '%.1f' %height, ha='center', va='bottom', size = 10)

ax2 = ax1.twinx()
ax2.bar(x, y2, color='#FFB07F', label='waste', alpha=0.7, width=0.5)
ax2.set_ylim(0, 6)
ax2.set_ylabel('waste(million twaste(million ton)on)')
ax2.tick_params(axis='y', direction='in')
plt.title('지역별 생활계 폐기물의 발생량 및 재활용률(2021)')
plt.show()


area_all=area_all.sort_values('population', ascending=False)

## 2021년 지역별 인구수와 생활계 폐기물의 재활용 처리 비율
# 데이터 준비
x = area_all['시도']
y1 = area_all['recycle_rate']
y2 = area_all['population']/1000000


# 그래프 그리기
fig, ax1 = plt.subplots()
ax1.plot(x, y1, '-s', color='#191D88', markersize=3, linewidth=2, alpha=0.7, label='rate')
ax1.set_ylim([0, 100])
ax1.set_xlabel('시도')
ax1.set_ylabel('recycle rate(%)')
ax1.tick_params(axis='both', direction='in')

for i in range(len(x)):
    height = y1[i]
    plt.text(x[i], height + 1, '%.1f' %height, ha='center', va='bottom', size = 10)

ax2 = ax1.twinx()
ax2.bar(x, y2, color='#FFB07F', label='population', alpha=0.7, width=0.5)
ax2.set_ylim(0, 15)
ax2.set_ylabel('population(million ton)')
ax2.tick_params(axis='y', direction='in')
plt.title('지역별 인구와 재활용률(2021)')
plt.show()


area_all['waste_sum'].sum()
area_all=area_all.assign(waste_per_day=area_all['waste_sum']/365)

# 지역별 1인당 일일 생활계폐기물 발생량 
area_all=area_all.assign(waste_head=area_all['waste_per_day']/area_all['population']*1000)

# 생활계폐기물 /생활폐기물관리지역 인구   => 1인당 1일 폐기물 배출량 1.18kg
area_all['waste_per_day'].sum()/(area_all['population'].sum()*1000)
area_all=area_all.sort_values('waste_sum', ascending=False)

## 2021년 지역별 1인당 일일 생활계 폐기물 배출량
# 데이터 준비
x = area_all['시도']
y1 = area_all['waste_head']
y2 = area_all['waste_per_day']

# 그래프 그리기
fig, ax1 = plt.subplots()
ax1.plot(x, y1, '-s', color='#191D88', markersize=3, linewidth=2, alpha=0.7, label='rate')
ax1.set_ylim([0, 2])
ax1.set_xlabel('시도')
ax1.set_ylabel('waste per head(kg)')
ax1.tick_params(axis='both', direction='in')

for i in range(len(x)):
    height = y1[i]
    plt.text(x[i], height + 0.05, '%.1f' %height, ha='center', va='bottom', size = 10)

ax2 = ax1.twinx()
ax2.bar(x, y2, color='#FFB07F', label='waste', alpha=0.7, width=0.5)
ax2.set_ylim(0, 16000)
ax2.set_ylabel('waste per day(ton)')
ax2.tick_params(axis='y', direction='in')
plt.title('지역별 1인당 일일 생활계 폐기물 배출량(2021)')
plt.show()

# 2001~2021년 OECD 주요국의 1인당 생활폐기물발생량
waste_country=pd.read_csv("waste/19_waste_per_head_OECD_02_18.csv", encoding='cp949')

country_2018=waste_country[['국가','2018']].sort_values('2018')


plt.figure(figsize=(10, 5))
y = range(0,15)
country = country_2018['국가']
values = country_2018['2018']
plt.barh(y, values)
plt.yticks(y, country)
plt.show()


plastic_21=pd.read_csv("waste/5_domestic_21.csv", encoding='cp949')
pet=plastic_21[plastic_21['폐기물_종류.2']=='PET병']['년도_발생량'].sum()
pet/plastic_21['년도_발생량'].sum()*100
plastic_21.groupby('폐기물_종류.2').agg(waste_ttl=('년도_발생량','sum'))