from fuzzychinese import FuzzyChineseMatch
from fuzzychinese import Radical
from fuzzychinese import Stroke
import pandas as pd
import logging
import logging
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
logging.basicConfig(level=logging.DEBUG)
#test_dict =  pd.Series(['长白朝鲜族自治县','长阳土家族自治县','城步苗族自治县','达尔罕茂明安联合旗','汨罗市','云南省药物研究所'])
#raw_word = pd.Series(['达茂联合旗','长阳县','汩罗市','云南药研所'])
demo_file= './demo_test.csv'
sanction = pd.read_csv(demo_file, encoding='utf-8')
print("sanction with rows", len(sanction))
test_dict = sanction['SanctionName']

#test_dict =  pd.Series(['长白朝鲜族自治县','长阳土家族自治县','城步苗族自治县','达尔罕茂明安联合旗','汨罗市','云南省药物研究所'])
#raw_word = pd.Series(['达茂联合旗','长阳县','汩罗市','云南药研所'])
request_file= './test_requests.csv'
requests = pd.read_csv(request_file, encoding='utf-8')
print("request with rows", len(requests))
raw_word = requests['RequestName']

assert('汩罗市'!='汨罗市') # They are not the same!

fcm = FuzzyChineseMatch(ngram_range=(3, 3), analyzer='radical')
fcm.fit(test_dict)
results = fcm.transform(raw_word, n=2)
#print(sanction)
#print(requests)
#print(raw_word.array)
#print(top2_similar)
#print(fcm.get_similarity_score().T)
#print(fcm.get_index().T)
results_df = pd.DataFrame(results.T, columns=raw_word.array)
results_df_melt = pd.melt(results_df)
results_df_melt.columns = ['RequestName', 'SanctionName']
print(results_df_melt)
similarity_score_df = pd.DataFrame(fcm.get_similarity_score().T, columns=raw_word.array)
similarity_score_melt = pd.melt(similarity_score_df)
similarity_score_melt.columns = ['RequestName', 'similarityScore']
similarity_score_melt = similarity_score_melt.drop('RequestName', 1)
print(similarity_score_melt)
merged = pd.merge(results_df_melt, similarity_score_melt, left_index=True, right_index=True)
#results_df_melt.join(similarity_score_melt, on='RequestName')
#merged['RequestName'] = merged['RequestName'].apply(lambda x: str(x))
#merged.join(requests, on='RequestName')
print(merged)
requests_merged = pd.merge(merged, requests, how="outer", on=["RequestName"])
final = pd.merge(requests_merged, sanction, how="inner", on=["SanctionName"])
print(final)
res = pd.concat([
        #raw_word,
        requests,
        pd.DataFrame(results, columns=['top1', 'top2']),
        pd.DataFrame(
            fcm.get_similarity_score(),
            columns=['top1_score', 'top2_score']),
        pd.DataFrame(
            fcm.get_index(),
            columns=['top1_index', 'top2_index'])],
                    axis=1)
#print(res)
#print(res.iloc[:, 0])
#print(res.top1)
compare = fcm.compare_two_columns(res.iloc[:, 0], res.top1)
#print(compare)
logging.info('Finished')
stroke = Stroke()
radical = Radical()
print("像", stroke.get_stroke("像"))
print("像", radical.get_radical("像"))

