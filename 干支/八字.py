#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 釘釘、抖音或微信pythontesting 釘釘群21734177
# CreateDate: 2019-2-21

import argparse
import collections
import pprint
from lunar_python import Lunar, Solar
#from colorama import init
from datas import self_zuo
from sizi import summarys
from common import *
from yue import months
from stUtil import rndrCode
from streamlit import date_input, radio as stRadio, sidebar, text_input
from datetime import datetime as DT, date
from sxtwl import siZhu2Year, JD2DD, GZ
from 算八字 import rtrv八字

curDT=DT.now() #http://www.131.com.tw/word/b3_2_14.htm
命格=['計算五行分數', '計算八字強弱', '子平真诠的計算', '計算大運', '網上的計算', '輸出地支關系', '輸出地支minor關系', '輸出根', ]
MENU, 表單=[], ['四柱', '算命', '陽農曆', '五行']  #stPrflRprt , 'ydata', '錯綜複雜', '二十四節氣'
for ndx, Menu in enumerate(表單): MENU.append(f'{ndx}{Menu}')
rndrCode(['MENU', MENU, curDT])
with sidebar:
  menu=stRadio('表單', MENU, horizontal=True, index=0)
  陽農=stRadio('曆別', ['陽曆', '農曆'], horizontal=True, index=0)
  正逆=stRadio('方向', ['正向', '逆向'], horizontal=True, index=0)
  算出命格=stRadio('命格', 命格, horizontal=True, index=0)
  srch=text_input('搜尋', '')
  年月日=date_input("輸入日期", curDT)
#curYear=datetime.now().year
#pickYear=choice()
#from zhdate import ZhDate
#lunar_date = ZhDate(2023, 6, 1)
方向=True if 正逆=='正向' else False
Gans = collections.namedtuple("Gans", "year month day time")
Zhis = collections.namedtuple("Zhis", "year month day time")

def jin_jiao(first, second):
    return True if Zhi.index(second) - Zhi.index(first) == 1 else False

description = '''

parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('year', action="store", help=u'year')
parser.add_argument('month', action="store", help=u'month')
parser.add_argument('day', action="store", help=u'day')
parser.add_argument('time', action="store",help=u'time')    
parser.add_argument("--start", help="start year", type=int, default=1850)
parser.add_argument("--end", help="end year", default='2030')
parser.add_argument('-b', action="store_true", default=False, help=u'直接輸入八字')
parser.add_argument('-g', action="store_true", default=False, help=u'是否采用公歷')
parser.add_argument('-r', action="store_true", default=False, help=u'是否爲閏月，僅僅使用于農歷')
parser.add_argument('-n', action="store_true", default=False, help=u'是否爲女，默認爲男')
parser.add_argument('--version', action='version', version='%(prog)s 1.0 Rongzhong xu 2022 06 15')
options = parser.parse_args()

rndrCode(options)
'''
def rtrv四柱():
  天干='甲乙丙丁戊己庚辛壬癸'
  地支='子丑寅卯辰巳午未申酉戌亥'
  from random import choice
  干=choice(天干)
  支=choice(地支)
  return 干+支

if menu==len(表單):
  pass
elif menu==MENU[0]: #ydata-profiling
  #rndmYear=date_input('年月日')
  四柱=''
  for itr in range(4): 四柱+=rtrv四柱()
  rndrCode(['四柱', 四柱])

  if 四柱:
    #yy, mm, dd=年月日.year, 年月日.month, 年月日.day
    干年, 干月, 干日, 干時=四柱[::2]
    gans = Gans(year=干年, month=干月, day=干日, time=干時)#, options.month[0], options.day[0], options.time[0]
    rndrCode([干年, 干月, 干日, 干時, gans])
    支年, 支月, 支日, 支時=四柱[1::2]
    zhis = Gans(year=支年, month=支月, day=支日, time=支時)#, options.month[0], options.day[0], options.time[0]
    rndrCode([支年, 支月, 支日, 支時, zhis])
    #rndrCode([干支年, 干支月, 干支日, 干支時])
    干支年, 干支月, 干支日, 干支時=[''.join(x) for x in list(zip(gans, zhis))]   #四柱[::3]
    rndrCode([干支年, 干支月, 干支日, 干支時])
    rndrCode(['干支年=', getGZ(干支年)])
    jds=siZhu2Year(getGZ(干支年), getGZ(干支月), getGZ(干支日), GZ(5, 5), 2003, 2029)    #getGZ(干支時), options.year, options.month, options.day, options.time, options.start, options.end
    rndrCode(['jds=', jds])
    for jd in jds:
      t = JD2DD(jd )
      rndrCode("可能出生時間: python bazi.py -g %d %d %d %d :%d:%d"%(t.Y, t.M, t.D, t.h, t.m, round(t.s)))   

elif menu==MENU[1]: #ydata-profiling
  if 陽農=='陽曆':
    年, 月, 日=年月日.year, 年月日.month, 年月日.day
    時=curDT.hour
    rndrCode([年, 月, 日, curDT.time()])
    solar = Solar.fromYmdHms(年, 月, 日, 時, 0, 0)   #int(options.year), int(options.month), int(options.day), int(options.time), curDT.now
    lunar = solar.getLunar()
  else:
    month_ = int(options.month)*-1 if options.r else int(options.month)
    lunar = Lunar.fromYmdHms(int(options.year), month_, int(options.day),int(options.time), 0, 0)
    solar = lunar.getSolar()
  day = lunar
  ba = lunar.getEightChar()
  gans = Gans(year=ba.getYearGan(), month=ba.getMonthGan(), day=ba.getDayGan(), time=ba.getTimeGan())
  zhis = Zhis(year=ba.getYearZhi(), month=ba.getMonthZhi(), day=ba.getDayZhi(), time=ba.getTimeZhi())
  rtrv八字(solar, ba, lunar, gans, zhis, 方向)
