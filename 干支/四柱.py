sxtwl是參考壽星天文歷 并使用C++實現日歷庫。因爲其依據天文歷法算法實現，故其可查詢範圍廣(BC722年以後與實歷相符，支持1800年以前及2200年以後的日歷查詢)。支持Android、IOS、Windows、MacOS、Linux等平台。使用swig暴露接口給python,lua,java等語言使用。

安裝方法
pip install sxtwl
舊工程代碼兼容 如果有已使用V1.x版本的工程，想兼容代碼

pip install sxtwl==1.1.0
或者在requirements.txt裏修改

sxtwl 1.1.0
具體使用方法參考： https://pypi.org/project/sxtwl/

本項目 GitHub / Gitee（碼云）。

因爲pip上傳後不能二次修改，參考事例可能會有錯誤無法修改，如果發現下面例子不能用，請以爲準: 傳送門

因爲考慮到繁體和簡體字的原因，所以本庫不以硬編碼的形式顯示結果。下面是參考的簡單索引
Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ShX = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]
numCn = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "驚蟄", "春分", "清明", "谷雨", "立夏", "小滿", "芒種", "夏至", "小暑", "大暑", "立秋", "處暑","白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"]
ymc = ["十一", "十二", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十" ]
rmc = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", 
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
XiZ = ['摩羯', '水瓶', '雙魚', '白羊', '金牛', '雙子', '巨蟹', '獅子', '處女', '天秤', '天蝎', '射手']
WeekCn = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]

from sxtwl import fromSolar, fromLunar
day = fromSolar(2021, 11, 7) # 從公歷年月日獲取一天的信息
day = fromLunar(2020, 12, 1) #從農歷年月日獲取一天的信息
獲取某天的信息(這裏的信息有，陰歷，陽歷，二十四節氣，天干地支，星期幾等)
print(f"公歷:{day.getSolarYear()}年{day.getSolarMonth()}月{day.getSolarDay()}日") # 公歷的年月日

print(WeekCn[day.getWeek()]) # 星期幾

print(f'該日屬于這個月的第{day.getWeekIndex()}周') #這個月的第幾周

# 星座(有bug?待修復)
print("星座:", XiZ[day.getConstellation()])

# 以春節爲界的農歷(注getLunarYear如果沒有傳參，或者傳true，是以春節爲界的)
s = "農歷:%d年%s%d月%d日" % (day.getLunarYear(), 
    '閏' if day.isLunarLeap() else '', day.getLunarMonth(), day.getLunarDay())
print(s)

# 以立春爲界的農歷
s = "農歷:%d年%s%d月%d日" % (day.getLunarYear(False), 
    '閏' if day.isLunarLeap() else '', day.getLunarMonth(), day.getLunarDay())
print(s)


# 以春節爲界的天干地支 
yTG = day.getYearGZ(True)
print("以春節爲界的年干支", Gan[yTG.tg] + Zhi[yTG.dz]) 
print("以春節爲界的生肖:", ShX[yTG.dz])

# 以立春爲界的天干地支 （注，如果沒有傳參，或者傳false，是以立春爲界的。剛好和getLunarYear相反）
yTG = day.getYearGZ()
print("以立春爲界的年干支", Gan[yTG.tg] + Zhi[yTG.dz]) 
print("以立春爲界的生肖:", ShX[yTG.dz])

mTG = day.getMonthGZ()
print("月干支", Gan[mTG.tg] + Zhi[mTG.dz]) #月干支

#日干支
dTG  = day.getDayGZ()
print("日干支", Gan[dTG.tg] + Zhi[dTG.dz]) 

#時干支,傳24小時制的時間，分早晚子時
hour = 18
sTG = day.getHourGZ(hour)
print("%d時的干支"%(hour, ), Gan[sTG.tg] + Zhi[sTG.dz]) 

#時干支
for hour in range(24):
    # 第一個參數爲該天的天干，第二個參數爲小時
    hTG  = sxtwl.getShiGz(dTG.tg, hour)
    print("%d時天干地支:"%(hour), Gan[hTG.tg] + Zhi[hTG.dz])


