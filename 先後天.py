八卦={'乾':'111', '坤':'000', '離':'101', '坎':'010', '兌':'011', '震':'001', '巽':'110', '艮':'100'}
from dbUtil import runQuery
from rndrCode import rndrCode
from streamlit import columns as stCLMN

def orientHexa(LST):
  前, 後=[], []
  for ndx, v in enumerate(LST):
    if ndx>3:
      前.append('|'.join(v))
    else:
      後.append('|'.join(v))
  return ','.join(後)+'\n'+','.join(前)
  #return sep.join(v)
  #sep='\n'if ndx>4 else '|'
def mkOrient(方位, 先後白陽, 六十四DF):
  #stCode('：'.join([方位, 先後白陽]))
  前後卦數=set()
  for pos in range(len(先後白陽)):
    #pos=先後白陽.find(v)
    try: 前卦, 後卦=先後白陽[pos], 先後白陽[pos+1]
    except: 前卦, 後卦=先後白陽[-1], 先後白陽[0]
    前卦數=八卦.get(前卦)
    後卦數=八卦.get(後卦)
    前後數=前卦數+後卦數
    後前數=後卦數+前卦數
    #stCode(['數', 先天, 先天數, 先後天數, 後先天數])
    #dataframe(六十四DF)
    #dataframe(六十四DF.apply(六十四DF['本卦數']==先後天數)) #六十四DF[]
    前後卦數.add(前後數)
    前後卦數.add(後前數)
  #stCode(['前後卦數', 前後卦數])
  #stCode(前後卦數)
  hexaINFO=''
  for 卦數 in 前後卦數:
    hexaDF=六十四DF[六十四DF['本卦數']==卦數]
    #dataframe(hexaDF)
    hexaCODE=hexaDF['UTF代碼'].str.cat()
    #dHEXA='\u'+hexaCODE
    #from codecs import encode  #unicode
    #dHEXA=encode(hexaCODE)  #HEXA
    #stCode(dHEXA.decode('utf-8')) # decodeHEXA.encode('utf-8') .decode(encoding='utf-8').encode('utf-8').decode('utf-8')
    #apply(lambda x:x).astype('str').convert_dtypes() astype(basestring).replace('"', '').decode("utf8")
    #stCode(六十四DF[六十四DF['本卦數']==卦數])
    #fullQuery=f'''select {', '.join(卦爻辭欄位)} from 卦爻辭 where 卦辭象曰 ~* '{hexaPttrn}';'''
    #卦爻辭內文=runQuery(fullQuery, db='tao')
    卦名=六十四DF[六十四DF['本卦數']==卦數].本卦名.values[0]
    #stCode(六十四DF[六十四DF['本卦數']==卦數])
    fullQuery=f'''select 卦辭象曰 from 卦爻辭 where 本卦='{卦名}';'''
    卦爻辭內文=runQuery(fullQuery, db='herbal')
    hexaINFO+='|'.join([卦名, 卦爻辭內文[0][0]])+'\n'
  return hexaINFO
