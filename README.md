白陽易經
from pandas import read_excel
hexa=read_excel('六十四卦EXCEL筆記.xls', sheet_name=None)
for k, v in hexa.items():v.to_csv(k+'.csv') #轉出成單一csv
#for txtFile in `ls *.txt`;do sed -i 's/[，。：]/ /g' $txtFile;done     #使用sed去除標點符號
