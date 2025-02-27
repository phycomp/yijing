白陽易經
from pandas import read_excel
hexa=read_excel('六十四卦EXCEL筆記.xls', sheet_name=None)
for k, v in hexa.items():v.to_csv(k+'.csv') #轉出成單一csv
#for txtFile in `ls *.txt`;do sed -i 's/[，。：]/ /g' $txtFile;done     #使用sed去除標點符號

"本卦名","本卦組合","本卦數","錯卦名","錯卦數","縱卦名","縱卦數","複卦名","複卦數","雜卦名","雜卦數","UTF代碼"
