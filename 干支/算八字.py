from ganzhi import ten_deities, zhi5, gan5, Gan, Zhi, zhi_3hes, temps, zhi5_list, relations, zhi_wuhangs, gan_hes, gong_he, zhi_hes, zhi_huis, kus, wuhangs, zhi3, gan_desc, zhi_desc
from datas import siling, zhi_atts, wangs, nayins, jieshas, year_shens, month_shens, day_shens, g_shens, tiaohous, jinbuhuan, jins, ges, emptie4s, shens_infos, minggongs, rizhus, empties, jianchus, jianlus, tianyis, yutangs, self_zuo, lu_types, wenxing
from stUtil import rndrCode
from common import yinyang, check_gan, get_empty, yinyangs, check_gong, gong_hui
from bidict import bidict
from yue import months
from sizi import summarys
from datetime import datetime, date
#from luohou import gans

def get_shens(gans, zhis, gan_, zhi_, me):
    all_shens = []
    for item in year_shens:
        if zhi_ in year_shens[item][zhis.year]:    
            all_shens.append(item)
    for item in month_shens:
        if gan_ in month_shens[item][zhis.month] or zhi_ in month_shens[item][zhis.month]:     
            all_shens.append(item)
    for item in day_shens:
        if zhi_ in day_shens[item][zhis.day]:     
            all_shens.append(item)
    for item in g_shens:
        if zhi_ in g_shens[item][me]:    
            all_shens.append(item) 
    if all_shens:  
        return "  神:" + ' '.join(all_shens)
    else:
        return ""

def is_ku(zhi):
  return True if zhi in "辰戌丑未" else False

def zhi_ku(zhi, items):
  return True if is_ku(zhi) and min(zhi5[zhi], key=zhi5[zhi].get) in items else False

def is_yang(me):
    return True if Gan.index(me) % 2 == 0 else False

def gan_ke(gan1, gan2):
  return True if ten_deities[gan1]['克'] == ten_deities[gan2]['本'] or ten_deities[gan2]['克'] == ten_deities[gan1]['本'] else False

