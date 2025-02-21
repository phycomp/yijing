from stUtil import rndrCode
#!/usr/bin/env python
HEXA={'111111': '乾', '000000': '坤', '010001': '屯', '100010': '蒙', '010111': '需', '111010': '訟', '000010': '師', '010000': '比', '110111': '小畜', '111011': '履', '000111': '泰', '111000': '否', '111101': '同人', '101111': '大有', '000100': '謙', '001000': '豫', '011001': '隨', '100110': '蠱', '000011': '臨', '110000': '觀', '101001': '噬嗑', '100101': '賁', '100000': '剝', '000001': '復', '111001': '無妄', '100111': '大畜', '100001': '頤', '011110': '大過', '010010': '坎', '101101': '離', '011100': '咸', '001110': '恆', '111100': '遁', '001111': '大壯', '101000': '晉', '000101': '明夷', '110101': '家人', '101011': '睽', '010100': '蹇', '001010': '解', '100011': '損', '110001': '益', '011111': '夬', '111110': '姤', '011000': '萃', '000110': '升', '011010': '困', '010110': '井', '011101': '革', '101110': '鼎', '001001': '震', '100100': '艮', '110100': '漸', '001011': '歸妹', '001101': '豐', '101100': '旅', '110110': '巽', '011011': '兌', '110010': '渙', '010011': '節', '110011': '中孚', '001100': '小過', '010101': '既濟', '101010': '未濟'}
hexaAttrs=['111111', '000000', '010001', '100010', '010111', '111010', '000010', '010000', '110111', '111011', '000111', '111000', '111101', '101111', '000100', '001000', '011001', '100110', '000011', '110000', '101001', '100101', '100000', '000001', '111001', '100111', '100001', '011110', '010010', '101101', '011100', '001110', '111100', '001111', '101000', '000101', '110101', '101011', '010100', '001010', '100011', '110001', '011111', '111110', '011000', '000110', '011010', '010110', '011101', '101110', '001001', '100100', '110100', '001011', '001101', '101100', '110110', '011011', '110010', '010011', '110011', '001100', '010101', '101010']

def allHexa():#Negation():
    for hexa in hexaAttrs:
        negation=hexa.replace('1','x').replace('0','1').replace('x','0')
        ngtnHexaName=HEXA[negation]
        #print(ngtnHexaName,negation)
        opposite=hexa[::-1]
        oppHexaName=HEXA[opposite]
        cross=hexa[1:4]+hexa[2:5]
        crossHexaName=HEXA[cross]
        cRoss=hexa[1:4]+hexa[2:5]
        crossOpp=cRoss[::-1]
        crossOppHexaName=HEXA[crossOpp]
        rndrCode(ngtnHexaName,negation,oppHexaName,opposite,crossHexaName,cross,crossOppHexaName,crossOpp)
allHexa()
#Negation()
def Opposite():
    for hexa in hexaAttrs:
        opposite=hexa[::-1]
        oppHexaName=HEXA[opposite]
        rndrCode(oppHexaName,opposite)
#Opposite()
def Cross():
    for hexa in hexaAttrs:
        cross=hexa[1:4]+hexa[2:5]
        crossHexaName=HEXA[cross]
        rndrCode(crossHexaName,cross)
#Cross()
def CrossOppst():
    for hexa in hexaAttrs:
        cRoss=hexa[1:4]+hexa[2:5]
        crossOpp=cRoss[::-1]
        crossOppHexaName=HEXA[crossOpp]
        rndrCode(crossOppHexaName,crossOpp)
