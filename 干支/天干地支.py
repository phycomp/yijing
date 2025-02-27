from streamlit import text_input, radio as stRadio, sidebar, date_input
from random import choice
from datetime import datetime, date
from stUtil import rndrCode
from 五行 import rtrv五行
MENU, 表單=[], ['天干地支', '陽農曆', '五行']  #stPrflRprt , 'ydata', '錯綜複雜', '二十四節氣'
for ndx, Menu in enumerate(表單): MENU.append(f'{ndx}{Menu}')
#'histnum', 'seqno', 'diagnosis', 'rochefhir'], dtype='object')
天干 = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
地支 = ['子', '醜', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'] # 天干和地支
def 天干地支(year):
    if year < 0:
        # 公元前的年份，需要加 1
        year = year + 1

    # 計算天干和地支的索引，并獲取到對應字符
    天干數, 地支數=len(天干), len(地支)
    干 = 天干[(year % 天干數) - 4]
    支 = 地支[(year % 地支數) - 4]
    return 干 + 支 # 拼接天干和地支，返回最終結果
with sidebar:
  menu=stRadio('表單', MENU, horizontal=True, index=None)
  srch=text_input('搜尋', '')
curYear=datetime.now().year
#pickYear=choice()
from zhdate import ZhDate
lunar_date = ZhDate(2023, 6, 1)

def 計算天支(): # 计算年份的天干地支
  干 = TIANGAN[(self.lunar_datetime.year - 3) % 10 - 1]
  支 = DIZHI[(self.lunar_datetime.year - 3) % 12 - 1]
  return 干 + 支

#使用Python實現的生辰八字計算和納音五行計算類 支持實現以下功能
#1.支持公歷和農歷直接的相互轉換
#2.支持生辰八字的計算 即年柱 月柱 日柱和時柱
#3.支持生辰八字對應五行的輸出
#4.支持公歷和農歷兩種輸入參數

with sidebar:
  #年月日=date(2019, 7, 6)   #date_input('年代', date(2019, 7, 6))   #pickYear   range(1970, curYear)   , horizontal=True
  年月日=date_input("輸入日期", datetime.now())
  #rndmYear=date_input('年月日')
if menu==len(表單):
  pass
elif menu==MENU[2]: #ydata-profiling
  if 年月日:
    yy, mm, dd=年月日.year, 年月日.month, 年月日.day
  rtrv五行(yy, mm, dd)
elif menu==MENU[1]: #ydata-profiling
  if 年月日:
    yy, mm, dd=年月日.year, 年月日.month, 年月日.day
    #農曆=ZhDate(年月日)   #yy, mm, dd
    #rndrCode(農曆)
    #rndrCode(農曆)
    農曆=ZhDate(yy, mm, dd)  #2023, 6, 1 新建農歷
    rndrCode(農曆)  # 查看農歷
    陽曆=農曆.to_datetime() # 農歷轉換成陽歷日期datetime 類型
    rndrCode(陽曆)
    #陽曆 = datetime(2023, 7, 18) # 公歷轉農歷
    #農曆 = ZhDate.from_datetime(陽曆)
    #rndrCode(農曆)
elif menu==MENU[0]: #ydata-profiling
    年=年月日.year
    rndrCode(天干地支(int(年)))
