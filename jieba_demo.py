# encoding=utf-8
import jieba
import paddle

paddle.enable_static()
jieba.enable_paddle()# 启动paddle模式。 0.40版之后开始支持，早期版本不支持
strs=["我来到北京清华大学","乒乓球拍卖完了","中国科学技术大学"]
for str in strs:
    seg_list = jieba.cut(str,use_paddle=True) # 使用paddle模式
    print("Paddle Mode: " + '/'.join(list(seg_list)))

seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print(", ".join(seg_list))

seg_list = jieba.cut_for_search("北京市电信工程设计院有限公司广州分公司")  # 搜索引擎模式
print(", ".join(seg_list))

seg_list = jieba.cut("北京市电信工程设计院有限公司广州分公司")  # 默认是精确模式
print(", ".join(seg_list))

import jieba.posseg as pseg
words = pseg.cut("我爱北京天安门",use_paddle=True) #paddle模式
for word, flag in words:
   print('%s %s' % (word, flag))

words = pseg.cut("广东华科大建筑技术开发有限公司",use_paddle=False) #paddle模式
for word, flag in words:
   print('%s %s' % (word, flag))

words = pseg.cut("北京市电信工程设计院有限公司广州分公司", use_paddle=False)  # paddle模式
for word, flag in words:
    print('%s %s' % (word, flag))

words = pseg.cut("上海景栗信息科技有限公司", use_paddle=False)  # paddle模式
for word, flag in words:
    print('%s %s' % (word, flag))

words = pseg.cut("云南牟定兴宏铜业有限公司", use_paddle=False)  # paddle模式
for word, flag in words:
        print('%s %s' % (word, flag))

result = jieba.tokenize(u'永和服装饰品有限公司')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))


import companynameparser
r = companynameparser.parse("北京市电信工程设计院有限公司广州分公司")
print(r)
print(companynameparser.parse("北京市电信工程设计院有限公司广州分公司").get('place'))
print(companynameparser.parse("北京市电信工程设计院有限公司广州分公司").get('brand'))
print(companynameparser.parse("北京市电信工程设计院有限公司广州分公司").get('trade'))

from cleanco import basename
from cleanco import countrysources, matches
classification_sources = countrysources()
#business_name = "GASOLINERA Y SERVICIOS VILLABONITA, S.A. DE C.V."
business_name = "GASOLINERA Y SERVICIOS VILLABONITA holding"
print('business_name ', basename(basename(business_name)))
print(matches("GASOLINERA Y SERVICIOS VILLABONITA, S.A. DE C.V.", classification_sources))

'''
from pyjyutping import jyutping
canton_py =  jyutping.convert("我係香港人", tone=False)
print('canton_py ', canton_py)
canton_py =  jyutping.convert("董建华", tone=False)
print('canton_py ', canton_py)
canton_py =  jyutping.convert("李嘉诚", tone=False)
print('canton_py ', canton_py)
canton_py =  jyutping.convert("林家栋", tone=False)
print('canton_py ', canton_py)

import pinyin_jyutping_sentence
canton_py_s =   pinyin_jyutping_sentence.jyutping("董建華", tone_numbers=True)
print('canton_py_s ', canton_py_s)
'''

