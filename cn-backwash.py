from fuzzychinese import FuzzyChineseMatch
from fuzzychinese import Radical
from fuzzychinese import Stroke
import pandas as pd
import datetime
import logging
from timeit import default_timer as timer

demo_file= './demo_sanction_list.csv'
sanction = pd.read_csv(demo_file, encoding='utf-8')
print("sanction with rows", len(sanction))
test_dict = sanction['Name']

#test_dict =  pd.Series(['长白朝鲜族自治县','长阳土家族自治县','城步苗族自治县','达尔罕茂明安联合旗','汨罗市','云南省药物研究所'])
#raw_word = pd.Series(['达茂联合旗','长阳县','汩罗市','云南药研所'])
request_file= './requests.csv'
requests = pd.read_csv(request_file, encoding='utf-8')[0:20000]
print("request with rows", len(requests))
import hanzidentifier
from hanziconv import HanziConv
requests['RequestName'] = requests['Name'].apply(lambda x: x if hanzidentifier.is_simplified(x) else HanziConv.toSimplified(x))
raw_word = requests['RequestName']

fcm = FuzzyChineseMatch(ngram_range=(3, 3), analyzer='radical')
start = timer()
print("start", datetime.datetime.now())
fcm.fit(test_dict)
print("fit", datetime.datetime.now())
top2_similar = fcm.transform(raw_word, n=20)
print("end: ", datetime.datetime.now())
end = timer()
time_use_s = end - start
#print(raw_word)
#print(fcm.get_index())
similar = pd.DataFrame(top2_similar)
#print(similar.T)
similarity = pd.DataFrame(fcm.get_similarity_score())
#print(similarity.T)
res1 = pd.concat([
        raw_word,
        pd.DataFrame(top2_similar),
        pd.DataFrame(
            fcm.get_similarity_score())],
            axis=1)

#res1.to_csv('CN_double_matches_full.csv')

'''res = pd.concat([
        raw_word,
        pd.DataFrame(top2_similar, columns=['top1', 'top2']),
        pd.DataFrame(
            fcm.get_similarity_score(),
            columns=['top1_score', 'top2_score']),
        pd.DataFrame(
            fcm.get_index(),
            columns=['top1_index', 'top2_index'])],
                    axis=1)
print(res)
'''
print("Total time usage for searching: {}s ({}rows search result)".format(int(time_use_s + 0.5), int(len(top2_similar.T))))
