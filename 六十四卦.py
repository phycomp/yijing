from streamlit import sidebar, session_state, radio as stRadio, columns as stCLMN, text_area, text_input, multiselect, toggle as stToggle #slider, markdown, dataframe, code as stCode, text_input, code as stCode  code as stCode, cache as stCache, 

from stUtil import rndrCode
from dbUtil import runQuery
from pandas import DataFrame
from 先後天 import mkOrient, orientHexa
from rtrvHexa import rtrvHexa
from qryCLMN import queryCLMN
本卦名=['乾', '坤', '屯', '蒙', '需', '訟', '師', '比', '小畜', '履', '泰', '否', '同人', '大有', '謙', '豫', '隨', '蠱', '臨', '觀', '噬嗑', '賁', '剝', '復', '無妄', '大畜', '頤', '大過', '坎', '離', '咸', '恆', '遁', '大壯', '晉', '明夷', '家人', '睽', '蹇', '解', '損', '益', '夬', '姤', '萃', '升', '困', '井', '革', '鼎', '震', '艮', '漸', '歸妹', '豐', '旅', '巽', '兌', '渙', '節', '中孚', '小過', '既濟', '未濟']

MENU, 表單=[], ['六十四卦', '先後天', '卦爻辭', '錯綜複雜', '納甲法', '十翼', '占卜']   #二十四節氣, '尋找卦爻辭', '搜索病歷號', '視力手術'
for ndx, Menu in enumerate(表單): MENU.append(f'{ndx}{Menu}')
with sidebar:
  menu=stRadio('MENU', MENU, index=0, horizontal=True)
  hexaPttrn=text_input('查詢')
  卦名=stRadio('六十四卦', 本卦名, horizontal=True)
try:
  六十四DF=session_state['六十四']
  卦爻辭DF=session_state['卦爻辭']
  newHexaCLMN=session_state['新六十四欄']
  new卦爻欄=session_state['new卦爻欄']
  查詢欄位=session_state['查詢欄位']
except Exception as e:
  hexaCLMN=queryCLMN(tblSchm='public', tblName='HEXA', db='herbal')
  六十四=runQuery(f'''select {','.join(hexaCLMN)} from "HEXA";''', db='herbal')   # where 本卦名='{卦名}'
  newHexaCLMN=session_state['新六十四欄']=list(map(lambda x:x.replace('"', ''), hexaCLMN))
  六十四DF=session_state['六十四']=DataFrame(六十四, index=None, columns=newHexaCLMN)    #本卦欄位

  卦爻辭欄=queryCLMN(tblSchm='public', tblName='卦爻辭', db='herbal')
  卦爻辭=runQuery(f'''select {','.join(卦爻辭欄)} from 卦爻辭;''', db='herbal')  # where 本卦='{卦名}'
  查詢欄位=new卦爻欄=list(map(lambda x:x.replace('"', ''), 卦爻辭欄))
  卦爻辭DF=session_state['卦爻辭']=DataFrame(卦爻辭, index=None, columns=new卦爻欄)    #本卦欄位
  查詢欄位.remove('id')
  session_state['查詢欄位']=查詢欄位
  #卦DF=DataFrame(爻辭卦, index=None, columns=hexaCLMN)  #卦爻辭欄位
qryCLMN=multiselect('查詢卦爻欄位', 查詢欄位)
isDisplayed = stToggle("顯示卦爻辭")
if isDisplayed:
  六十四DF
  卦爻辭DF
if menu==len(MENU):
  pass
elif menu==MENU[6]: #'占卜'
  pass
elif menu==MENU[5]: #'十翼'
  pass
elif menu==MENU[4]: #納甲法二十四節氣
  pass
elif menu==MENU[3]: #'錯綜複雜'
  #CLMN=queryCLMN(tblSchm='public', tblName='HEXA', db='herbal')
  #rsltHEXA=runQuery(f"""select {','.join(CLMN)} from "HEXA";""", db='herbal')
  #hexaDF=DataFrame(rsltHEXA, columns=CLMN)    #
  六十四DF=session_state['六十四']
  卦爻辭DF=session_state['卦爻辭']
  hexa=stRadio('錯綜複雜', '錯綜複雜', horizontal=True) #縱
  if hexa:
    newHEXA=六十四DF[六十四DF['本卦名']==卦名][f'{hexa}卦名'].values[0]##
    #rndrCode(newHEXA.values[0])
    leftPane, rightPane=stCLMN([5, 15])
    with leftPane:
      六十四DF[六十四DF['本卦名']==newHEXA].T   #hexaDF[]
    with rightPane:
      卦爻辭DF[卦爻辭DF['本卦']==卦名].T#[f'{hexa}卦名'].values[0]##
    #rndrCode(newHEXA.values[0])
    #hexaDF[hexaDF['本卦名']==new卦爻辭]   #hexaDF[]
elif menu==MENU[2]:
  CLMN=queryCLMN(tblSchm='public', tblName='卦爻辭', db='herbal')
  rsltHEXA=runQuery(f"""select {','.join(CLMN)} from 卦爻辭;""", db='herbal')
  hexaDF=DataFrame(rsltHEXA, columns=CLMN)    #
elif menu==MENU[1]:  #'二十四節氣'
  from collections import OrderedDict
  cnt, 八卦方位=0, OrderedDict([('正北', '坤坎坎'), ('東北', '震艮艮'), ('正東', '離震坤'), ('東南', '兌巽震'), ('正南', '乾離離'), ('西南', '巽坤兌'), ('正西', '坎兌乾'), ('西北', '艮乾巽')])
  with sidebar:
    orientHexa=orientHexa(list(八卦方位.items()))    #, args=
    text_area('八卦方位', orientHexa)   #','.join()
  leftPane, rightPane=stCLMN([1,1])
  hexa方位=list(八卦方位.keys())
  for 方位, 先後白陽 in 八卦方位.items():
    hexaINFO=mkOrient(方位, 先後白陽, 六十四DF)
    if cnt>=4:
      with rightPane:
        text_area(hexa方位[cnt], hexaINFO[:-1])
    else:
      with leftPane:
        text_area(hexa方位[cnt], hexaINFO[:-1])
    cnt+=1

elif menu==MENU[0]:
  leftPane, midPane, rightPane=stCLMN([4, 12, 8])
  if 卦名:
    with leftPane:
      六十四DF[六十四DF['本卦名']==卦名].T
    with rightPane:
      卦爻辭DF[卦爻辭DF['本卦']==卦名].T
      #卦爻辭DF.T
    #卦爻辭欄位=['本卦', '卦辭象曰']
    if hexaPttrn:
      qryPttrn=' or '.join([f"{v} ~ '{hexaPttrn}'" for v in qryCLMN])
      fullQuery=f'''select {','.join(qryCLMN)} from 卦爻辭 where {qryPttrn};'''   #卦辭象曰 ~ '{hexaPttrn}'
      rndrCode(fullQuery)
      卦爻辭內文=runQuery(fullQuery, db='herbal')
      卦爻辭內文DF=DataFrame(卦爻辭內文, columns=查詢欄位, index=None)
      with midPane:
        卦爻辭內文DF.T
