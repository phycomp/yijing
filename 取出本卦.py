from streamlit import sidebar, text_input, columns as stCLMN, radio as stRadio, dataframe
from rndrCode import rndrCode

def rtrvHexa(hexaDF, CLMN, 特定):
  dataframe(hexaDF)
  with sidebar:
    srch=text_input('搜尋', '')
  leftPane, rightPane=stCLMN([5, 15])
  with leftPane:
    hexa=stRadio('卦名', CLMN, horizontal=True, index=0)
  with rightPane:
    if hexa:
      #rndrCode([hexaDF[hexaDF[特定].str.contains(hexa)].T, CLMN, 特定])
      #hexaDF[['本卦']==hexa] #.query(f"本卦=='{hexa}'")  #[['卦名']==hexa]query(f'醫籍=={dset.values[0]}')
      df=hexaDF[hexaDF[特定].str.contains(hexa)].T
      dataframe(df)