# 當日是否有節氣
if day.hasJieQi():
    print('節氣：%s'% jqmc[day.getJieQi()])
    #獲取節氣的儒略日數
    jd = day.getJieQiJD()
    # 將儒略日數轉換成年月日時秒
    t = sxtwl.JD2DD(jd )

    # 注意，t.s是小數，需要四舍五入
    print("節氣時間:%d-%d-%d %d:%d:%d"%(t.Y, t.M, t.D, t.h, t.m, round(t.s)))
else:
    print("當天不是節氣日")

獲取某日的前幾天或者後幾天的信息 （可以用到很多場景中）
# 獲取某天的後面幾天
num = 1    #你喜歡寫多少天 也多少天，可以寫負數，相當于往前
day = day.after(num)  #獲取num天後的日信息
s = "公歷:%d年%d月%d日" % (day.getSolarYear(), day.getSolarMonth(), day.getSolarDay())
print(s)

# 同上
day = day.before(num)
s = "公歷:%d年%d月%d日" % (day.getSolarYear(), day.getSolarMonth(), day.getSolarDay())
print(s)
獲取一年中的閏月
# 獲取一年中的閏月
year = 2020
month = sxtwl.getRunMonth(year)
if month >= 0:
    print("%d年的閏月是%d"%(year, month) )
else:
    print("沒有閏月")
獲取一個農歷月的天數
# 一個農歷月的天數
year = 2020 #農歷年
month  = 4 #農歷月
isRun = False #是否是閏月
daynum = sxtwl.getLunarMonthNum(year, month, isRun)
print("農歷%d年%s%d月的天數:"%(year, '閏'if isRun else '', month), daynum)

儒略日數與公歷的互轉
#儒略日數轉公歷
jd = sxtwl.J2000
t = sxtwl.JD2DD(jd )

#公歷轉儒略日
jd = sxtwl.toJD(t)
查找某日之前或者之後的節氣
# 查找某日前後的節氣,此例爲之後，之前把after替換成before
while True:
    # 這裏可以使用after或者before，不用擔心速度，這裏的計算在底層僅僅是+1這麼簡單
    day = day.after(1)
    # hasJieQi的接口比getJieQiJD速度要快，你也可以使用getJieQiJD來判斷是否有節氣。
    if day.hasJieQi():
        print('節氣：%s'% jqmc[day.getJieQi()])
        #獲取節氣的儒略日數， 如果說你要計算什麼時間的相距多少，直接比對儒略日要方便，相信我。
        jd = day.getJieQiJD()

        # 將儒略日數轉換成年月日時秒
        t = sxtwl.JD2DD(jd )

        # 注意，t.s是小數，需要四舍五入
        print("節氣時間:%d-%d-%d %d:%d:%d"%(t.Y, t.M, t.D, t.h, t.m, round(t.s)))

        break
四柱反查 (好像還有bug，待修復)
###==================================================================================
# 四柱反查工具方法
# 實際項目中不要這樣子搞哈，因爲漢字utf-8，GBK2312不同的編碼。建議還是直接使用天干地支的數字索引 
def getGZ(gzStr):
    tg = -1
    dz = -1
    for i, v in enumerate(Gan):
        if gzStr[0]  == v:
            tg = i
            break

    for i, v in enumerate(Zhi):
        if  gzStr[1] == v:
            dz = i
            break   
    return sxtwl.GZ(tg, dz)
###==================================================================================

# 四注反查 分別傳的是年天干，月天干，日天干，時天干， 開始查詢年，結束查詢年  返回滿足條件的儒略日數
jds = sxtwl.siZhu2Year(getGZ('辛丑'), getGZ('己亥'), getGZ('丙寅'), getGZ('癸巳'), 2003, 2029);
for jd in jds:
    t = sxtwl.JD2DD(jd )
    print("符合條件的時間:%d-%d-%d %d:%d:%d"%(t.Y, t.M, t.D, t.h, t.m, round(t.s)))