def get_gong(zhis, gans):
    result = []
    for i in range(3):
        if  gans[i] != gans[i+1]:
            continue
        zhi1 = zhis[i]
        zhi2 = zhis[i+1]
        if abs(Zhi.index(zhi1) - Zhi.index(zhi2)) == 2:
            value = Zhi[(Zhi.index(zhi1) + Zhi.index(zhi2))//2]
            #if value in ("丑", "辰", "未", "戌"):
            result.append(value)
        if (zhi1 + zhi2 in gong_he) and (gong_he[zhi1 + zhi2] not in zhis):
            result.append(gong_he[zhi1 + zhi2])

        #if (zhi1 + zhi2 in gong_hui) and (gong_hui[zhi1 + zhi2] not in zhis):
            #result.append(gong_hui[zhi1 + zhi2])

    return result

def not_yang(me):
    return False if Gan.index(me) % 2 == 0 else True

def get_gen(gan, zhis):
    zhus = []
    zhongs = []
    weis = []
    result = ""
    for item in zhis:
        zhu = zhi5_list[item][0]
        if ten_deities[gan]['本'] == ten_deities[zhu]['本']:
            zhus.append(item)

    for item in zhis:
        if len(zhi5_list[item]) ==1:
            continue
        zhong = zhi5_list[item][1]
        if ten_deities[gan]['本'] == ten_deities[zhong]['本']:
            zhongs.append(item)

    for item in zhis:
        if len(zhi5_list[item]) < 3:
            continue
        zhong = zhi5_list[item][2]
        if ten_deities[gan]['本'] == ten_deities[zhong]['本']:
            weis.append(item)

    if not (zhus or zhongs or weis):
        return "無根"
    else:
        result = result + "強：{}{}".format(''.join(zhus), chr(12288)) if zhus else result
        result = result + "中：{}{}".format(''.join(zhongs), chr(12288)) if zhongs else result
        result = result + "弱：{}".format(''.join(weis)) if weis else result
        return result


def gan_zhi_he(zhu):
    gan, zhi = zhu
    if ten_deities[gan]['合'] in zhi5[zhi]:
        return "|"
    return ""

def rtrv八字(solar, ba, lunar, gans, zhis, 方向):
  me = gans.day
  month = zhis.month
  alls = list(gans) + list(zhis)
  zhus = [item for item in zip(gans, zhis)]

  gan_shens = []
  for seq, item in enumerate(gans):
    gan_shens.append('--') if seq == 2 else gan_shens.append(ten_deities[me][item])
  #rndrCode(gan_shens)

  zhi_shens = [] # 地支的主氣神
  for item in zhis:
      d = zhi5[item]
      zhi_shens.append(ten_deities[me][max(d, key=d.get)])
  #rndrCode(zhi_shens)
  shens = gan_shens + zhi_shens

  zhi_shens2 = [] # 地支的所有神，包含余氣和尾氣, 混合在一起
  zhi_shen3 = [] # 地支所有神，字符串格式
  for item in zhis:
      d = zhi5[item]
      tmp = ''
      for item2 in d:
          zhi_shens2.append(ten_deities[me][item2])
          tmp += ten_deities[me][item2]
      zhi_shen3.append(tmp)
  shens2 = gan_shens + zhi_shens2

  # 計算五行分數 http://www.131.com.tw/word/b3_2_14.htm

  scores = {"金":0, "木":0, "水":0, "火":0, "土":0}
  gan_scores = {"甲":0, "乙":0, "丙":0, "丁":0, "戊":0, "己":0, "庚":0, "辛":0, "壬":0, "癸":0}
  for item in gans:
      scores[gan5[item]] += 5
      gan_scores[item] += 5

  for item in list(zhis) + [zhis.month]:
      for gan in zhi5[item]:
          scores[gan5[gan]] += zhi5[item][gan]
          gan_scores[gan] += zhi5[item][gan]

  # 計算八字強弱
  # 子平真诠的計算
  weak = True
  me_status = []
  for item in zhis:
      me_status.append(ten_deities[me][item])
      if ten_deities[me][item] in ('長', '帝', '建'):
          weak = False

  if weak:
      if shens.count('比') + me_status.count('庫') >2:
          weak = False

  # 計算大運
  seq = Gan.index(gans.year)
  if 方向:
      direction = -1 if not seq % 2  else  1
  else:
      direction = 1 if not seq % 2 else -1

  dayuns = []
  gan_seq = Gan.index(gans.month)
  zhi_seq = Zhi.index(zhis.month)
  for i in range(12):
      gan_seq += direction
      zhi_seq += direction
      dayuns.append(Gan[gan_seq%10] + Zhi[zhi_seq%12])

  # 網上的計算
  me_attrs_ = ten_deities[me].inverse
  strong = gan_scores[me_attrs_['比']] + gan_scores[me_attrs_['劫']] \
      + gan_scores[me_attrs_['枭']] + gan_scores[me_attrs_['印']]


  if not None: #options.b
      #rndrCode("direction",direction)
      sex = '女' if 方向 else '男'   #性別默認為男
      rndrCode(f"""{sex}命 公歷 {solar.getYear()}年{solar.getMonth()}月{solar.getDay()}日""")
      yun = ba.getYun(not 方向)
      rndrCode(f"""農歷 {lunar.getYear()}年{lunar.getMonth()}月{lunar.getDay()}日 穿=害 上運時間：{yun.getStartSolar().toFullString().split()[0]} 命宮:{ba.getMingGong()} 胎元:{ba.getTaiYuan()}""")
      rndrCode(["\t", siling[zhis.month], lunar.getPrevJieQi(True), lunar.getPrevJieQi(True).getSolar().toYmdHms(),lunar.getNextJieQi(True), lunar.getNextJieQi(True).getSolar().toYmdHms()])

  rndrCode("-"*120)

  #rndrCode(zhi_3hes, "生：寅申巳亥 敗：子午卯酉　庫：辰戌丑未")
  #rndrCode("地支六合:", zhi_6hes)
  out = ''
  for item in zhi_3hes:
      out = out + "{}:{}  ".format(item, zhi_3hes[item])
  rndrCode(['\033[1;36;40m' + ' '.join(list(gans)), ' '*5, ' '.join(list(gan_shens)) + '\033[0m',' '*5, out])
  out = ''

  rndrCode(['\033[1;36;40m' + ' '.join(list(zhis)), ' '*5, ' '.join(list(zhi_shens)) + '\033[0m', ' '*5, out, "解讀:釘ding或v信pythontesting"])
  rndrCode("-"*120)
  rndrCode(["{1:{0}^15s}{2:{0}^15s}{3:{0}^15s}{4:{0}^15s}".format(chr(12288), '【年】{}:{}{}{}'.format(temps[gans.year],temps[zhis.year],ten_deities[gans.year].inverse['建'], gan_zhi_he(zhus[0])), '【月】{}:{}{}{}'.format(temps[gans.month],temps[zhis.month], ten_deities[gans.month].inverse['建'], gan_zhi_he(zhus[1])), '【日】{}:{}{}'.format(temps[me], temps[zhis.day], gan_zhi_he(zhus[2])), '【時】{}:{}{}{}'.format(temps[gans.time], temps[zhis.time], ten_deities[gans.time].inverse['建'], gan_zhi_he(zhus[3])))])
  rndrCode("-"*120)


  rndrCode("\033[1;36;40m{1:{0}<15s}{2:{0}<15s}{3:{0}<15s}{4:{0}<15s}\033[0m".format(
      chr(12288),
      '{}{}{}【{}】{}'.format(gans.year, yinyang(gans.year), gan5[gans.year], ten_deities[me][gans.year], check_gan(gans.year, gans)),
      '{}{}{}【{}】{}'.format(gans.month, yinyang(gans.month), gan5[gans.month], ten_deities[me][gans.month], check_gan(gans.month, gans)),
      '{}{}{}{}'.format(me, yinyang(me),gan5[me], check_gan(me, gans)),
      '{}{}{}【{}】{}'.format(gans.time, yinyang(gans.time), gan5[gans.time], ten_deities[me][gans.time], check_gan(gans.time, gans)),
  ))

  rndrCode("\033[1;36;40m{1:{0}<15s}{2:{0}<15s}{3:{0}<15s}{4:{0}<15s}\033[0m".format(
      chr(12288),
      "{}{}{}【{}】{}".format(
          zhis.year, yinyang(zhis.year), ten_deities[me][zhis.year],
          ten_deities[gans.year][zhis.year], get_empty(zhus[2],zhis.year)),
      "{}{}{}【{}】{}".format(
          zhis.month, yinyang(zhis.month), ten_deities[me][zhis.month],
          ten_deities[gans.month][zhis.month], get_empty(zhus[2],zhis.month)),
      "{}{}{}".format(zhis.day, yinyang(zhis.day), ten_deities[me][zhis.day]),
      "{}{}{}【{}】{}".format(
          zhis.time, yinyang(zhis.time), ten_deities[me][zhis.time],
          ten_deities[gans.time][zhis.time], get_empty(zhus[2],zhis.time)),
  ))

  statuses = [ten_deities[me][item] for item in zhis]


  for seq, item in enumerate(zhis):
      out = ''
      multi = 2 if item == zhis.month and seq == 1 else 1

      for gan in zhi5[item]:
          out = out + "{}{}{}　".format(gan, gan5[gan], ten_deities[me][gan])
      rndrCode(["\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), out.rstrip('　'))])

  # 輸出地支關系
  for seq, item in enumerate(zhis):

      output = ''
      others = zhis[:seq] + zhis[seq+1:]
      for type_ in zhi_atts[item]:
          flag = False
          if type_ in ('害',"破","會",'刑'):
              continue
          for zhi in zhi_atts[item][type_]:
              if zhi in others:
                  if not flag:
                      output = output + "　" + type_ + "：" if type_ not in ('衝','暗') else output + "　" + type_
                      flag = True
                  if type_ not in ('衝','暗'):
                      output += zhi
          output = output.lstrip('　')
      rndrCode(["\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), output)])

  # 輸出地支minor關系
  for seq, item in enumerate(zhis):

      output = ''
      others = zhis[:seq] + zhis[seq+1:]
      for type_ in zhi_atts[item]:
          flag = False
          if type_ not in ('害',"會"):
              continue
          for zhi in zhi_atts[item][type_]:
              if zhi in others:
                  if not flag:
                      output = output + "　" + type_ + "："
                      flag = True
                  output += zhi
      output = output.lstrip('　')
      rndrCode(["\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), output)])

  # 輸出根
  for  item in gans:
      output = output.lstrip('　')
      rndrCode(["\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), get_gen(item, zhis))])

  for seq, item in enumerate(zhus):

      # 檢查空亡
      result = "{}－{}".format(nayins[item], '亡') if zhis[seq] == wangs[zhis[0]] else nayins[item]

      # 天干與地支關系
      result = relations[(gan5[gans[seq]], zhi_wuhangs[zhis[seq]])] + result

      # 檢查劫殺
      result = "{}－{}".format(result, '劫殺') if zhis[seq] == jieshas[zhis[0]] else result
      # 檢查元辰
      result = "{}－{}".format(result, '元辰') if zhis[seq] == Zhi[(Zhi.index(zhis[0]) + direction*-1*5)%12] else result
      rndrCode(["{1:{0}<15s} ".format(chr(12288), result)])

  all_ges = []

  # 神煞計算

  strs = ['','','','',]

  all_shens = set()
  all_shens_list = []

  for item in year_shens:
      for i in (1,2,3):
          if zhis[i] in year_shens[item][zhis.year]:
              strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
              all_shens.add(item)
              all_shens_list.append(item)

  for item in month_shens:
      for i in range(4):
          if gans[i] in month_shens[item][zhis.month] or zhis[i] in month_shens[item][zhis.month]:
              strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
              if i == 2 and gans[i] in month_shens[item][zhis.month]:
                  strs[i] = strs[i] + "●"
              all_shens.add(item)
              all_shens_list.append(item)

  for item in day_shens:
      for i in (0,1,3):
          if zhis[i] in day_shens[item][zhis.day]:
              strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
              all_shens.add(item)
              all_shens_list.append(item)

  for item in g_shens:
      for i in range(4):
          if zhis[i] in g_shens[item][me]:
              strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
              all_shens.add(item)
              all_shens_list.append(item)

  # rndrCode(all_shens_list)
  #rndrCode(strs)
  for seq in range(2):
    rndrCode(["{1:{0}<15s} ".format(chr(12288), strs[seq])])
  for seq in range(2,4):
    rndrCode(["{1:{0}<14s} ".format(chr(12288), strs[seq])])

  # 計算六合:相鄰的才算合
  zhi_6he = [False, False, False, False]

  for i in range(3):
      if zhi_atts[zhis[i]]['六'] == zhis[i+1]:
          zhi_6he[i] = zhi_6he[i+1] = True

  # 計算六衝:相鄰的才算合

  zhi_6chong = [False, False, False, False]

  for i in range(3):
      if zhi_atts[zhis[i]]['冲'] == zhis[i+1]:
          zhi_6chong[i] = zhi_6chong[i+1] = True

  # 計算干合:相鄰的才算合

  gan_he = [False, False, False, False]
  for i in range(3):
      if (gans[i],gans[i+1]) in set(gan_hes) or (gans[i+1],gans[i]) in set(gan_hes):
          gan_he[i] = gan_he[i+1] = True

  # 計算刑:相鄰的才算

  zhi_xing = [False, False, False, False]

  for i in range(3):
      if zhi_atts[zhis[i]]['刑'] == zhis[i+1] or zhi_atts[zhis[i+1]]['刑'] == zhis[i]:
          zhi_xing[i] = zhi_xing[i+1] = True
  rndrCode("-"*120)
  rndrCode("大運：")

  for item in dayuns:
      rndrCode(item)
  # for item in gans:
  #     rndrCode(get_gen(item, zhis))
  # rndrCode()
  rndrCode("-"*120)

  me_lu = ten_deities[me].inverse['建']

  me_jue = ten_deities[me].inverse['絕']
  me_tai = ten_deities[me].inverse['胎']
  me_di = ten_deities[me].inverse['帝']
  shang = ten_deities[me].inverse['傷']
  shang_lu = ten_deities[shang].inverse['建']
  shang_di = ten_deities[shang].inverse['帝']
  yin = ten_deities[me].inverse['印']
  yin_lu = ten_deities[yin].inverse['建']
  xiao = ten_deities[me].inverse['枭']
  xiao_lu = ten_deities[xiao].inverse['建']
  cai = ten_deities[me].inverse['財']
  cai_lu = ten_deities[cai].inverse['建']
  cai_di = ten_deities[cai].inverse['帝']
  piancai = ten_deities[me].inverse['才']
  piancai_lu = ten_deities[piancai].inverse['建']
  piancai_di = ten_deities[piancai].inverse['帝']
  guan = ten_deities[me].inverse['官']
  guan_lu = ten_deities[guan].inverse['建']
  guan_di = ten_deities[guan].inverse['帝']
  sha = ten_deities[me].inverse['殺']
  sha_lu = ten_deities[sha].inverse['建']
  sha_di = ten_deities[sha].inverse['帝']

  jie = ten_deities[me].inverse['劫']
  shi = ten_deities[me].inverse['食']
  shi_lu = ten_deities[shi].inverse['建']
  shi_di = ten_deities[shi].inverse['帝']

  me_ku = ten_deities[me]['庫'][0]
  cai_ku = ten_deities[cai]['庫'][0]
  guan_ku = ten_deities[guan]['庫'][0]
  yin_ku = ten_deities[yin]['庫'][0]
  shi_ku = ten_deities[shi]['庫'][0]



  rndrCode(["調候：", tiaohous['{}{}'.format(me, zhis[1])], "\t##金不換大運：", jinbuhuan['{}{}'.format(me, zhis[1])]])
  rndrCode(["金不換大運：說明：", jins[me]])
  rndrCode(["格局選用：", ges[ten_deities[me]['本']][zhis[1]]])
  if len(set('寅申巳亥')&set(zhis)) == 0:
      rndrCode("缺四生：一生不敢作爲")
  if len(set('子午卯酉')&set(zhis)) == 0:
      rndrCode("缺四柱地支缺四正，一生避是非")
  if len(set('辰戌丑未')&set(zhis)) == 0:
      rndrCode("四柱地支缺四庫，一生沒有潛伏性兇災。")
  if ( '甲', '戊', '庚',) in (tuple(gans)[:3], tuple(gans)[1:]):
      rndrCode("地上三奇：白天生有申佳，需身強四柱有貴人。")
  if ( '辛', '壬', '癸',) in (tuple(gans)[:3], tuple(gans)[1:]):
      rndrCode("人間三奇，需身強四柱有貴人。")
  if ( '乙', '丙', '丁',) in (tuple(gans)[:3], tuple(gans)[1:]):
      rndrCode("天上三奇：晚上生有亥佳，需身強四柱有貴人。")

  if zhi_shens2.count('亡神') > 1:
      rndrCode("二重亡神，先喪母；")

  if get_empty(zhus[2],zhis.time):
      rndrCode("時坐空亡，子息少。 母法P24-41 母法P79-4：損破祖業，後另再成就。")

  if zhis.count(me_jue) + zhis.count(me_tai) > 2:
      rndrCode("胎絕超過3個：夭或窮。母法P24-44 丁未 壬子 丙子 戊子")

  if not_yang(me) and zhi_ku(zhis[2], (me,jie)) and zhi_ku(zhis[3], (me,jie)):
      rndrCode("陰日主時日支入比劫庫：性格孤獨，難發達。母法P28-112 甲申 辛未 辛丑 己丑 母法P55-11 爲人孤獨，且有災疾")

  #rndrCode(cai_lu, piancai_lu)
  if zhis[1:].count(piancai_lu) + zhis[1:].count(cai_lu) + zhis[1:].count(piancai_di) + zhis[1:].count(cai_di) == 0:
      rndrCode("月日時支沒有財或偏財的祿旺。")

  if zhis[1:].count(guan_lu) + zhis[1:].count(guan_di) == 0:
      rndrCode("月日時支沒有官的祿旺。")

  if '辰' in zhis and ('戌' not in zhis) and 方向:
      rndrCode("女命有辰無戌：孤。")
  if '戌' in zhis and ('辰' not in zhis) and 方向:
      rndrCode("女命有戌無辰：帶祿。")

  if emptie4s.get(zhus[2], 0) != 0:
      if scores[emptie4s.get(zhus[2], 0)] == 0:
          rndrCode("四大空亡：33歲以前身體不佳！")

  for item in all_shens:
    rndrCode([item, ":",  shens_infos[item]])
  if 方向:
    rndrCode(["#"*20, "女命"])
    if all_shens_list.count("驿馬") > 1:
      rndrCode("二逢驿馬，母家荒涼。P110 丙申 丙申 甲寅 丁卯")
    if gan_shens[0] == '傷':
      rndrCode("年上傷官：帶疾生產。P110 戊寅 戊午 丁未 丁未")
  rndrCode("-"*120)

  children = ['食','傷'] if 方向 else ['官','殺']

  liuqins = bidict({'才': '父親',"財":'財' if 方向 else '妻', "印": '母親', "枭": '偏印' if 方向 else '祖父',
                    "官":'丈夫' if 方向 else '女兒', "殺":'情夫' if 方向 else '兒子', "劫":'兄弟' if 方向 else '姐妹', "比":'姐妹' if 方向 else '兄弟',
                    "食":'女兒' if 方向 else '下屬', "傷":'兒子' if 方向 else '孫女'})

  # 六親分析
  for item in Gan:
    rndrCode(["{}:{} {}-{} {} {} {}".format(item, ten_deities[me][item], liuqins[ten_deities[me][item]],  ten_deities[item][zhis[0]] ,ten_deities[item][zhis[1]], ten_deities[item][zhis[2]], ten_deities[item][zhis[3]])])
    if Gan.index(item) == 4: pass

  # 計算上運時間，有年份時才適用
  temps_scores = temps[gans.year] + temps[gans.month] + temps[me] + temps[gans.time] + temps[zhis.year] + temps[zhis.month]*2 + temps[zhis.day] + temps[zhis.time]
  rndrCode(["\033[1;36;40m五行分數", scores, '  八字強弱：', strong, "通常>29爲強，需要參考月份、坐支等", "weak:", weak])

  gongs = get_gong(zhis, gans)
  zhis_g = set(zhis) | set(gongs)

  jus = []
  for item in zhi_hes:
      if set(item).issubset(zhis_g):
          rndrCode("三合局", item)
          jus.append(ju[ten_deities[me].inverse[zhi_hes[item]]])


  for item in zhi_huis:
      if set(item).issubset(zhis_g):
          rndrCode("三會局", item)
          jus.append(ju[ten_deities[me].inverse[zhi_huis[item]]])

  rndrCode(["濕度分數", temps_scores,"正爲暖燥，負爲寒濕，正常區間[-6,6] 拱：", get_gong(zhis, gans)])
  for item in gan_scores:
      rndrCode("{}[{}]-{} ".format(item, ten_deities[me][item], gan_scores[item]))
  rndrCode("-"*120)
  yinyangs(zhis)
  shen_zhus = list(zip(gan_shens, zhi_shens))

  minggong = Zhi[::-1][(Zhi.index(zhis[1]) + Zhi.index(zhis[3]) -6  )%12 ]
  rndrCode([minggong, minggongs[minggong]])
  rndrCode(["坐：", rizhus[me+zhis.day]])



  # 地網
  if '辰' in zhis and '巳' in zhis:
      rndrCode("地網：地支辰巳。天羅：戌亥。天羅地網全兇。")

  # 天羅
  if '戌' in zhis and '亥' in zhis:
      rndrCode("天羅：戌亥。地網：地支辰巳。天羅地網全兇。")

  # 魁罡格
  if zhus[2] in (('庚','辰'), ('庚','戌'),('壬','辰'), ('戊','戌'),):
      rndrCode("魁罡格：基礎96，日主庚辰,庚戌,壬辰, 戊戌，重叠方有力。日主強，無刑衝佳。")
      rndrCode("魁罡四柱曰多同，貴氣朝來在此中，日主獨逢衝克重，財官顯露禍無窮。魁罡重叠是貴人，天元健旺喜臨身，財官一見生災禍，刑煞俱全定苦辛。")

  # 金神格
  if zhus[3] in (('乙','丑'), ('己','巳'),('癸','酉')):
      rndrCode("金神格：基礎97，時柱乙丑、己巳、癸酉。只有甲和己日，甲日爲主，甲子、甲辰最突出。月支通金火2局爲佳命。不通可以選其他格")

  # 六陰朝陽
  if me == '辛' and zhis.time == '子':
      rndrCode("六陰朝陽格：基礎98，辛日時辰爲子。")

  # 六乙鼠貴
  if me == '乙' and zhis.time == '子':
      rndrCode("六陰朝陽格：基礎99，乙日時辰爲子。忌諱午衝，丑合，不適合有2個子。月支最好通木局，水也可以，不適合金火。申酉大運有兇，午也不行。夏季爲傷官。入其他格以格局論。")

  # 從格
  if max(scores.values()) > 25:
      rndrCode("有五行大于25分，需要考慮專格或者從格。")
      rndrCode("從旺格：安居遠害、退身避位、淡泊名利,基礎94;從勢格：日主無根。")


  if zhi_6he[3]:
      if abs(Gan.index(gans[3]) - Gan.index(gans[2])) == 1:
          rndrCode("日時干鄰支合：連珠得合：妻賢子佳，與事業無關。母法總則P21-11")

  for i,item in enumerate(zhis):
      if item == me_ku:
          if gan_shens[i] in ('才','財'):
              rndrCode("財坐劫庫，大破敗。母法P61-4 戊寅 丙辰 壬辰 庚子")

  #rndrCode(zhi_6chong[3], gans, me)
  if zhi_6chong[3] and  gans[3] == me:
      rndrCode("日時天比地衝：女爲家庭辛勞，男藝術宗教。 母法P61-5 己丑 丙寅 甲辰 甲戌")

  #rndrCode(zhi_6chong[3], gans, me)
  if zhi_xing[3] and  gan_ke(me, gans[3]):
      rndrCode("日時天克地刑：破敗祖業、自立發展、後無終局。 母法P61-7 己丑 丙寅 甲午 庚午")

  if (cai,yin_lu) in zhus and (cai not in zhi_shens2):
      rndrCode("浮財坐印祿:破祖之後，自己也敗。 母法P78-29 辛丑 丁酉 壬寅 庚子")


  for i in range(3):
      if is_yang(me):
          break
      if zhi_xing[i] and zhi_xing[i+1] and gan_ke(gans[i], gans[i+1]):
          rndrCode("陰日主天克地刑：孤獨、雙妻。 母法P61-7 己丑 丙寅 甲午 庚午")


  # 建祿格
  if zhi_shens[1] == '比':
      all_ges.append('建')
      rndrCode("建祿格：最好天干有財官。如果官殺不成格，有兄弟，且任性。有爭財和理財的雙重性格。如果創業獨自搞比較好，如果合伙有完善的財務制度也可以。")
      if gan_shens[0] in '比劫':
          rndrCode("\t建祿年透比劫兇")
      elif '財' in gan_shens and '官' in gan_shens:
          rndrCode("\t建祿財官雙透，吉")
      if me in ('甲','乙'):
          rndrCode("\t甲乙建祿四柱劫財多，無祖財，克妻，一生不聚財，做事虛詐，爲人大模大樣，不踏實。乙財官多可爲吉。甲壬申時佳；乙辛巳時佳；")

      if me in ('丙'):
          rndrCode("\t丙：己亥時辰佳；")
      if me in ('丁'):
          rndrCode("\t丁：陰男克1妻，陽男克3妻。財官多可爲吉。庚子時辰佳；")
      if me in ('戊'):
          rndrCode("\t戊：四柱無財克妻，無祖業，後代多事端。如合申子辰，子息晚，有2子。甲寅時辰佳；")
      if me in ('己'):
          rndrCode("\t己：即使官財出干成格，妻也晚。偏財、殺印成格爲佳。乙丑時辰佳；")
      if me in ('庚'):
          rndrCode("\t庚：上半月生難有祖財，下半月較好，財格比官殺要好。丙戌時辰佳；")
      if me in ('辛'):
          rndrCode("\t辛：干透劫財，妻遲財少；丁酉時辰佳；")
      if me in ('壬'):
          rndrCode("\t 壬：戊申時辰佳；")
      if me in ('癸'):
          rndrCode("\t 癸：己亥時辰佳")



  # 甲分析

  if me == '甲':
      if zhis.count('辰') > 1 or zhis.count('戌') > 1:
          rndrCode("甲日：辰或戌多、性能急躁不能忍。")
      if zhis[2] == '子':
          rndrCode("甲子：調候要火。")
      if zhis[2] == '寅':
          rndrCode("甲寅：有主見之人，需要財官旺支。")
      if zhis[2] == '辰':
          rndrCode("甲辰：印庫、性柔和而有實權。")
      if zhis[2] == '午':
          rndrCode("甲午：一生有財、調候要水。")
      if zhis[2] == '戌':
          rndrCode("甲戌：自坐傷官，不易生財，爲人仁善。")

  if me in ('庚', '辛') and zhis[1] == '子' and zhis.count('子') >1:
      rndrCode("冬金子月，再有一子字，孤克。 母法P28-106 甲戌 丙子 庚子 丁丑")


  # 比肩分析
  if '比' in gan_shens:
      rndrCode("比：同性相斥。討厭自己。老是想之前有沒有搞錯。沒有持久性，最多跟你三五年。 散財，月上比肩，做事沒有定性，不看重錢，感情不持久。不懷疑人家，人心很好。善意好心惹麻煩。年上問題不大。")

      if gan_shens[0] == '比' and gan_shens[1] == '比':
          rndrCode("比肩年月天干并現：不是老大，出身平常。女儀容端莊，有自己的思想；不重視錢財,話多不能守秘。30隨以前是非小人不斷。")

      if gan_shens[1] == '比' and '比' in zhi_shen3[1]:
          rndrCode("月柱干支比肩：爭夫感情豐富。30歲以前錢不夠花。")

      if gan_shens[0] == '比':
          rndrCode("年干比：上面有哥或姐，出身一般。")

      if zhi_shens[2] == '比':
          rndrCode("基52女坐比透比:夫妻互恨 丙辰 辛卯 辛酉 甲午。")


      if gan_shens.count('比') > 1:
          rndrCode("""----基51:天干2比
          自我排斥，易後悔、舉棋不定、匆促決定而有失；男傾向于群力，自己決策容易孤注一擲，小事謹慎，大事決定後不再重復考慮。
          女有自己的思想、容貌佳，注意細節，喜歡小孩重過丈夫。輕視老公。對丈夫多疑心，容易吃醋衝動。
          男不得女歡心.
          難以保守秘密，不適合多言；
          地支有根，一生小是非不斷。沒官殺制，無耐心。 END""")


      # 比肩過多
      if shens2.count('比') > 2 and '比' in zhi_shens:
          #rndrCode(shens2, zhi_shens2)
          rndrCode('''----比肩過多基51：
          女的愛子女超過丈夫；輕易否定丈夫。 換一種說法：有理想、自信、貪財、不懼內。男的雙妻。
          兄弟之間缺乏幫助。夫妻有時不太和諧。好友知交相處不會很久。
          即使成好格局，也是勞累命，事必躬親。除非有官殺制服。感情煩心。
          基53：善意多言，引無畏之爭；難以保守秘密，不適合多言；易犯無事忙的自我表現；不好意思拒絕他人;累積情緒而突然放棄。
          比肩過多，女：你有幫夫運，多協助他的事業，多提意見，偶爾有爭執，問題也不大。女：感情啰嗦
          對人警惕性低，樂天知命;情感過程多有波折
          ''')

          if (not '官' in shens) and  (not '殺' in shens):
              rndrCode("基51: 比肩多，四柱無正官七殺，性情急躁。")


          if '劫' in gan_shens:
              rndrCode("天干比劫并立，比肩地支專位，女命感情豐富，多遇爭夫。基52")

          if gan_shens[0] == '比':
              rndrCode("年干爲比，不是長子，父母緣較薄，晚婚。")

          if gan_shens[3] == '比':
              rndrCode("母法總則P21-6：時干爲比，如日時地支衝，男的對妻子不利，女的爲夫辛勞，九流藝術、宗教則關系不大。")

          if gan_shens[1] == '比':
              if zhi_shens[1] == '食':
                  rndrCode("月柱比坐食，易得貴人相助。")
              if zhi_shens[1] == '傷':
                  rndrCode("月柱比坐傷，一生只有小財氣，難富貴。")
              if zhi_shens[1] == '比':
                  rndrCode("月柱比坐比，單親家庭，一婚不能到頭。地支三合或三會比，天干2比也如此。")
              if zhi_shens[1] == '財':
                  rndrCode("月柱比坐財，不利妻，也主父母身體不佳。因親友、人情等招財物的無謂損失。")
              if zhi_shens[1] == '殺':
                  rndrCode("月柱比坐殺，穩重。")


      for seq, gan_ in enumerate(gan_shens):
          if gan_ != '比':
              continue
          if zhis[seq] in  empties[zhus[2]]:
              rndrCode("基51:比肩坐空亡，不利父親與妻。年不利父，月不利父和妻，在時則沒有關系。甲戌 丙寅 甲子 己巳\n\t基52女：夫妻緣分偏薄，在年只是不利父，在月30歲以前夫妻緣薄 E")
          if zhi_shens[seq] == '比':
              rndrCode("比坐比-平吉：與官殺對立，無主權。養子：克偏財，泄正印。吉：爲朋友盡力；兇：受兄弟朋友拖累。父緣分薄，自我孤僻，男多遲婚")
          if zhi_shens[seq] == '劫':
              rndrCode("女比肩坐劫:夫妻互恨，基52丁丑 壬子 壬戌 壬寅。\n\t還有刑衝且爲羊刃，女恐有不測之災：比如車禍、開刀和意外等。基52丙午 庚子 丙戌 丙申")
              rndrCode("比坐劫-大兇：爲忌親友受損，合作事業中途解散，與妻子不合。如年月3見比，父緣薄或已死別。")
              if ten_deities[gans[seq]][zhis[seq]] == '絕' and seq < 2:
                  rndrCode("比肩坐絕，兄弟不多，或者很難謀面。戊己和壬癸的準确率偏低些。")
          if zhi_shens[seq] == '財':
              rndrCode("比肩坐財：因親人、人情等原因引起無謂損失。")
          if zhi_shens[seq] == '殺':
              rndrCode("比肩坐殺:穩重。")
          if zhi_shens[seq] == '枭':
              rndrCode("比肩坐偏印：三五年發達，後面守成。")
          if zhi_shens[seq] == '劫' and Gan.index(me) % 2 == 0:
              rndrCode("比肩坐陽刃：父親先亡，基于在哪柱判斷時間。基51：丙午 丙申 丙申 丁酉。E在年不利父，在其他有刀傷、車禍、意外災害。\t基52女命年克父親，月若30歲以前結婚不利婚姻")
          if zhi_shens[seq] in ('劫','比') and'劫' in gan_shens:
              rndrCode("天干比劫并立，比肩又坐比劫，女多遇爭夫，個性強，不易協調。")
          if  zhi_xing[seq]:
              rndrCode("比肩坐刑(注意不是半刑)，幼年艱苦，白手自立長。 甲申 己巳 甲寅 庚午 基51")
              if zhi_shens[seq] == '劫':
                  rndrCode("比肩坐刑劫,兄弟不合、也可能與妻子分居。")
          if zhi_6chong[seq]:
              rndrCode("比肩衝，手足不和，基于柱定時間 甲申 己巳 甲寅 庚午 基51。女命忌諱比劫和合官殺，多爲任性引發困難之事。")

  if zhi_shens[2] == '比':
      rndrCode("日支比：1-39對家務事有家長式領導；錢來得不容易且有時有小損財。e 自我，如有刑衝，不喜歸家！")
  if zhi_shens[3] == '比':
      rndrCode("時支比：子女爲人公正倔強、行動力強，能得資產。")
  if '比' in (gan_shens[1],zhi_shens[1]):
      rndrCode("月柱比：三十歲以前難有成就。冒進、不穩定。女友不持久、大男子主義。")
  if '比' in (gan_shens[3],zhi_shens[3]):
      rndrCode("時柱比：與親人意見不合。")

  if shens.count('比') + shens.count('劫') > 1:
      rndrCode("比劫大于2，男：感情阻礙、事業起伏不定。")


  # 日坐祿
  if me_lu == zhis[2]:

      if zhis.count(me_lu) > 1:
          if yin_lu in zhis:
              if '比' in gan_shens or '劫' in gan_shens:

                  rndrCode("雙祿帶比印（專旺）、孤克之命。比論孤，劫論兇。母法總則P20-3。比祿印劫不可合見四位")

      if zhi_6he[2] and '比' in gan_shens:
          if yin_lu in zhis:
              rndrCode("透比，坐祿六合，有印專旺：官非、殘疾。六合近似劫財，如地支會印，法死。 母法總則P20-4")

          rndrCode("透比，坐祿六合，如地支會印，法死。 母法總則P20-4")


      if (zhi_xing[3] and gan_he[3] and gan_shens[3] == '財') or (zhi_xing[2] and gan_he[2] and zhi_xing[1] and gan_he[1] and gan_shens[1] == '財'):

          rndrCode("日祿與正財干合支刑：克妻子，即便是吉命，也無天倫之樂。 母法總則P22-21")

  if zhis.count(me_lu) > 2:
      rndrCode("祿有三，孤。 母法總則P23-36")


  if zhis[3] == me_ku:
      if '財' in gan_shens or '才' in gan_shens:
          rndrCode("時支日庫，透財：清高、藝術九流。 母法總則P59-5 己未 辛未 丁巳 庚戌 P61-8 丁未 壬寅 癸卯 丙辰")

      if piancai_lu == zhis[2]:
          rndrCode("時支日庫，坐偏財：吉祥近貴，但親屬淡薄。 母法總則P59-6 辛未 辛卯 丁酉 庚戌")




  # 時坐祿
  if me_lu == zhis[3]:
      if '傷' in gan_shens and '傷' in zhi_shens2:
          rndrCode("時祿，傷官格，晚年吉。 母法總則P56-26 己未 丙寅 乙丑 己卯")
      if '殺' == gan_shens[3]:
          rndrCode("殺坐時祿：爲人反復不定。 母法總則P56-28 己未 丙寅 乙丑 己卯")

  # 自坐劫庫
  if  zhis[2] == me_ku:
      if gan_shens[3] == '殺' and '殺' in zhi_shen3[3]:
          rndrCode("自坐劫庫,時殺格，貴！母法總則P30-143 辛未 辛卯 壬辰 戊申 母法總則P55-14 P60-22")

      if gan_shens[3] == '官' and '官' in zhi_shen3[3]:
          rndrCode("自坐劫庫,正官格，孤貴！母法總則P56-24 辛未 辛卯 壬辰 戊申 母法總則P55-14")

      if zhi_ku(zhis[3], (cai,piancai)):
          rndrCode("自坐劫庫,時財庫，另有刃祿孤刑藝術，無者辛勞！母法總則P30-149 母法總則P56-17 56-18")

      if gan_shens[3] == '財' and '財' in zhi_shen3[3]:
          rndrCode("自坐劫庫，時正財格，雙妻，喪妻。 母法總則P55-13 己酉 戊寅 壬辰 丁未 P61-6 乙酉 戊寅 壬辰 丁未")

      if (yin, me_lu) in zhus:
          rndrCode("自坐劫庫,即便吉，也會猝亡 母法總則P61-9 丁丑 甲辰 壬辰 辛亥")


  # 劫財分析
  if '劫' in gan_shens:
      rndrCode("劫財扶助，無微不至。劫財多者謙虛之中帶有傲氣。凡事先理情，而後情理。先細節後全局。性剛強、精明干練、女命不適合干透支藏。")
      rndrCode("務實，不喜歡抽象性的空談。不容易認錯，比較倔。有理想，但是不夠靈活。不怕闲言闲語干擾。不顧及別人面子。")
      rndrCode("合作事業有始無終。太重細節。做小領導還是可以的。有志向，自信。殺或食透干可解所有負面。女命忌諱比劫和合官殺，多爲任性引發困難之事。")

      if gan_shens[0] == '劫' and gan_shens[1] == '劫':
          rndrCode("劫年月天干并現：喜怒形于色，30歲以前大失敗一次。過度自信，精明反被精明誤。")

      if gan_shens[1] == '劫':
          if  '劫' in zhi_shen3[1]:
              rndrCode("月柱干支劫：與父親無緣，30歲以前任性，早婚防分手，自我精神壓力極其重。")
          if  zhis[1] == cai_lu and zhis.count(yin_lu) > 1:
              rndrCode("月干劫：月支財祿，如地支2旺印，旺財不敵，官非、刑名意外。")


      if shens2.count('劫') > 2:
          rndrCode('----劫財過多, 婚姻不好')
      if zhi_shens[2] == '劫':
          rndrCode("日坐劫財，透天干。在年父早亡，在月夫妻關系不好。比如財產互相防範；鄙視對方；自己決定，哪怕對方不同意；老夫少妻；身世有差距；斤斤計較；敢愛敢恨的後遺症\n\t以上多針對女。男的一般有雙妻。天干有殺或食可解。基54丁未 己酉 丙午 己丑")

  if zhus[2] in (('壬','子'),('丙','午'), ('戊','午')):
      rndrCode("日主專位劫財，壬子和丙午，晚婚。不透天干，一般是眼光高、獨立性強。對配偶不利，互相輕視；若刑衝，做事立場不明遭嫉妒，但不會有大災。女性婚後通常還有自己的事業,能辦事。")
  if ('劫','傷') in shen_zhus or ('傷','劫',) in shen_zhus:
          rndrCode("同一柱中，劫財、陽刃傷官都有，外表華美，富屋窮人，婚姻不穩定，富而不久；年柱不利家長，月柱不利婚姻，時柱不利子女。傷官的狂妄。基55丙申 丁酉 甲子 丁卯")

  if gan_shens[0] == '劫':
      rndrCode("年干劫財：家運不濟。克父，如果坐劫財，通常少年失父；反之要看地支劫財根在哪一柱子。")

  if '劫' in (gan_shens[1],zhi_shens[1]):
      rndrCode("月柱劫：容易孤注一擲，30歲以前難穩定。男早婚不利。")
  if '劫' in (gan_shens[3],zhi_shens[3]):
      rndrCode("時柱劫：只要不是去經濟大權還好。")
  if zhi_shens[2] == '劫':
      rndrCode("日支劫：男的克妻，一說是家庭有糾紛，對外尚無重大損失。如再透月或時天干，有嚴重內憂外患。")

  if '劫' in shens2 and  '比' in zhi_shens and '印' in shens2 and not_yang():
      rndrCode("陰干比劫印齊全，單身，可入道！")

  if zhi_shens[0] == '劫' and is_yang():
      rndrCode("年陽刃：得不到長輩福；不知足、施恩反怨。")
  if zhi_shens[3] == '劫' and is_yang():
      rndrCode("時陽刃：與妻子不和，晚無結果，四柱再有比刃，有疾病與外災。")

  # 陽刃格
  if zhi_shens[1] == '劫' and is_yang():
      all_ges.append('刃')
      rndrCode("陽刃格：喜七殺或三四個官。基礎90 甲戊庚逢衝多禍，壬丙逢衝還好。")
      if me in ('庚', '壬','戊'):
          rndrCode("陽刃'庚', '壬','午'忌諱正財運。庚逢辛酉兇，丁酉吉，庚辰和丁酉六合不兇。壬逢壬子兇，戊子吉；壬午和戊子換祿不兇。")
      else:
          rndrCode("陽刃'甲', '丙',忌諱殺運，正財偏財財庫運還好。甲：乙卯兇，辛卯吉；甲申與丁卯暗合吉。丙：丙午兇，壬午吉。丙子和壬午換祿不兇。")

      if zhis.count(yin_lu) > 0 and gan_shens[1] == '劫': # 母法總則P20-1
          rndrCode("陽刃格月干爲劫：如果印祿位有2個，過旺，兇災。不透劫財，有一印祿,食傷泄，仍然可以吉。 母法總則P20-1")

      if gan_shens[3] == '枭' and '枭' in zhi_shen3[3]:

          rndrCode("陽刃格:時柱成偏印格，貧、夭、帶疾。 母法總則P28-107 癸未 辛酉 庚寅 戊寅")


  if zhi_shens.count('劫') > 1 and Gan.index(me) % 2 == 0:
      if zhis.day == yin_lu:
          rndrCode("雙陽刃，自坐印專位：刑妻、妨子。兇終、官非、意外災害。母法總則P21-13")

  if zhi_shens[1:].count('劫') > 0 and Gan.index(me) % 2 == 0:
      if zhis.day == yin_lu and ('劫' in gan_shens or '比' in gan_shens):
          rndrCode("陽刃，自坐印專位，透比或劫：刑妻。母法總則P36-8 己酉 丁卯 甲子 乙亥")

  if zhis[2] in (me_lu,me_di) and zhis[3] in (me_lu,me_di):
      rndrCode("日時祿刃全，如沒有官殺制，刑傷父母，妨礙妻子。母法總則P30-151 丁酉 癸卯 壬子 辛亥 母法總則P31-153 ")

  #rndrCode(gan_shens)
  for seq, gan_ in enumerate(gan_shens):
      if gan_ != '劫':
          continue
      if zhis[seq] in (cai_lu, piancai_lu):
          rndrCode("劫財坐財祿，如逢衝，大兇。先衝後合和稍緩解！母法總則P21-7 書上實例不準！")

          if zhi_shens[seq] == '財' and zhi_6he[seq]:
              rndrCode("劫財坐六合財支：久疾暗病！母法總則P28-113 乙未 丙戌 辛亥 庚寅！")

  if gan_shens[1] == '劫' and zhis[1] in (cai_lu, piancai_lu)  and zhis.count(yin_lu) > 1 and '劫' in gan_shens:
      rndrCode("月干劫坐財祿，有2印祿，劫透，財旺也敗：官非、刑名、意外災害！  母法總則P20-2")

  # 自坐陽刃
  if '劫' in zhi_shen3[2] and is_yang() and zhis[2] in zhengs:
      if zhis[3] in (cai_lu, piancai_lu):
          rndrCode("坐陽刃,時支財祿，吉祥但是妻子性格不受管制！母法總則P30-137 丁未 庚戌 壬子 乙巳")
      if zhi_ku(zhis[3], (cai, piancai)):
          rndrCode("坐陽刃,時支財庫，名利時進時退！母法總則P30-148 丙寅 壬寅 壬子 庚戌")

      if gan_shens[3] == '殺' and '殺' in zhi_shen3[3]:
          rndrCode("坐陽刃,時殺格，貴人提攜而富貴！母法總則P30-143 甲戌 丙寅 壬子 戊申")


  # 偏印分析
  if '枭' in gan_shens:
      rndrCode("----偏印在天干如成格：偏印在前，偏財(財次之)在後，有天月德就是佳命(偏印格在日時，不在月透天干也麻煩)。忌諱倒食，但是坐絕沒有這能力。")
      rndrCode("經典認爲：偏印不能扶身，要身旺；偏印見官殺未必是福；喜傷官，喜財；忌日主無根；   女顧兄弟姐妹；男六親似冰")
      rndrCode("偏印格干支有衝、合、刑，地支是偏印的絕位也不佳。")

      #rndrCode(zhi_shen3)
      if (gan_shens[1] == '枭' and '枭' in zhi_shen3[1]):
          rndrCode("枭月重叠：福薄慧多，青年孤獨，有文藝宗教傾向。")

      if zhi_shens2.count('枭') > 1:
          rndrCode("偏印根透2柱，孤獨有色情之患難。做事有始無終，女聲譽不佳！pd40")

      if  zhi_shens2.count('枭'):
          rndrCode("偏印成格基礎89生財、配印；最喜偏財同時成格，偏印在前，偏財在後。最忌諱日時坐實比劫刃。")
          all_ges.append('枭')

      if shens2.count('枭') > 2:
          rndrCode("偏印過多，性格孤僻，表達太含蓄，要別人猜，說話有時帶刺。偏悲觀。有偏財和天月德貴人可以改善。有藝術天賦。做事大多有始無終。如四柱全陰，女性聲譽不佳。")
          rndrCode("對兄弟姐妹不錯。男的因才干受子女尊敬。女的偏印多，子女不多。第1克傷食，第2藝術性。")
          if '傷' in gan_shens:
              rndrCode("女命偏印多，又與傷官同透，夫離子散。有偏財和天月德貴人可以改善。")

      if gan_shens.count('枭') > 1:
          rndrCode("天干兩個偏印：遲婚，獨身等，婚姻不好。三偏印，家族人口少，親屬不多建。基56甲午 甲戌 丙午 丙申")

      if shen_zhus[0] == ('枭', '枭'):
          rndrCode("偏印在年，干支俱透，不利于長輩。偏母當令，正母無權，可能是領養，庶出、同父異母等。 基56乙卯 甲申 丁丑 丁未")

      if zhi_shen3[1] == ['枭']:
          rndrCode("月專位偏印：有手藝。坐衰其貌不揚。")


  for seq, zhi_ in enumerate(zhi_shens):
      if zhi_ != '枭' and gan_shens[seq] != '枭':
          continue

      if ten_deities[gans[seq]][zhis[seq]] == '絕':
          rndrCode("偏印坐絕，或者天干坐偏印爲絕，難以得志。費力不討好。基56辛酉 辛卯 丁巳 甲辰  丁卯 丁未 己丑 丁卯")

      if  gan_shens[seq] == '枭':
          if '枭' in zhi_shen3[seq] :
              rndrCode("干支都與偏印，克夫福薄！")

          if '比' in zhi_shen3[seq] :
              rndrCode("偏印坐比：勞心勞力，常遇陰折 pd41")

          if zhi_shens[seq] == '傷':
              rndrCode("偏印坐傷官：克夫喪子 pd41")


  if zhi_shens[3]  == '枭' and gan_shens[0]  == '枭':
      rndrCode("偏印透年干-時支，一直受家裏影響。")

  if '枭' in (gan_shens[0],zhi_shens[0]):
      rndrCode("偏印在年：少有富貴家庭；有宗教素養，不喜享樂，第六感強。")
  if '枭' in (gan_shens[1],zhi_shens[1]):
      rndrCode("偏印在月：有慧少福，能舍己爲人。")
      if zhi_shens[1]  == '枭' and zhis[1] in "子午卯酉":
          rndrCode("偏印專位在月支：比較適合音樂，藝術，宗教等。子午卯酉。22-30之間職業定型。基56：壬午 癸卯 丁丑 丁未")
          if gan_shens[1] == '枭':
              rndrCode("干支偏印月柱，專位入格，有慧福淺，不爭名利。基57:戊子 辛酉 癸未 丁巳")
  if '枭' in (gan_shens[3],zhi_shens[3]):
      rndrCode("偏印在時：女與後代分居；男50以前奠定基礎，晚年享清福。")
  if zhi_shens[2] == '枭' or zhis.day == xiao_lu:
      rndrCode("偏印在日支：家庭生活沉悶")
      if zhi_6chong[2] or zhi_xing[2]:
          rndrCode("偏印在日支(專位？),有衝刑：孤獨。基57：甲午 癸酉 丁卯 丁未 母法總則P55-5： 辛丑 辛卯 癸酉 戊午 P77-13")
      if zhus[2] in (('丁','卯'),('癸','酉')):
          rndrCode("日專坐偏印：丁卯和癸酉。婚姻不順。又刑衝，因性格而起爭端而意外傷害。 基56")
      if zhis[3] == me_jue:
          rndrCode("日坐偏印，日支絕：無親人依靠，貧乏。 母法總則P55-5：丙辰 丙申 丁卯 壬子。pd41 專位偏印：男女姻緣都不佳。")

      if '枭' in gan_shens and is_yang() and zhis.time == me_di:

          rndrCode("日坐偏印成格，時支陽刃：不利妻子，自身有疾病。 母法總則P55-6：甲子 甲戌 丙寅 甲午")
      if gan_shens[3] == zhi_shens[3] == '劫':
          rndrCode("日坐偏印，時干支劫：因自己性格而引災。 母法總則P57-34：甲子 甲戌 丙寅 甲午")

      if zhis.count(me_di) > 1 and is_yang():
          rndrCode("日坐偏印，地支雙陽刃：性格有極端傾向。 母法總則P57-35：甲申 庚午 丙寅 甲午")


  if zhis.time == xiao_lu:
      if zhi_shens[3] == '枭' and '枭' in gan_shens:
          if '財' in shens2 or '才' in shens2:
              rndrCode("時支偏印成格有財：因機智引兇。 母法總則P60-18：甲申 乙亥 丁亥 癸卯")
          else:
              rndrCode("時支偏印成格無財：頑固引兇。 母法總則P60-17：甲子 乙亥 丁亥 癸卯")


  # 印分析
  if '印' in gan_shens:
      if '印' in zhi_shens2:
          rndrCode("基礎82，成格喜官殺、身弱、忌財克印。合印留財，見利忘義.透財官殺通關或印生比劫；合衝印若無他格或調候破格。日主強兇，祿刃一支可以食傷泄。")
          all_ges.append('印')

      if (gan_shens[1] == '印' and '印' in zhi_shen3[1]):
          rndrCode("印月重叠：女遲婚，月陽刃者離寡，能獨立謀生，有修養的才女。")

      if gan_shens[0] == '印' :
          rndrCode("年干印爲喜：出身于富貴之家。")

      if shens2.count('印') > 2:
          rndrCode("正印多的：聰明有謀略，比較含蓄，不害人，識時務。正印不怕日主死絕，反而怕太強。日主強，正印多，孤寂，不善理財。 pd41男的克妻，子嗣少。女的克母。")
      for seq, gan_ in enumerate(gan_shens):
          if gan_ != '印':
              continue
          if ten_deities[gans[seq]][zhis[seq]] in ('絕', '死'):
              if seq <3:
                  rndrCode("正印坐死絕，或天干正印地支有衝刑，不利母親。時柱不算。")
          if zhi_shens[seq] == '財':
              rndrCode("男正印坐正財，夫妻不好。月柱正印坐正財專位，必離婚。在時柱，50多歲才有正常婚姻。(男) 基59 乙酉 己卯 庚子 丁亥  庚申 庚辰 庚午 己卯")
          if zhi_shens[seq] == '印':
              rndrCode("正印坐正印，專位，過于自信。基59：戊辰 乙卯 丙申 丙申。務實，拿得起放得下。女的話大多晚婚。母長壽；女子息遲，頭胎恐流產。女四柱沒有官殺，沒有良緣。男的搞藝術比較好，經商則孤僻，不聚財。")

          if zhi_shens[seq] == '枭' and len(zhi5[zhis[seq]]) == 1:
              rndrCode("正印坐偏印專位：基59壬寅 壬子 乙酉 甲申。有多種職業;家庭不吉：親人有疾或者特別嗜好。子息遲;財務雙關。明一套，暗一套。女的雙重性格。")

          if zhi_shens[seq] == '傷':
              rndrCode("正印坐傷官：適合清高的職業。不適合追逐名利，女的婚姻不好。基59辛未 丁酉 戊子 丙辰")

          if zhi_shens[seq] == '劫' and me in ('甲','庚','壬'):
              rndrCode("正印坐陽刃，身心多傷，心疲力竭，偶有因公殉職。主要指月柱。工作看得比較重要。")


      if '殺' in gan_shens and '劫' in zhi_shens and me in ('甲','庚','壬'):
          rndrCode("正印、七殺、陽刃全：基60癸巳 庚申 甲寅 丁卯：女命宗教人，否則獨身，清高，身體恐有隱疾，性格狹隘缺耐心。男小疾多，紙上談兵，婚姻不佳，恐非婚生子女，心思細膩對人要求也高。")

      if '官' in gan_shens or '殺' in gan_shens:
          rndrCode("身弱官殺和印都透天干，格局佳。")
      else:
          rndrCode("單獨正印主秀氣、藝術、文才。性格保守")
      if '官' in gan_shens or '殺' in gan_shens or '比' in gan_shens:
          rndrCode("正印多者，有比肩在天干，不怕財。有官殺在天干也不怕。財不強也沒關系。")
      else:
          rndrCode("正印怕財。")
      if '財' in gan_shens:
          rndrCode("印和財都透天干，都有根，最好先財後印，一生吉祥。先印後財，能力不錯，但多爲他人奔波。(男)")


  if zhi_shens[1]  == '印':
      rndrCode("月支印：女命覺得丈夫不如自己，分居是常態，自己有能力。")
      if gan_shens[1]  == '印':
          rndrCode("月干支印：男權重于名，女命很自信，與夫平權。pd41:聰明有權謀，自我")
          if '比' in gan_shens:
              rndrCode("月干支印格，透比，有衝亡。")

  if zhi_shens[2]  == '印':
      if gan_shens[3] == '才' and '才' in zhi_shen3[3]:
          rndrCode("坐印，時偏財格：他鄉發迹，改弦易宗，妻賢子孝。 母法總則：P55-1 丁丑 丁未 甲子 戊辰")

      if gan_shens[3] == '財' and ('財' in zhi_shen3[3] or zhis[3] in (cai_di, cai_lu)):
          rndrCode("坐印，時財正格：晚年發達，妻賢子不孝。 母法總則：P55-2 乙酉 丙申 甲子 己巳")


  if zhi_shens[3]  == '印' and zhis[3] in zhengs:
      rndrCode("時支專位正印。男忙碌到老。女的子女各居一方。親情淡薄。")

  if gan_shens[3]  == '印' and '印' in zhi_shen3[3]:
      rndrCode("時柱正印格，不論男女，老年辛苦。女的到死都要控制家產。子女無緣。")

  if gan_shens.count('印') + gan_shens.count('枭') > 1:
      rndrCode("印枭在年干月干，性格迂腐，故作清高，女子息遲，婚姻有阻礙。印枭在時干，不利母子，性格不和諧。")


  if zhis[1] in (yin_lu, xiao_lu) :
      rndrCode("印或枭在月支，有壓制丈夫的心態。")

  if zhis[3] in (yin_lu, xiao_lu) :
      rndrCode("印或枭在時支，夫災子寡。")

  # 坐印庫
  if zhi_ku(zhis[2], (yin, xiao)):
      if shens2.count('印') >2:
          rndrCode("母法總則P21-5: 日坐印庫，又成印格，意外傷殘，兇終。過旺。")
      if zhi_shens[3] == '劫':
          rndrCode("自坐印庫，時陽刃。帶比祿印者貧，不帶吉。 母法總則P21-14")

  if zhis.count("印") > 1:
      if gan_shens[1] == "印" and zhi_shens[1] == "印" and '比' in gan_shens:
          rndrCode("月干支印，印旺，透比，旺而不久，衝亡。母法總則P21-8")

  if zhis[1] == yin_lu:
      if ('財' in gan_shens and '財' in zhi_shens) or ('才' in gan_shens and '才' in zhi_shens):
          rndrCode("母法總則P22-18 自坐正印專旺，成財格，移他鄉易宗，妻賢子孝。")


  # 偏財分析
  if '才' in gan_shens:
      rndrCode("偏財明現天干，不論是否有根:財富外人可見;實際財力不及外觀一半。沒錢別人都不相信;協助他人常超過自己的能力")
      rndrCode("偏財出天干，又與天月德貴人同一天干者。在年月有聲明遠揚的父親，月時有聰慧的紅顏知己。喜奉承。")
      rndrCode("偏財透天干，四柱沒有刑衝，長壽。女子爲孝順女，主要針對年月。時柱表示中年以後有自己的事業，善于理財。")
      if '才' in zhi_shens2:
          rndrCode("財格基礎80:比劫用食傷通關或官殺制；身弱有比劫仍然用食傷通關。如果時柱坐實比劫，晚年破產。")
          all_ges.append('才')
      rndrCode("偏財透天干，講究原則，不拘小節。喜奉承，善于享受。財格基礎80")

      if '比' in gan_shens or '劫' in gan_shens and gan_shens[3] == '才':
          rndrCode("年月比劫，時干透出偏財。祖業凋零，再白手起家。有刑衝爲千金散盡還復來")
      if '殺' in gan_shens and '殺' in zhi_shens:
          rndrCode("偏財和七殺并位，地支又有根，父子外合心不合。因爲偏財生殺攻身。偏財七殺在日時，則爲有難伺候的女朋友。 基62壬午 甲辰 戊寅 癸亥")

      if zhi_shens[0]  == '才':
          rndrCode("偏財根透年柱，家世良好，且能承受祖業。")

      for seq, gan_ in enumerate(gan_shens):
          if gan_ != '才':
              pass
          if '劫' in zhi_shen3[seq] and zhis[seq] in zhengs:
              rndrCode("偏財坐陽刃劫財,可做父緣薄，也可幼年家貧。也可以父先亡，要參考第一大運。偏財坐專位陽刃劫財,父親去他鄉.基61壬午 壬寅 戊子 丁巳")
          if get_empty(zhus[2],zhis[seq]) == '空':
              rndrCode("偏財坐空亡，財官難求。")

  if shens2.count('才') > 2:
      rndrCode("偏財多的人慷慨，得失看淡。花錢一般不會後悔。偏樂觀，甚至是浮誇。生活習慣颠倒。適應能力強。有團隊精神。得女性歡心。小事很少失信。")
      rndrCode("樂善好施，有團隊精神，女命偏財，聽父親的話。時柱偏財女，善于理財，中年以後有事業。")
  if (zhi_shens[2]  == '才' and len(zhi5[zhis[2]]) == 1) or (zhi_shens[3]  == '才' and len(zhi5[zhis[3]]) == 1):
      rndrCode("日時地支坐專位偏財。不見刑衝，時干不是比劫，大運也沒有比劫刑衝，晚年發達。")



  # 財分析

  if (gan_shens[0] in ('財', '才')  and gan_shens[1]  in ('財', '才')) or (gan_shens[1] in ('財', '才') and ('財' in zhi_shen3[1] or '才' in zhi_shen3[1])):
      rndrCode("財或偏財月重叠：女職業婦女，有理財辦事能力。因自己理財能力而影響婚姻。一財得所，紅顏失配。男的雙妻。")


  if '財' in gan_shens:
      if '財' in zhi_shens2:
          all_ges.append('財')

      if is_yang():
          rndrCode("男日主合財星，夫妻恩愛。如果爭合或天干有劫財，雙妻。")
      if '財' in zhi_shens:
          rndrCode("財格基礎80:比劫用食傷通關或官殺制；身弱有比劫仍然用食傷通關。")

      if '官' in gan_shens:
          rndrCode("正官正財并行透出，(身強)出身書香門第。")
      if '官' in gan_shens or '殺' in gan_shens:
          rndrCode("官或殺與財并行透出，女壓夫，財生官殺，老公壓力大。")
      if gan_shens[0] == '財':
          rndrCode("年干正財若爲喜，富裕家庭，但不利母親。")
      if '財' in zhi_shens:
          if '官' in gan_shens or '殺' in gan_shens:
              rndrCode("男財旺透官殺，女厭夫。")
      if gan_shens.count('財') > 1:
          rndrCode("天干兩正財，財源多，大多做好幾種生意，好趕潮流，人云亦云。有時會做自己外行的生意。")
          if '財' not in zhi_shens2:
              rndrCode("正財多而無根虛而不踏實。重財不富。")

  for seq, gan_ in enumerate(gan_shens):
      if gan_ != '財' and zhis[seq] != '財':
          continue
      if zhis[seq] in day_shens['驿馬'][zhis.day] and seq != 2:
          rndrCode("女柱有財+驿馬，動力持家。")
      if zhis[seq] in day_shens['桃花'][zhis.day] and seq != 2:
          rndrCode("女柱有財+桃花，不吉利。")
      if zhis[seq] in empties[zhus[2]]:
          rndrCode("財坐空亡，不持久。")
      if ten_deities[gans[seq]][zhis[seq]] in ('絕', '墓'):
          rndrCode("男財坐絕或墓，不利婚姻。")

  if shens2.count('財') > 2:
      rndrCode("正財多者，爲人端正，有信用，簡樸穩重。")
      if '財' in zhi_shens2 and (me not in zhi_shens2):
          rndrCode("正財多而有根，日主不在生旺庫，身弱懼內。")

  if zhi_shens[1] == '財' and 方向:
      rndrCode("女命月支正財，有務實的婚姻觀。")

  if zhi_shens[1] == '財':
      rndrCode("月令正財，無衝刑，有賢內助，但是母親與妻子不和。生活簡樸，多爲理財人士。")
  if zhi_shens[3] == '財' and len(zhi5[zhis[3]]) == 1:
      rndrCode("時支正財，一般兩個兒子。")
  if zhus[2] in (('戊','子'),) or zhus[3] in (('戊','子'),):
      rndrCode("日支專位正財，得勤儉老婆。即戊子。日時專位支正財，又透正官，中年以後發達，獨立富貴。")

  if zhus[2] in (('壬','午'),('癸','巳'),):
      rndrCode("坐財官印，只要四柱沒有刑衝，大吉！")

  if zhus[2] in (('甲','戌'),('乙','亥'),):
      rndrCode("女('甲','戌'),('乙','亥'） 晚婚 -- 不準！")

  if '財' == gan_shens[3] or  '財' == zhi_shens[3]:

      rndrCode("未必準确：時柱有正財，口快心直，不喜拖泥帶水，刑衝則浮躁。陽刃也不佳.反之有美妻佳子")
  if (not '財' in shens2) and (not '才' in shens2):
      rndrCode("四柱無財，即便逢財運，也是虛名虛利. 男的晚婚")


  #rndrCode("shang", shang, ten_deities[shang].inverse['建'], zhi_shens)
  #if ten_deities[shang].inverse['建'] in zhis:
      #rndrCode("女命一財得所，紅顏失配。")

  if zhis.day in (cai_lu, cai_di):
      if (zhi_shens[1] == '劫' or zhi_shens[3] == '劫' ) and Gan.index(me) % 2 == 0:
          rndrCode("自坐財祿，月支或時支爲陽刃，兇。無衝是非多，衝刑主病災。 母法總則P22-15  母法總則P36-4 丙寅 戊戌 甲午 丁卯 P56-32 己未 丙寅 丙申 甲午")
      if ('劫' in zhi_shens ) and Gan.index(me) % 2 == 0 and '劫' in gan_shens :
          rndrCode("自坐財祿，透劫財，有陽刃，刑妻無結局。 母法總則P36-7 戊子 乙卯 甲午 乙亥")
      if me in ('甲', '乙') and ('戊' in gans or '己' in gans):
          rndrCode("火土代用財，如果透財，多成多敗，早年灰心。 母法總則P22-19 辛未 癸巳 甲午 戊辰")

      if gan_shens[3] == '枭':
          rndrCode("財祿時干偏印：主親屬孤獨 母法總則P31-158 丁丑 丙午 甲辰 己巳")
          if '枭' in zhi_shen3[3]:
              rndrCode("財祿時干偏印格：財雖吉、人丁孤單、性格藝術化 母法總則P56-20 己巳 丙辰 甲午 壬申")

      if zhis[3] == yin_lu:
          rndrCode("坐財祿，時支印祿：先難後易 母法總則P30-147 甲申 己巳 壬午 己酉 母法總則P55-16")


  if (gan_he[3] and gan_shens[3] == '財' and jin_jiao(zhis[2], zhis[3]) ) or (gan_he[2] and gan_he[1] and gan_shens[1] == '財' and jin_jiao(zhis[1], zhis[2])):

      rndrCode("日主合財且進角合：一生吉祥、平安有裕！ 母法總則P22-22 丁丑 丙午 甲辰 己巳")


  if zhis.day == cai_lu or zhi_shens[2] == '財':
      if gan_shens[3] == '枭' and ('枭' in zhi_shen3[3] or zhis[3] == xiao_lu ):
          rndrCode("日坐財，時偏印格：他鄉有成，爲人敦厚。母法總則P55-4 甲寅 辛未 甲午 壬申")
      if zhi_6chong[2] or zhi_xing[2]:
          rndrCode("日坐財，有衝或刑：財吉而有疾。母法總則P55-10 丙寅 戊戌 甲午 甲子")


  if gan_shens[3] == '財' and zhi_ku(zhis[3], (me,jie)):
      rndrCode("正財坐日庫于時柱:孤獨、難爲父母，但事業有成。 母法總則P31-156 丁丑 丙午 甲辰 己巳")

  # 自坐財庫
  if zhis[2] == cai_ku:
      if zhis[3] == me_ku :
          rndrCode("自坐財庫,時劫庫：有財而孤單。 母法總則P30-136 丁丑 丙午 甲辰 己巳 母法總則P55-11 P61-5 甲子 己巳 壬戌 甲辰")

      if zhis[2] == zhis[3]:
          rndrCode("自坐財庫,時坐財庫：妻有災，妻反被妾制服。 母法總則P30-150 辛酉 乙未 壬戌 庚戌 母法總則P56-19")


      if gan_shens[3] == '殺' and '殺' in zhi_shen3[3]:
          rndrCode("自坐財庫,時殺格，財生殺，兇！母法總則P30-147 甲寅 己巳 壬戌 戊申 有可能是時柱有殺就算。 母法總則P55-15")

  # 時坐財庫
  if zhi_ku(zhis[3], (cai,piancai)):
      if '傷' in gan_shens and '傷' in zhi_shens:
          rndrCode("時坐財庫,傷官生財:財好，體弱，旺處壽傾倒！母法總則P59-8 戊申 辛酉 戊子 丙辰")

  if gan_shens[3] == '財' and '財' in zhi_shen3[3]:
      rndrCode("時上正財格:不必財旺，因妻致富。 母法總則P30-140 丙午 戊戌 壬寅 丁未 母法總則P60-21")

      if zhis[3] == me_ku:
          rndrCode("時上正財格坐比劫庫，克妻。 母法總則P30-141 丙午 戊戌 壬寅 丁未")
      if zhis[2] == cai_ku:
          rndrCode("時上正財格自坐財庫，妻佳，中年喪妻，續弦也佳。 母法總則P30-142 庚子 辛巳 壬戌 丁未 P61-7")

  #rndrCode(cai_di, cai_lu, zhis, gan_he)
  if zhis[3] in (cai_di, cai_lu):
      if gan_he[3]:
          rndrCode("時財祿，天干日時雙合，損妻家財。 母法總則P31-157 庚戌 戊寅 癸酉 戊午")
      if '傷' == gan_shens[3] and '傷' in zhi_shens2:
          rndrCode("時支正財時干傷成格：雖富有也刑克。 母法總則P59-1 丁丑 壬寅 丁巳 戊申")
      #rndrCode(zhi_ku(zhis[1], (shi,shang)) , (shi,shang), zhis[3] == cai_lu)
      if zhi_ku(zhis[1], (shi,shang)) and zhis[3] == cai_lu:
          rndrCode("時支正財祿，月支傷入墓：生財極爲辛勤。 母法總則P59-4 甲子 戊辰 庚戌 己卯")

  # rndrCode(cai_di, cai_lu, zhis, gan_he)
  if zhis[3] == cai_lu:
      if zhi_xing[3] or zhi_6chong[3]:
          rndrCode("時支正財祿有衝刑：得女伴且文學清貴。 母法總則P60-11 丁丑 辛亥 己巳 乙亥")
      if any(zhi_xing[:3]) or any(zhi_6chong[:3]):
          rndrCode("時支正財祿,它支有衝刑：刑妻、孤高、藝術、近貴人。 母法00總則P60-19 乙未 己丑 庚寅 己卯")
      if gan_shens.count('財') >1 :
          rndrCode("時支正財祿,天干財星多：孤雅、九流、表面風光。 母法總則P60-20 乙酉 乙酉 庚辰 己卯")


  # 官分析
  if '官' in gan_shens:
      if '官' in zhi_shens2:
          rndrCode("官若成格：忌傷；忌混雜；基礎78。有傷用財通關或印制。混雜用合或者身官兩停。日主弱則不可扶。")
          all_ges.append('官')

          if '比' in gan_shens or '劫' in gan_shens:
              rndrCode("官格透比或劫：故做清高或有潔癖的文人。")

          if '傷' in gan_shens:
              rndrCode("官格透傷：表裏不一。")

          if '財' in gan_shens or '才' in gan_shens:
              rndrCode("官格透財：聚財。")

          if '印' in gan_shens:
              rndrCode("官格透印：人品清雅。")

          if not ('印' in gan_shens or '財' in gan_shens or '才' in gan_shens):
              rndrCode("官獨透成格：敦厚人。")


      if (gan_shens[0] == '官' and gan_shens[1] == '官') or (gan_shens[1] == '官' and '官' in zhi_shen3[1]):
          rndrCode("官月重叠：女易離婚，早婚不吉利。爲人性格溫和。")

      if gan_shens[3] == '官' and len(zhi5[zhis[3]]) == 1:
          rndrCode("官專位時坐地支，男有得力子息。")
      if gan_shens[0] == '官' :
          rndrCode("年干爲官，身強有可能出身書香門第。")
          if gan_shens[3] == '官':
              rndrCode("男命年干，時干都爲官，對後代和頭胎不利。")
      if (not '財' in gan_shens) and (not '印' in gan_shens):
          rndrCode("官獨透天干成格，四柱無財或印，爲老實人。")
      if '傷' in gan_shens:
          rndrCode("正官傷官通根透，又無其他格局，失策。尤其是女命，異地分居居多，婚姻不美滿。基64:辛未 丁酉 甲戌 辛未 ")
      if '殺' in gan_shens:
          rndrCode("年月干殺和偏官，30以前婚姻不穩定。月時多爲體弱多病。")

      if '印' in gan_shens and '印' in zhi_shens2 and '官' in zhi_shens2:
          rndrCode("官印同根透，無刑衝合，吉。")
          if '財' in gan_shens and '財' in zhi_shens2:
              rndrCode("財官印同根透，無刑衝合，吉。")

      if gan_shens[1] == '官' in ten_deities[me][zhis[1]] in ('絕', '墓'):
          rndrCode("官在月坐墓絕，不是特殊婚姻就是遲婚。如果與天月德同柱，依然不錯。丈夫在庫中：1，老夫少妻；2，不爲外人所知的親密感情；3，特殊又合法的婚姻。")
      if zhi_shens[1] == '官' and gan_shens[1] == '官':
          rndrCode("月柱正官坐正官，婚變。月柱不宜通。坐祿的。")


      for seq, gan_ in enumerate(gan_shens):
          if gan_ != '官':
              continue
          if zhi_shens[seq] in ('劫','比') :
              rndrCode("天干正官，地支比肩或劫財，親友之間不適合合作，但是他適合經營爛攤子。")
          if zhi_shens[seq] == '殺' :
              rndrCode("正官坐七殺，男命恐有訴訟之災。女命婚姻不佳。月柱尤其麻煩，二度有感情糾紛。年不算，時從輕。 基64 壬子 壬子 丁丑 癸卯")
          if zhi_shens[seq] == '劫' and Gan.index(me) % 2 == 0:
              rndrCode("官坐羊刃：要殺才能制服陽刃，有力不從心之事情。 辛卯 丁酉 庚午 庚辰 基65")
          if zhi_shens[seq] == '印':
              rndrCode("官坐印，無刑衝合，吉")


  if shens2.count('官') > 2 and '官' in gan_shens and '官' in zhi_shens2:
      rndrCode("正官多者，虛名。爲人性格溫和，比較實在。做七殺看")
  if zhis.day == guan_lu or zhi_shens[2] == '官':
      rndrCode("日坐正官專位，淑女。 基65 庚申 癸未 丙子 乙未")
      if is_yang() and zhis.time == me_di:
          rndrCode("日坐正官，時支陽刃：先富後敗，再東山再起。 子平母法 P55-7")

  if gan_shens.count('官') > 2 :
      rndrCode("天干2官，女下有弟妹要照顧，一生爲情所困。")


  if zhi_shens[1] == '官' and '傷' in zhi_shens2:
      rndrCode("月支正官，又成傷官格，難做真正夫妻。有實，無名。 基66辛丑 辛卯 戊子 辛酉")


  # 殺分析
  if '殺' in gan_shens:
      rndrCode("七殺是非多。但是對男人有時是貴格。比如毛主席等。成格基礎85可殺生印或食制印、身殺兩停、陽刃駕殺。")
      if '殺' in zhi_shens2:
          rndrCode("殺格：喜食神制，要食在前，殺在後。陽刃駕殺：殺在前，刃在後。身殺兩停：比如甲寅日庚申月。殺印相生，忌食同成格。")
          all_ges.append('殺')

          if '比' in gan_shens or '劫' in gan_shens:
              rndrCode("殺格透比或劫：性急但還有分寸。")

          if '殺' in gan_shens:
              rndrCode("殺格透官：精明瑣屑，不怕髒。")

          if '食' in gan_shens or '傷' in gan_shens:
              rndrCode("殺格透食傷：外表寧靜，內心剛毅。")

          if '印' in gan_shens:
              rndrCode("殺格透印：圓潤、精明干練。")

      if (gan_shens[0] == '殺' and gan_shens[1] == '殺') :
          rndrCode("殺月干年干重叠：不是老大，出身平常，多災，爲人不穩重。")

      if (gan_shens[1] == '殺' and '殺' in zhi_shen3[1]):
          rndrCode("殺月重叠：女易離婚，其他格一生多病。")

      if gan_shens[0] == '殺':
          rndrCode("年干七殺，早年不好。或家裏窮或身體不好。")
          if gan_shens[1] == '殺':
              rndrCode("年月天干七殺，家庭復雜。")
      if '官' in gan_shens:
          rndrCode("官和殺同見天干不佳。女在年干月干，30以前婚姻不佳，或體弱多病。基65 甲寅 乙亥 戊子 丙辰")
      if gan_shens[1] == '殺' and zhi_shens[1] == '殺':
          rndrCode("月柱都是七殺，克得太過。有福不會享。六親福薄。時柱沒關系。")
          if '殺' not in zhi_shens2 :
              rndrCode("七殺年月浮現天干，性格好變，不容易定下來。30歲以前不行。")
      if '殺' in zhi_shens and '劫' in zhi_shens:
          rndrCode("七殺地支有根時要有陽刃強爲佳。殺身兩停。")
      if gan_shens[1] == '殺' and gan_shens[3] == '殺':
          rndrCode("月時天干爲七殺：體弱多病")
      if gan_shens[0] == '殺' and gan_shens[3] == '殺':
          rndrCode("七殺年干時干：男頭胎麻煩（概率），女婚姻有阻礙。")
      if gan_shens[3] == '殺':
          rndrCode("七殺在時干，固執有毅力。基67")
      if '印' in gan_shens:
          rndrCode("身弱殺生印，不少是精明練達的商人。")
      if '財' in gan_shens or '才' in gan_shens:
          rndrCode("財生殺，如果不是身弱有印，不佳。")
          for zhi_ in zhis:
              if set((ten_deities[me].inverse['殺'], ten_deities[me].inverse['財'])) in set(zhi5[zhi_]):
                  rndrCode("殺不喜與財同根透出，這樣殺的力量太強。")


  for seq, gan_ in enumerate(gan_shens):
      if gan_ != '殺' and zhi_shens[seq] != '殺':
          continue
      if gan_ == '殺' and '殺' in zhi_shen3[seq] and seq != 3:
          rndrCode("七殺坐七殺，六親福薄。")
      if get_empty(zhus[2],zhis[seq]) == '空':
          rndrCode("七殺坐空亡，女命夫緣薄。 基68 壬申 庚戌 甲子 丙寅")
      if zhis[seq] == '食':
          rndrCode("七殺坐食：易有錯誤判斷。")
      if zhi_xing[seq] or zhi_6chong[seq]:
          rndrCode("七殺坐刑或對衝，夫妻不和。")


  if shens2.count('殺') > 2:
      rndrCode("殺多者如果無制，性格剛強。打抱不平，不易聽人勸。女的喜歡佩服的人。")
  if zhi_shens[2]  == '殺' and len(zhi5[zhis[2]]) == 1:
      rndrCode("天元坐殺：乙酉，己卯，如無食神，陽刃，性急，聰明，對人不信任。如果七殺還透出月干無制，體弱多病，甚至夭折。如果在時干，晚年不好。")

  if zhus[2] in (('丁', '卯'), ('丁', '亥'), ('丁', '未')) and zhis.time == '子':
      rndrCode("七殺坐桃花，如有刑衝，引感情引禍。忌諱午運。")

  if gan_shens.count('殺') > 2 :
      rndrCode("天干2殺，不是老大、性格浮躁不持久。")

  if ten_deities[shang].inverse['建'] in zhis and 方向:
      rndrCode("女地支有殺的祿：丈夫條件還可以。對外性格急，對丈夫還算順從。")



  if zhis[2] == me_jue:
      rndrCode("#"*10, "自坐絕")
      if zhi_6he[2]:

          rndrCode("自己坐絕（天元坐殺）：日支與它支合化、雙妻，子息遲。母法總則P21-9 P56-30 d第10點暫未編碼。")

      rndrCode("自己坐絕支，絕支合會，先貧後富。母法總則P57-3 母法總則P23-33")
      if zhis[3] == zhis[2]:
          rndrCode("日主日時絕，旺達則有刑災。母法總則P57-2 母法總則P24-43 戊午 癸亥 乙酉 乙酉")

      if zhis[3] == zhis[2] == zhis[1]:
          rndrCode("日主月日時絕，旺達則有刑災，平常人不要緊。母法總則P57-1")
      if zhi_shens.count('比') + zhi_shens.count('劫') > 1 :
          rndrCode("自坐絕，地支比劫大于1，旺衰巨變，兇：母法總則P22-16。 母法總則P36-5月支或時支都爲陽刃，兇。")

      if zhis[1] == me_jue:
          rndrCode("日主月日絕，有格也疾病夭。母法總則P23-35")

      if zhis[3] == cai_lu:
          rndrCode(" 母法總則P59-2  自坐絕，月支財祿:身弱財旺有衰困時，克妻子。書上例子不對")

      if zhis[3] == cai_di:
          rndrCode(" 母法總則P59-3  自坐絕，月支偏財祿:有困頓時娶背景不佳妻。書上例子不對")




  if zhis[3] == me_jue:
      rndrCode("#"*10, "自己時坐絕: 母法總則P57-4: 若成傷官格，難求功名，適合藝術九流。")
      if zhi_shens[2] == '枭':
          rndrCode("母法總則P57-5: 自時支坐絕，自坐枭: 不是生意人，清貧藝術九流人士。")
      #rndrCode(zhi_shens, cai_di, cai_lu)
      if zhis[1] in (cai_di, cai_lu):
          rndrCode(" 母法總則P57-6  自時支坐絕，月支坐財:先富，晚年大敗，刑破。 癸未 庚申 丁巳 庚子")

      if zhis[1] in (me_lu, me_di):
          rndrCode(" 母法總則P28-114  自時支坐絕，月支帝:刑妻克子。 甲子 癸酉 辛丑 辛卯 -- 陰干也算陽刃？")

      if zhis[3] in (cai_di,cai_lu):
          rndrCode(" 母法總則P57-8  自時支坐絕，時支財:中年發後無作爲。 甲子 癸酉 辛丑 辛卯")


  if zhis[2] == sha_lu:
      if zhi_ku(zhis[3], (guan, sha)):
          rndrCode("自坐殺祿，時支爲官殺庫，一生有疾，生計平常。 母法總則P21-12 母法總則P55-8 甲子 丙寅 乙酉 己丑 P56-31")

  if zhis[3] == sha_lu:
      if zhi_xing[3] or zhi_6chong[3]:

          rndrCode("時支殺祿帶刑衝：縱然吉命也帶疾不永壽。 母法總則P60-15 乙未 乙酉 戊申 甲寅")

  if gan_shens[3] == '殺' and zhis[3] in (cai_di, cai_lu):
      rndrCode("七殺時柱坐財祿旺：性格嚴肅。 母法總則P59-7 母法總則P79-3 雙妻，子息遲。 ")

  #rndrCode(sha_lu, zhi_6chong,zhi_xing )
  if zhis[3] == sha_lu:
      if (zhi_6chong[3] or zhi_xing[3]):
          rndrCode("七殺時祿旺：遇刑衝壽夭帶疾。 母法總則P28-118 衝別的柱也算？ 乙未 戊寅 辛丑 甲午 ")
      if zhis[1] == sha_lu:
          rndrCode("七殺時月祿旺：體疾。 母法總則P28-119 甲寅 庚午 辛丑 甲午  母法總則P60-16")

  #rndrCode(zhi_ku(zhis[2], (guan,sha)),set(zhis), set('辰戌丑未'))
  if zhi_ku(zhis[2], (guan,sha)):
      if set(zhis).issubset(set('辰戌丑未')):
          rndrCode("自坐七殺入墓：地支都爲庫，孤獨藝術。 母法總則P57-33  丙辰 戊戌 乙丑 庚辰")

  if '殺' in gan_shens and zhi_shens.count('殺') > 1:
      rndrCode("七殺透干，地支雙根，不論貧富，親屬離散。母法總則P79-6 乙未 丙戌 戊寅 甲寅")

  if  '殺' in jus + all_ges:

      if '比' in gan_shens or '劫' in gan_shens:
          rndrCode("殺格透比或劫：性急但還有分寸。")

      if '殺' in gan_shens:
          rndrCode("殺格透官：精明瑣屑，不怕髒。")

      if '食' in gan_shens or '傷' in gan_shens:
          rndrCode("殺格透食傷：外表寧靜，內心剛毅。")

      if '印' in gan_shens:
          rndrCode("殺格透印：圓潤、精明干練。")

  # 食分析
  if '食' in gan_shens:
      if '食' in zhi_shens2:
          rndrCode("食神成格的情況下，壽命比較好。食神和偏財格比較長壽。食神厚道，爲人不慷慨。食神有口福。成格基礎84，喜財忌偏印(只能偏財制)。")
          rndrCode("食神無財一生衣食無憂，無大福。有印用比劫通關或財制。")
          all_ges.append('食')


      if (gan_shens[0] == '食' and gan_shens[1] == '食') or (gan_shens[1] == '食' and '食' in zhi_shen3[1]):
          rndrCode("食月重叠：生長安定環境，性格仁慈、無衝刑長壽。女早年得子。無衝刑偏印者是佳命。")


      if '枭' in gan_shens:
          rndrCode("男的食神碰到偏印，身體不好。怕偏印，正印要好一點。四柱透出偏財可解。")
          if '劫' in gan_shens:
              rndrCode("食神不宜與劫財、偏印齊出干。體弱多病。基69")
          if '殺' in gan_shens:
              rndrCode("食神不宜與殺、偏印齊成格。體弱多病。")
      if '食' in zhi_shens:
          rndrCode("食神天透地藏，女命陽日主適合社會性職業，陰日主適合上班族。")
      if (not '財' in gan_shens) and (not '才' in gan_shens):
          rndrCode("食神多，要食傷生財才好，無財難發。")
      if '傷' in gan_shens:
          rndrCode("食傷混雜：食神和傷官同透天干：志大才疏。")
      if '殺' in gan_shens:
          rndrCode("食神制殺，殺不是主格，施舍後後悔。")



      for seq, gan_ in enumerate(gan_shens):
          if gan_ != '食':
              continue
          if zhi_shens[seq] =='劫':
              rndrCode("食神坐陽刃，辛勞。基69 戊申 戊午 丙子 丙申")


  if shens2.count('食') > 2:
      rndrCode("食神四個及以上的爲多，做傷官處理。食神多，要食傷生財才好，無財難發。")
      if '劫' in gan_shens or '比' in gan_shens:
          rndrCode("食神帶比劫，好施舍，樂于做社會服務。")

  if ('殺', '食') in shen_zhus or ( '食', '殺') in shen_zhus:
      rndrCode("食神與七殺同一柱，易怒。食神制殺，最好食在前。有一定概率。基69辛未 丁酉 乙未 戊寅")

  if ('枭', '食') in shen_zhus or ( '食', '枭') in shen_zhus:
      rndrCode("女命最怕食神偏印同一柱。不利後代，時柱尤其重要。基69庚午 己卯 丁未 丁未")

  if '食' in zhi_shen3[2] and zhis[2] in zhengs:
      rndrCode("日支食神專位容易發胖，有福。只有2日：癸卯，己酉。男命有有助之妻。")
  if zhi_shens[2]  == '食' and zhi_shens[2]  == '殺':
      rndrCode("自坐食神，時支殺專，二者不出天干，多成敗，最後失局。")

  if zhi_shens[2]  == '食':
      rndrCode("自坐食神，相敬相助，即使透枭也無事，不過心思不定，做事毅力不足，也可能假客氣。專位容易發胖，有福。")


  if zhis[2]  == shi_lu:
      if zhis[3]  == sha_lu and (sha not in gan_shens):
          rndrCode("自坐食，時支專殺不透干：多成敗，終局失制。母法總則P56-22 丙子 庚寅 己酉 丁卯")

  if '食' in zhi_shen3[3] and '枭' in zhi_shen3[3] + gan_shens[3]:
      rndrCode("時支食神逢偏印：體弱，慢性病，女的一婚不到頭。")

  if zhis[2] in kus and zhi_shen3[2][2] in ('食', '傷'):
      rndrCode("自坐食傷庫：總覺得錢不夠。")

  if  '食' in (gan_shens[0], zhi_shens[0]):
      rndrCode("年柱食：可三代同堂。")

  if zhi_ku(zhis[3], (shi, shang)) and ('食' in zhi_shen3[1] or '傷' in zhi_shen3[1]):
      rndrCode("時食庫，月食當令，孤克。")

  # 自坐食傷庫
  if zhi_ku(zhis[2], (shi, shang)):
      if zhis[3] == guan_lu:
          rndrCode("坐食傷庫：時支官，發達時接近壽終。 母法總則P60-13 乙丑 丙戌 庚辰 壬午")

  # 自坐食傷庫
  if zhi_ku(zhis[3], (shi, shang)):

      if zhis[1] in (shi_di, shi_lu):
          rndrCode("坐食傷庫：月支食傷當令，吉命而孤克。 母法總則P60-14 甲戌 丙子 辛卯 壬辰")


  # 傷分析
  if '傷' in gan_shens:
      rndrCode("傷官有才華，但是清高。要生財，或者印制。")
      if '傷' in zhi_shens2:
          rndrCode("食神重成傷官，不適合傷官配印。金水、土金、木火命造更高。火土要調候，容易火炎土燥。傷官和七殺的局不適合月支爲庫。")
          all_ges.append('傷')
          rndrCode("傷官成格基礎87生財、配印。不考慮調候逆用比順用好，調候更重要。生正財用偏印，生偏財用正印。\n傷官配印，如果透殺，透財不佳。傷官七殺同時成格，不透財爲上好命局。")

      if (gan_shens[0] == '傷' and gan_shens[1] == '傷') or (gan_shens[1] == '傷' and '傷' in zhi_shen3[1]):
          rndrCode("父母兄弟均無緣。孤苦，性剛毅好掌權。30歲以前有嚴重感情苦重，適合老夫少妻，繼室先同居後結婚。")


      if '印' in gan_shens and ('財' not in gan_shens):
          rndrCode("傷官配印，無財，有手藝，但是不善于理財。有一定個性")
      if gan_shens[0] == '傷' and gan_shens[1] == '傷' and (not '傷' in zhi_shens2):
          rndrCode("年月天干都浮現傷官，親屬少。")

      if zhi_shens[1]  == '傷' and len(zhi5[zhis[1]]) == 1 and gan_shens[1] == '傷':
          rndrCode("月柱：傷官坐專位傷官，夫緣不定。假夫妻。比如老板和小蜜。")


      for seq, gan_ in enumerate(gan_shens):
          if gan_ != '傷':
              continue
          if zhi_shens[seq] =='劫':
              rndrCode("傷官地支坐陽刃，力不從心 基70己酉 丁卯 甲午 辛未。背祿逐馬，克官劫財。影響15年。傷官坐劫財：只適合純粹之精明商人或嚴謹掌握財之人。")

  if shens2.count('傷') > 2:
      if 方向:
          rndrCode("女命傷官多，即使不入傷官格，也緣分淺，多有苦情。")
      if gan_shens.count('傷') > 2:
          rndrCode("天干2傷官：性驕，六親不靠。婚前訴說家人，婚後埋怨老公。30歲以前爲婚姻危機期。")

  if zhi_shens[2]  == '傷' and len(zhi5[zhis[2]]) == 1:
      rndrCode("女命婚姻宮傷官：強勢克夫。男的對妻子不利。只有庚子日。")

  if gan_shens[3]  == '傷' and me_lu == zhis[3]:
      rndrCode("傷官坐時祿：六親不靠，無衝刑晚年發，有衝刑不發。 母法P27-96己未 壬申 己亥 庚午, 可以參三命。")

  if zhis[3]  in (shang_lu, shang_di) and  zhis[1]  in (shang_lu, shang_di):
      rndrCode("月支時支食傷當令：日主無根，泄盡日主，兇。 母法P28-104 甲午 乙亥 庚戌 丙子  母法P60-104")

  #rndrCode("shang", shang, ten_deities[shang].inverse['建'], zhi_shens)
  if ten_deities[shang].inverse['建'] in zhis and 方向:
      rndrCode("女命地支傷官祿：婚姻受不得窮。")

  rndrCode(["局", jus, "格", all_ges])

  if me+zhis.month in months:
      rndrCode("\n\n《窮通寶鑒》")
      rndrCode("=========================")
      rndrCode(months[me+zhis.month])


  sum_index = ''.join([me, '日', *zhus[3]])
  if sum_index in summarys:
      rndrCode("\n\n《三命通會》")
      rndrCode("=========================")
      rndrCode(summarys[sum_index])

  if not None: #options.b
      rndrCode("\n\n大運")
      rndrCode("="*120)
      for dayun in yun.getDaYun()[1:]:
          gan_ = dayun.getGanZhi()[0]
          zhi_ = dayun.getGanZhi()[1]
          fu = '*' if (gan_, zhi_) in zhus else " "
          zhi5_ = ''
          for gan in zhi5[zhi_]:
              zhi5_ = zhi5_ + "{}{}　".format(gan, ten_deities[me][gan])

          zhi__ = set() # 大運地支關系

          for item in zhis:

              for type_ in zhi_atts[zhi_]:
                  if item in zhi_atts[zhi_][type_]:
                      zhi__.add(type_ + ":" + item)
          zhi__ = '  '.join(zhi__)

          empty = chr(12288)
          if zhi_ in empties[zhus[2]]:
              empty = '空'

          jia = ""
          if gan_ in gans:
              for i in range(4):
                  if gan_ == gans[i]:
                      if abs(Zhi.index(zhi_) - Zhi.index(zhis[i])) == 2:
                          jia = jia + "  --夾：" +  Zhi[( Zhi.index(zhi_) + Zhi.index(zhis[i]) )//2]
                      if abs( Zhi.index(zhi_) - Zhi.index(zhis[i]) ) == 10:
                          jia = jia + "  --夾：" +  Zhi[(Zhi.index(zhi_) + Zhi.index(zhis[i]))%12]

          out = "{1:<4d}{2:<5s}{3} {15} {14} {13}  {4}:{5}{8}{6:{0}<6s}{12}{7}{8}{9} - {10:{0}<10s} {11}".format(
              chr(12288), dayun.getStartAge(), '', dayun.getGanZhi(),ten_deities[me][gan_], gan_,check_gan(gan_, gans),
              zhi_, yinyang(zhi_), ten_deities[me][zhi_], zhi5_, zhi__,empty, fu, nayins[(gan_, zhi_)], ten_deities[me][zhi_])
          gan_index = Gan.index(gan_)
          zhi_index = Zhi.index(zhi_)
          out = out + jia + get_shens(gans, zhis, gan_, zhi_, me)

          rndrCode(out)
          zhis2 = list(zhis) + [zhi_]
          gans2 = list(gans) + [gan_]
          for liunian in dayun.getLiuNian():
              gan2_ = liunian.getGanZhi()[0]
              zhi2_ = liunian.getGanZhi()[1]
              fu2 = '*' if (gan2_, zhi2_) in zhus else " "
              #rndrCode(fu2, (gan2_, zhi2_),zhus)

              zhi6_ = ''
              for gan in zhi5[zhi2_]:
                  zhi6_ = zhi6_ + "{}{}　".format(gan, ten_deities[me][gan])

              # 大運地支關系
              zhi__ = set() # 大運地支關系
              for item in zhis2:

                  for type_ in zhi_atts[zhi2_]:
                      if type_ == '破':
                          continue
                      if item in zhi_atts[zhi2_][type_]:
                          zhi__.add(type_ + ":" + item)
              zhi__ = '  '.join(zhi__)

              empty = chr(12288)
              if zhi2_ in empties[zhus[2]]:
                  empty = '空'
              out = "{1:>3d} {2:<5d}{3} {15} {14} {13}  {4}:{5}{8}{6:{0}<6s}{12}{7}{8}{9} - {10:{0}<10s} {11}".format(
                  chr(12288), liunian.getAge(), liunian.getYear(), gan2_+zhi2_,ten_deities[me][gan2_], gan2_,check_gan(gan2_, gans2),
                  zhi2_, yinyang(zhi2_), ten_deities[me][zhi2_], zhi6_, zhi__,empty, fu2, nayins[(gan2_, zhi2_)], ten_deities[me][zhi2_])

              jia = ""
              if gan2_ in gans2:
                  for i in range(5):
                      if gan2_ == gans2[i]:
                          zhi1 = zhis2[i]
                          if abs(Zhi.index(zhi2_) - Zhi.index(zhis2[i])) == 2:
                              # rndrCode(2, zhi2_, zhis2[i])
                              jia = jia + "  --夾：" +  Zhi[( Zhi.index(zhi2_) + Zhi.index(zhis2[i]) )//2]
                          if abs( Zhi.index(zhi2_) - Zhi.index(zhis2[i]) ) == 10:
                              # rndrCode(10, zhi2_, zhis2[i])
                              jia = jia + "  --夾：" +  Zhi[(Zhi.index(zhi2_) + Zhi.index(zhis2[i]))%12]

                          if (zhi1 + zhi2_ in gong_he) and (gong_he[zhi1 + zhi2_] not in zhis):
                              jia = jia + "  --拱：" + gong_he[zhi1 + zhi2_]

              out = out + jia + get_shens(gans, zhis, gan2_, zhi2_, me)
              all_zhis = set(zhis2) | set(zhi2_)
              if set('戌亥辰巳').issubset(all_zhis):
                  out = out + "  天羅地網：戌亥辰巳"
              if set('寅申巳亥').issubset(all_zhis) and len(set('寅申巳亥')&set(zhis)) == 2 :
                  out = out + "  四生：寅申巳亥"
              if set('子午卯酉').issubset(all_zhis) and len(set('子午卯酉')&set(zhis)) == 2 :
                  out = out + "  四敗：子午卯酉"
              if set('辰戌丑未').issubset(all_zhis) and len(set('辰戌丑未')&set(zhis)) == 2 :
                  out = out + "  四庫：辰戌丑未"
              rndrCode(out)



      # 計算星宿
      d2 = date(1, 1, 4)
      rndrCode(["星宿", lunar.getXiu(), lunar.getXiuSong()])

      # 計算建除
      seq = 12 - Zhi.index(zhis.month)
      rndrCode(jianchus[(Zhi.index(zhis.day) + seq)%12])

  # 檢查三會 三合的拱合
  result = ''
  #for i in range(2):
      #result += check_gong(zhis, i*2, i*2+1, me, gong_he)
      #result += check_gong(zhis, i*2, i*2+1, me, gong_hui, '三會拱')

  result += check_gong(zhis, 1, 2, me, gong_he)
  result += check_gong(zhis, 1, 2, me, gong_hui, '三會拱')

  if result:
      rndrCode(result)

  rndrCode("="*120)



  # 格局分析
  ge = ''
  if (me, zhis.month) in jianlus:
      rndrCode(jianlu_desc)
      rndrCode("-"*120)
      rndrCode(jianlus[(me, zhis.month)])
      rndrCode("-"*120 + "\n")
      ge = '建'
  #elif (me == '丙' and ('丙','申') in zhus) or (me == '甲' and ('己','巳') in zhus):
      #rndrCode("格局：專財. 運行官旺 財神不背,大發財官。忌行傷官、劫財、衝刑、破祿之運。喜身財俱旺")
  elif (me, zhis.month) in (('甲','卯'), ('庚','酉'), ('壬','子')):
      ge = '月刃'
  else:
      zhi = zhis[1]
      if zhi in wuhangs['土'] or (me, zhis.month) in (('乙','寅'), ('丙','午'),  ('丁','巳'), ('戊','午'), ('己','巳'), ('辛','申'), ('癸','亥')):
          for item in zhi5[zhi]:
              if item in gans[:2] + gans[3:]:
                  ge = ten_deities[me][item]
      else:
          d = zhi5[zhi]
          ge = ten_deities[me][max(d, key=d.get)]

  # 天乙貴人
  flag = False
  for items in tianyis[me]:
      for item in items:
          if item in zhis:
              if not flag:
                  rndrCode("| 天乙貴人：")
                  flag = True
              rndrCode(item)

  # 玉堂貴人
  flag = False
  for items in yutangs[me]:
      for item in items:
          if item in zhis:
              if not flag:
                  rndrCode("| 玉堂貴人：")
                  flag = True
              rndrCode(item)

  # 天羅
  if  nayins[zhus[0]][-1] == '火':			
      if zhis.day in '戌亥':
          rndrCode("| 天羅：{}".format(zhis.day))

  # 地網		
  if  nayins[zhus[0]][-1] in '水土':			
      if zhis.day in '辰巳':
          rndrCode("| 地網：{}".format(zhis.day)) 		



  # 學堂分析
  for seq, item in enumerate(statuses):
      if item == '長':
        rndrCode(["學堂:", zhis[seq], "\t"])
        if  nayins[zhus[seq]][-1] == ten_deities[me]['本']:
          rndrCode(f"正學堂:{nayins[zhus[seq]]}")

  #xuetang = xuetangs[ten_deities[me]['本']][1]
  #if xuetang in zhis:
      #rndrCode("學堂:", xuetang, "\t\t")
      #if xuetangs[ten_deities[me]['本']] in zhus:
          #rndrCode("正學堂:", xuetangs[ten_deities[me]['本']], "\t\t")

  # 學堂分析

  for seq, item in enumerate(statuses):
      if item == '建':
          rndrCode("| 詞館:", zhis[seq])
          if  nayins[zhus[seq]][-1] == ten_deities[me]['本']:
              rndrCode("- 正詞館:", nayins[zhus[seq]])


  ku = ten_deities[me]['庫'][0]
  if ku in zhis:
      rndrCode(f"庫：{ku}")

      for item in zhus:
          if ku != zhus[1]:
              continue
          if nayins[item][-1] == ten_deities[me]['克']:
              rndrCode("庫中有財，其人必豐厚")
          if nayins[item][-1] == ten_deities[me]['被克']:
              rndrCode(item, ten_deities[me]['被克'])
              rndrCode("絕處無依，其人必滞")

  # 天元分析
  for item in zhi5[zhis[2]]:
      name = ten_deities[me][item]
      rndrCode(self_zuo[name])
  rndrCode("-"*120)


  # 出身分析
  cai = ten_deities[me].inverse['財']
  guan = ten_deities[me].inverse['官']
  jie = ten_deities[me].inverse['劫']
  births = tuple(gans[:2])
  if cai in births and guan in births:
      birth = '不錯'
  #elif cai in births or guan in births:
      #birth = '較好'
  else:
      birth = '一般'

  rndrCode(f"出身:{birth}")

  guan_num = shens.count("官")
  sha_num = shens.count("殺")
  cai_num = shens.count("財")
  piancai_num = shens.count("才")
  jie_num = shens.count("劫")
  bi_num = shens.count("比")
  yin_num = shens.count("印")

  # 食神分析
  if ge == '食':
      rndrCode("****食神分析****: 格要日主食神俱生旺，無衝破。有財輔助財有用。  食神可生偏財、克殺")
      rndrCode("陽日食神暗官星，陰日食神暗正印。食神格人聰明、樂觀、優雅、多才多藝。食居先，煞居後，功名顯達。")
      rndrCode("======================================")
      rndrCode('''
      喜:身旺 宜行財鄉 逢食看財  忌:身弱 比 倒食(偏印)  一名進神　　二名爵星　　三名壽星
      月令建祿最佳，時祿次之，更逢貴人運
      ''')

      shi_num = shens.count("食")
      if shi_num > 2:
          rndrCode("食神過多:食神重見，變爲傷官，令人少子，縱有，或帶破拗性. 行印運")
      if set(('財','食')) in set(gan_shens[:2] + zhi_shens[:2]):
          rndrCode("祖父蔭業豐隆")
      if set(('財','食')) in set(gan_shens[2:] + zhi_shens[2:]):
          rndrCode("妻男獲福，怕母子俱衰絕，兩皆無成")
      if cai_num >1:
          rndrCode("財多則不清，富而已")

      for seq, item in enumerate(gan_shens):
          if item == '食':
              if ten_deities[gans[seq]][zhis[seq]] == '墓':
                  rndrCode("食入墓，即是傷官入墓，住壽難延。")


      for seq, item in enumerate(gan_shens):
          if item == '食' or zhi_shens[seq] == '食':
              if get_empty(zhus[2],zhis[seq]):
                  rndrCode("大忌空亡，更有官煞顯露，爲太醫師巫術數九流之士，若食神逢克，又遇空亡，則不貴，再行死絕或枭運，則因食上氣上生災，翻胃噎食，缺衣食，忍飢寒而已")

      # 倒食分析
      if '枭' in shens and (me not in ['庚', '辛','壬']) and ten_deities[me] != '建':
          flag = True
          for item in zhi5[zhis.day]:
              if ten_deities[me]['合'] == item:
                  flag = False
                  break
          if flag:
              rndrCode("倒食:凡命帶倒食，福薄壽夭，若有制合沒事，主要爲地支爲天干的殺;日支或者偏印的坐支爲日主的建祿狀態。偏印和日支的主要成分天干合")
              rndrCode("凡命有食遇枭，猶尊長之制我，不得自由，作事進退悔懶，有始無終，財源屢成屢敗，容貌欹斜，身品瑣小，膽怯心虛，凡事無成，克害六親，幼時克母，長大傷妻子")
              rndrCode("身旺遇此方爲福")
      rndrCode("-"*120)

  # 傷官分析
  if ge == '傷':
      rndrCode("\n****傷官分析****: 喜:身旺,財星,印绶,傷盡 忌:身弱,無財,刑衝,入墓枭印　")
      rndrCode(" 多材藝，傲物氣高，心險無忌憚，多謀少遂，弄巧成拙，常以天下之人不如己，而人亦憚之、惡之。 一名剝官神　　二名羊刃煞")
      rndrCode(" 身旺用財，身弱用印。用印不忌諱官煞。用印者須去財方能發福")
      rndrCode("官星隱顯，傷之不盡，歲運再見官星，官來乘旺，再見刑衝破害，刃煞克身，身弱財旺，必主徒流死亡，五行有救，亦殘疾。若四柱無官而遇傷煞重者，運入官鄉，歲君又遇，若不目疾，必主災破。")
      rndrCode("嬌貴傷不起、謹慎過頭了略顯膽小，節儉近于吝啬")
      rndrCode("======================================")

      if '財' in shens or '才' in shens:
          rndrCode("傷官生財")
      else:
          rndrCode("傷官無財，主貧窮")

      if '印' in shens or '枭' in shens:
          rndrCode('印能制傷，所以爲貴，反要傷官旺，身稍弱，始爲秀氣;印旺極深，不必多見，偏正叠出，反爲不秀，故傷輕身重而印绶多見，貧窮之格也。')
          if '財' in shens or '才' in shens:
              rndrCode('財印相克，本不并用，只要干頭兩清而不相礙；又必生財者，財太旺而帶印，佩印者印太重而帶財，調停中和，遂爲貴格')
      if ('官' in shens) :
          rndrCode(shang_guans[ten_deities[me]['本']])
          rndrCode('金水獨宜，然要財印爲輔，不可傷官并透。若冬金用官，而又化傷爲財，則尤爲極秀極貴。若孤官無輔，或官傷并透，則發福不大矣。')
      if ('殺' in shens) :
          rndrCode("煞因傷而有制，兩得其宜，只要無財，便爲貴格")
      if gan_shens[0] == '傷':
          rndrCode("年干傷官最重，謂之福基受傷，終身不可除去，若月支更有，甚于傷身七煞")

      for seq, item in enumerate(gan_shens):
          if item == '傷':
              if ten_deities[gans[seq]][zhis[seq]] == '墓':
                  rndrCode("食入墓，即是傷官入墓，住壽難延。")


      for seq, item in enumerate(gan_shens):
          if item == '食' or zhi_shens[seq] == '食':
              if get_empty(zhus[2],zhis[seq]):
                  rndrCode("大忌空亡，更有官煞顯露，爲太醫師巫術數九流之士，若食神逢克，又遇空亡，則不貴，再行死絕或枭運，則因食上氣上生災，翻胃噎食，缺衣食，忍飢寒而已")
      rndrCode()
      rndrCode("-"*120)

  # 劫財分析
  if ge == '劫':
      rndrCode("\n****劫財(陽刃)分析****：陽刃衝合歲君,勃然禍至。身弱不作兇。")
      rndrCode("======================================")
      if "劫" == gan_shens[3] or "劫" == zhi_shens[3]:
          rndrCode("劫財陽刃,切忌時逢,歲運并臨,災殃立至,獨陽刃以時言,重于年月日也。")

      shi_num = shens.count("食")
      rndrCode("-"*120)

  # 財分析

  if ge == '財' or ge == '才':
      rndrCode("\n****財分析 **** 喜:旺,印,食,官 忌:比 羊刃 空絕 衝合   財星,天馬星,催官星,壯志神")
      if gan_shens.count('財') + gan_shens.count('才') > 1:
          rndrCode('財喜根深，不宜太露，然透一位以清用，格所最喜，不爲之露。即非月令用神，若寅透乙、卯透甲之類，一亦不爲過，太多則露矣。')
          rndrCode('財旺生官，露亦不忌，蓋露不忌，蓋露以防劫，生官則劫退，譬如府庫錢糧，有官守護，即使露白，誰敢劫之？')
      if '傷' in gan_shens:
          rndrCode("有傷官，財不能生官")
      if '食' in shens:
          rndrCode("有財用食生者，身強而不露官，略帶一位比劫，益覺有情")
          if '印' in shens or '枭' in 'shens':
              rndrCode("注意印食衝突")
      if '比' in shens:
          rndrCode("比不吉，但是傷官食神可化!")
      if '殺' in shens:
          rndrCode("不論合煞制煞，運喜食傷身旺之方!")

      if "財" == zhi_shens[0]:
          rndrCode("歲帶正馬：月令有財或傷食，不犯刑衝分奪，旺祖業豐厚。同類月令且帶比，或遇運行傷劫 貧")
      if "財" == zhi_shens[3]:
          rndrCode("時帶正馬：無衝刑破劫，主招美妻，得外來財物，生子榮貴，財產豐厚，此非父母之財，乃身外之財，招來產業，宜儉不宜奢。")
      if "財" == zhi_shens[2] and (me not in ('壬','癸')):
          rndrCode("天元坐財：喜印食 畏官煞，喜月令旺 ")
      if ('官' not in shens) and ('傷' not in shens) and ('食' not in shens):
          rndrCode("財旺生官:若月令財無損克，亦主登科")


      if cai_num > 2 and ('劫' not in shens) and ('比' not in shens) \
         and ('比' not in shens) and ('印' not in shens):
          rndrCode("財　不重叠多見　財多身弱，柱無印助; 若財多身弱，柱無印助不爲福。")

      if '印' in shens:
          rndrCode("先財後印，反成其福，先印後財，反成其辱是也?")
      if '官' in gan_shens:
          rndrCode("官星顯露，別無傷損，或更食生印助日主健旺，富貴雙全")
      if '財' in gan_shens and (('劫' not in shens) and ('比' not in shens)):
          rndrCode("財不宜明露")
      for seq, item in enumerate(gan_shens):
          if item == '財':
              if ten_deities[gans[seq]][zhis[seq]] == '墓':
                  rndrCode("財星入墓，必定刑妻")
              if ten_deities[gans[seq]][zhis[seq]] == '長':
                  rndrCode("財遇長生，田園萬頃")

      if ('官' not in shens) and (('劫' in shens) or ('比' in shens)):
          rndrCode("切忌有姊妹兄弟分奪，柱無官星，禍患百出。")

      if bi_num + jie_num > 1:
          rndrCode("兄弟輩出: 縱入官鄉，發福必渺.")

      for seq, item in enumerate(zhi_shens):
          if item == '才' or ten_deities[me][zhis[seq]] == '才':
              if get_empty(zhus[2],zhis[seq]):
                  rndrCode("空亡 官將不成，財將不住")

      rndrCode("-"*120)

  # 財庫分析
  if ten_deities[ten_deities[me].inverse["財"]]['庫'][-1] in zhis:
      rndrCode("財臨庫墓: 一生財帛豐厚，因財致官, 天干透土更佳")
  if cai_num < 2 and (('劫' in shens) or ('比' in shens)):
      rndrCode("財少身強，柱有比劫，不爲福")




  # 官分析
  if ge == "官":
      rndrCode("\n**** 官分析 ****\n 喜:身旺 財印   忌：身弱 偏官 傷官 刑衝 泄氣 貪合 入墓")
      rndrCode("一曰正官 二曰祿神 最忌刑衝破害、傷官七煞，貪合忘官，劫財比等等，遇到這些情況便成爲破格 財印并存要分開")
      rndrCode("運：財旺印衰喜印，忌食傷生財；旺印財衰喜財，喜食傷生財；帶傷食用印制；")
      rndrCode("帶煞傷食不礙。劫合煞財運可行，傷食可行，身旺，印绶亦可行；傷官合煞，則傷食與財俱可行，而不宜逢印")
      rndrCode("======================================")
      if guan_num > 1:
          rndrCode("官多變殺，以干爲準")
      if "財" in shens and "印" in shens and ("傷" not in shens) and ("殺" not in shens):
          rndrCode("官星通過天干顯露出來，又得到財、印兩方面的扶持，四柱中又沒有傷煞，行運再引到官鄉，是大富大貴的命。")
      if "財" in shens or '才' in shens:
          rndrCode("有財輔助")
      if "印" in shens or "枭" in shens:
          rndrCode("有印輔助　正官帶傷食而用印制，運喜官旺印旺之鄉，財運切忌。若印绶叠出，財運亦無害矣。")
      if "食" in shens:
          rndrCode("又曰凡論官星，略見一位食神坐實，便能損局，有殺則無妨。惟月令隱祿，見食卻爲三奇之貴。因爲食神和官相合。")
      if "傷" in shens:
          rndrCode("傷官需要印或偏印來抑制，　有殺也無妨")
      if "殺" in shens:
          rndrCode("傷官需要印或偏印來抑制。用劫合煞，則財運可行，傷食可行，身旺，印绶亦可行，只不過復露七煞。若命用傷官合煞，則傷食與財俱可行，而不宜逢印矣。")

      if zhi_shens[2] in ("財","印"):
          rndrCode("凡用官，日干自坐財印，終顯")
      if zhi_shens[2] in ("傷","殺"):
          rndrCode("自坐傷、煞，終有節病")



      # 檢查天福貴人
      if (guan, ten_deities[guan].inverse['建']) in zhus:
          rndrCode("天福貴人:主科名巍峨，官職尊崇，多掌絲綸文翰之美!")

      # 天元坐祿
      if guan in zhi5[zhis[2]]:
          rndrCode("天元作祿: 日主與官星并旺,才是貴命。大多不貴即富,即使是命局中有缺點,行到好的大運時,便能一發如雷。")
          rndrCode(tianyuans[ten_deities[me]['本']])

      # 歲德正官
      if gan_shens[0] == '官' or zhi_shens[0] == '官':
          rndrCode("歲德正官: 必生宦族,或蔭襲祖父之職,若月居財官分野,運向財官旺地,日主健旺,貴無疑矣。凡年干遇官,福氣最重,發達必早。")

      # 時上正官
      if gan_shens[0] == '官' or zhi_shens[0] == '官':
          rndrCode("時上正官: 正官有用不須多，多則傷身少則和，日旺再逢生印绶，定須平步擢高科。")

      rndrCode()
      rndrCode("-"*120)
  # 官庫分析
  if ten_deities[ten_deities[me].inverse["官"]]['庫'][-1] in zhis:
      rndrCode("官臨庫墓")
      if lu_ku_cai[me] in zhis:
          rndrCode("官印祿庫: 有官庫，且庫中有財")

  # 殺(偏官)分析
  if ge == "殺":
      rndrCode("\n殺(偏官)分析 **** 喜:身旺  印绶  合煞  食制 羊刃  比  逢煞看印及刃  以食爲引   忌：身弱  財星  正官  刑衝  入墓")
      rndrCode("一曰偏官 二曰七煞 三曰五鬼 四曰將星 五曰孤極星 原有制伏,煞出爲福,原無制伏,煞出爲禍   性情如虎，急躁如風,尤其是七殺爲丙、丁火時。")
      rndrCode("坐長生、臨官、帝旺,更多帶比同類相扶,則能化鬼爲官,化煞爲權,行運引至印鄉,必發富貴。倘歲運再遇煞地,禍不旋踵。")
      rndrCode("七殺喜酒色而偏爭好斗、愛軒昂而扶弱欺強")
      rndrCode("======================================")
      if "財" in shens:
          rndrCode("逢煞看財,如身強煞弱,有財星則吉,身弱煞強,有財引鬼盜氣,非貧則夭;")
      if "比" in shens:
          rndrCode("如果比比自己弱，可以先挨殺。")
      if "食" in shens:
          rndrCode("有食神透制,即《經》云:一見制伏,卻爲貴本")
          if "財" in shens or "印" in shens or '才' in shens or "枭" in shens:
              rndrCode("煞用食制，不要露財透印，以財能轉食生煞，而印能去食護煞也。然而財先食後，財生煞而食以制之，或印先食後，食太旺而印制，則格成大貴。")
      if "劫" in shens:
          rndrCode("有陽刃配合,即《經》云:煞無刃不顯,逢煞看刃是也。")
      if "印" in shens:
          rndrCode("印: 則煞生印，印生身")
      if sha_num > 1:
          rndrCode("七煞重逢")
          if weak:
              rndrCode("棄命從煞，須要會煞從財.四柱無一點比印绶方論，如遇運扶身旺，與煞爲敵，從煞不專，故爲禍患")
              rndrCode("陰干從地支，煞純者多貴，以陰柔能從物也。陽干從地支，煞純者亦貴，但次于陰，以陽不受制也。")
              rndrCode("水火金土皆從，惟陽木不能從，死木受斧斤，反遭其傷故也。")
              rndrCode("古歌曰：五陽坐日全逢煞，棄命相從壽不堅，如是五陰逢此地，身衰煞旺吉堪言。")
      if "殺" == zhi_shens[2]:
          rndrCode("爲人心多性急，陰險懷毒，僭僞謀害，不近人情")
      if "殺" == zhi_shens[3] or "殺" == gan_shens[3]:
          rndrCode(" 時殺：月制干強，其煞反爲權印。《經》云：時上偏官身要強，陽刃、衝刑煞敢當，制多要行煞旺運，煞多制少必爲殃。")
          rndrCode(" 一位爲妙，年、月、日重見，反主辛苦勞碌。若身旺，煞制太過，喜行煞旺運，或三合煞運，如無制伏，要行制伏運方發。但忌身弱，縱得運扶持發福，運過依舊不濟。")
          rndrCode("《獨步》云：時上一位，貴藏在支中，是日，主要旺強名利，方有氣。")
          rndrCode("《古歌》云：時上偏官喜刃衝，身強制伏祿豐隆。正官若也來相混，身弱財多主困窮。")
          rndrCode("時上偏官一位強，日辰自旺喜非常。有財有印多財祿，定是天生作棟梁。")
          rndrCode("煞臨子位，必招悖逆之兒。")

      if "殺" == zhi_shens[0]:
          rndrCode(" 年上七煞：出身寒微，命有貴子。")
          rndrCode("歲煞一位不宜制，四柱重見卻宜制，日主生旺，制伏略多，喜行煞旺地，制伏太過，或煞旺身衰，官煞混雜，歲運如之，碌碌之輩。若制伏不及，運至身衰煞旺鄉，必生禍患。")
          rndrCode("《獨步》云：時上一位，貴藏在支中，是日，主要旺強名利，方有氣。")
          rndrCode("《古歌》云：時上偏官喜刃衝，身強制伏祿豐隆。正官若也來相混，身弱財多主困窮。")
          rndrCode("時上偏官一位強，日辰自旺喜非常。有財有印多財祿，定是天生作棟梁。")
      if ('官' in shens) :
          rndrCode("官煞混雜：身弱多夭貧")

      for seq, item in enumerate(gan_shens):
          if item == '殺':
              if ten_deities[gans[seq]][zhis[seq]] == '長':
                  rndrCode("七煞遇長生乙位，女招貴夫。")
      rndrCode()
      rndrCode("-"*120)

  # 印分析
  if ge == "印":
      rndrCode("\n印分析 **** 喜:食神 天月德 七煞 逢印看煞 以官爲引   忌： 刑衝 傷官 死墓 辰戊印怕木 丑未印不怕木")
      rndrCode("一曰正印 二曰魁星 三曰孫極星")
      rndrCode("以印绶多者爲上,月最要,日時次之,年干雖重,須歸祿月、日、時,方可取用,若年露印,月日時無,亦不濟事。")
      rndrCode("======================================")
      if "官" in shens:
          rndrCode("官能生印。身旺印強，不愁太過，只要官星清純")
      if "殺" in shens:
          rndrCode("喜七煞,但煞不可太多,多則傷身。原無七煞,行運遇之則發;原有七煞,行財運,或印绶死絕,或臨墓地,皆兇。")
      if "傷" in shens or "食" in shens:
          rndrCode("傷食：身強印旺，恐其太過，泄身以爲秀氣；若印淺身輕，而用層層傷食，則寒貧之局矣。")
      if "財" in shens or "才" in shens:
          rndrCode("有印多而用財者，印重身強，透財以抑太過，權而用之，只要根深，無防財破。 若印輕財重，又無劫財以救，則爲貪財破印，貧賤之局也。")

      if yin_num > 1:
          rndrCode("印绶復遇拱祿、專祿、歸祿、鼠貴、夾貴、時貴等格,尤爲奇特,但主少子或無子,印绶多者清孤。")
      if "劫" in shens:
          rndrCode("化印爲劫；棄之以就財官")
      rndrCode()
      rndrCode("-"*120)

  # 偏印分析
  if ge == "枭":
      rndrCode("\n印分析 **** 喜:食神 天月德 七煞 逢印看煞 以官爲引   忌： 刑衝 傷官 死墓 辰戊印怕木 丑未印不怕木")
      rndrCode("一曰正印 二曰魁星 三曰孫極星")
      rndrCode("以印绶多者爲上,月最要,日時次之,年干雖重,須歸祿月、日、時,方可取用,若年露印,月日時無,亦不濟事。")
      rndrCode("======================================")
      if "官" in shens:
          rndrCode("官能生印。身旺印強，不愁太過，只要官星清純")
      if "殺" in shens:
          rndrCode("喜七煞,但煞不可太多,多則傷身。原無七煞,行運遇之則發;原有七煞,行財運,或印绶死絕,或臨墓地,皆兇。")
      if "傷" in shens or "食" in shens:
          rndrCode("傷食：身強印旺，恐其太過，泄身以爲秀氣；若印淺身輕，而用層層傷食，則寒貧之局矣。")
      if "財" in shens or "才" in shens:
          rndrCode("棄印就財。")

      if yin_num > 1:
          rndrCode("印绶復遇拱祿、專祿、歸祿、鼠貴、夾貴、時貴等格,尤爲奇特,但主少子或無子,印绶多者清孤。")
      if "劫" in shens:
          rndrCode("化印爲劫；棄之以就財官")
      rndrCode()
      rndrCode("-"*120)



  gan_ = tuple(gans)
  for item in Gan:
      if gan_.count(item) == 3:
          rndrCode("三字干：", item, "--", gan3[item])
          break

  gan_ = tuple(gans)
  for item in Gan:
      if gan_.count(item) == 4:
          rndrCode("四字干：", item, "--", gan4[item])
          break

  zhi_ = tuple(zhis)
  for item in Zhi:
      if zhi_.count(item) > 2:
          rndrCode(f"三字支：{item}--{zhi3[item]}")
          break

  rndrCode("="*120)
  rndrCode(f"你屬{me} 特點：--{gan_desc[me]}")
  rndrCode(f"年份:{zhis[0]} 特點：--{zhi_desc[zhis[0]]}")

  # 羊刃分析
  key = '帝' if Gan.index(me)%2 == 0 else '冠'

  if ten_deities[me].inverse[key] in zhis:
      rndrCode("\n羊刃:", me, ten_deities[me].inverse[key])
      rndrCode("======================參考：https://www.jianshu.com/p/c503f7b3ed04")
      if ten_deities[me].inverse['冠']:
          rndrCode("羊刃重重又見祿，富貴饒金玉。 官、印相助福相資。")
      else:
          rndrCode("勞累命！")




  # 將星分析
  me_zhi = zhis[2]
  other_zhis = zhis[:2] + zhis[3:]
  flag = False
  tmp_list = []
  if me_zhi in ("申", "子", "辰"):
      if "子" in other_zhis:
          flag = True
          tmp_list.append((me_zhi, '子'))
  elif me_zhi in ("丑", "巳", "酉"):
      if "酉" in other_zhis:
          flag = True
          tmp_list.append((me_zhi, '酉'))
  elif me_zhi in ("寅", "午", "戌"):
      if "午" in other_zhis:
          flag = True
          tmp_list.append((me_zhi, '午'))
  elif me_zhi in ("亥", "卯", "未"):
      if "卯" in other_zhis:
          flag = True
          tmp_list.append((me_zhi, '卯'))

  if flag:
      rndrCode("\n\n將星: 常欲吉星相扶，貴煞加臨乃爲吉慶。")
      rndrCode("=========================")
      rndrCode('''理愚歌》云：將星若用亡神臨，爲國棟梁臣。言吉助之爲貴，更夾貴庫墓純粹而
      不雜者，出將入相之格也，帶華蓋、正印而不夾庫，兩府之格也；只帶庫墓而帶正印，員郎
      以上，既不帶墓又不帶正印，止有華蓋，常調之祿也；帶華印而正建驿馬，名曰節印，主旌節
      之貴；若歲干庫同庫爲兩重福，主大貴。''')
      rndrCode(tmp_list)

  # 華蓋分析
  flag = False
  if me_zhi in ("申", "子", "辰"):
      if "辰" in other_zhis:
          flag = True
  elif me_zhi in ("丑", "巳", "酉"):
      if "丑" in other_zhis:
          flag = True
  elif me_zhi in ("寅", "午", "戌"):
      if "戌" in other_zhis:
          flag = True
  elif me_zhi in ("亥", "卯", "未"):
      if "未" in other_zhis:
          flag = True

  if flag:
      rndrCode("\n\n華蓋: 多主孤寡，總貴亦不免孤獨，作僧道藝術論。")
      rndrCode("=========================")
      rndrCode('''《理愚歌》云：華蓋雖吉亦有妨，或爲孽子或孤孀。填房入贅多阙口，爐鉗頂笠拔缁黃。
      又云：華蓋星辰兄弟寡，天上孤高之宿也；生來若在時與胎，便是過房庶出者。''')


  # 咸池 桃花
  flag = False
  taohuas = []
  year_zhi = zhis[0]
  if me_zhi in ("申", "子", "辰") or year_zhi in ("申", "子", "辰"):
      if "酉" in zhis:
          flag = True
          taohuas.append("酉")
  elif me_zhi in ("丑", "巳", "酉") or year_zhi in ("丑", "巳", "酉"):
      if "午" in other_zhis:
          flag = True
          taohuas.append("午")
  elif me_zhi in ("寅", "午", "戌") or year_zhi in ("寅", "午", "戌"):
      if "卯" in other_zhis:
          flag = True
          taohuas.append("卯")
  elif me_zhi in ("亥", "卯", "未") or year_zhi in ("亥", "卯", "未"):
      if "子" in other_zhis:
          flag = True
          taohuas.append("子")

  if flag:
      rndrCode("\n\n咸池(桃花): 牆裏桃花，煞在年月；牆外桃花，煞在日時；")
      rndrCode("=========================")
      rndrCode('''一名敗神，一名桃花煞，其神之奸邪淫鄙，如生旺則美容儀，耽酒色，疏財好歡，
      破散家業，唯務貪淫；如死絕，落魄不檢，言行狡詐，遊蕩賭博，忘恩失信，私濫奸淫，
      靡所不爲；與元辰并，更臨生旺者，多得匪人爲妻；與貴人建祿并，多因油鹽酒貨得生，
      或因婦人暗昧之財起家，平生有水厄、痨瘵之疾，累遭遺失暗昧之災。此人入命，有破無成，
      非爲吉兆，婦人尤忌之。
      咸池非吉煞，日時與水命遇之尤兇。''')
      rndrCode(taohuas, zhis)

  # 祿分析
  flag = False
  for item in zhus:
      if item in lu_types[me]:
          if not flag:
              rndrCode("\n\n祿分析:")
              rndrCode("=========================")	
          rndrCode(item,lu_types[me][item])


  # 文星貴人
  if wenxing[me] in zhis:
    rndrCode(f"文星貴人: {me} {wenxing[me]}")

  # 天印貴人
  if tianyin[me] in zhis:
    rndrCode(f"天印貴人: 此號天印貴，榮達受皇封 {me} {tianyin[me]}")


  short = min(scores, key=scores.get)
  rndrCode(f"五行缺{short}的建議參見 http://t.cn/E6zwOMq")
  if '殺' in shens:
    if yinyang(me) == '+': rndrCode("陽殺:話多,熱情外向,異性緣好")
    else: rndrCode("陰殺:話少,性格柔和")
  if '印' in shens and '才' in shens and '官' in shens: rndrCode("印,偏財,官:三奇 怕正財")
  if '才' in shens and '殺' in shens: rndrCode("男:因女致禍、因色致禍; 女:賠貨")
  if '才' in shens and '枭' in shens: rndrCode("偏印因偏財而不懶！")
