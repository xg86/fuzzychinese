from fuzzychinese import FuzzyChineseMatch
from fuzzychinese import Radical
from fuzzychinese import Stroke
import pandas as pd
import logging
import logging
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
logging.basicConfig(level=logging.DEBUG)

demo_file= './wc_zh_sanction_dummy_clean.csv'
wc_sanction = pd.read_csv(demo_file, encoding='utf-8')
print("sanction with rows", len(wc_sanction))
wc_sanction.FIRST_NAME = wc_sanction.FIRST_NAME.fillna('')
wc_sanction['SanctionName'] = wc_sanction['LAST_NAME']+wc_sanction['FIRST_NAME']
from pypinyin import lazy_pinyin
wc_sanction['SanctionNamePinYin'] = wc_sanction['SanctionName'].apply(lambda x: ''.join(lazy_pinyin(x)))

from hanziconv import HanziConv

request_file= './cn_p_request.csv'
requests = pd.read_csv(request_file, encoding='utf-8')
print("request with rows", len(requests))
requests.firstName = requests.firstName.fillna('')
requests.lastName = requests.lastName.fillna('')
import re
requests['lastName'] = requests['lastName'].apply(lambda x: re.sub('[!/&]', '', x))
requests['firstName'] = requests['firstName'].apply(lambda x: re.sub('[“”、#-=]', '', x))
requests['wholeName'] = requests['lastName']+requests['firstName']
import hanzidentifier
requests['RequestName'] = requests['wholeName'].apply(lambda x: x if hanzidentifier.is_simplified(x) else HanziConv.toSimplified(x))
requests['RequestNamePinYin'] = requests['RequestName'].apply(lambda x: ''.join(lazy_pinyin(x)))

requests.to_csv('requests_cleaned.csv')
raw_word = requests['RequestName']

fcm = FuzzyChineseMatch(ngram_range=(3, 3), analyzer='radical')
fcm.fit(wc_sanction['SanctionName'])
results = fcm.transform(raw_word, n=10)
#print(sanction)
#print(requests)
#print(raw_word.array)
#print(top2_similar)
#print(fcm.get_similarity_score().T)
#print(fcm.get_index().T)
results_df = pd.DataFrame(results.T, columns=raw_word.array)
results_df_melt = pd.melt(results_df)
results_df_melt.columns = ['RequestName', 'SanctionName']
results_df_melt.to_csv('results_df_melt.csv')

similarity_score_df = pd.DataFrame(fcm.get_similarity_score().T, columns=raw_word.array)
similarity_score_melt = pd.melt(similarity_score_df)
similarity_score_melt.columns = ['RequestName', 'similarity']
similarity_score_melt = similarity_score_melt.drop('RequestName', 1)
similarity_score_melt.to_csv('similarity_score_melt.csv')
merged = pd.merge(results_df_melt, similarity_score_melt, left_index=True, right_index=True)
#results_df_melt.join(similarity_score_melt, on='RequestName')
#merged['RequestName'] = merged['RequestName'].apply(lambda x: str(x))
#merged.join(requests, on='RequestName')
merged.to_csv('merged.csv')
requests_merged = pd.merge(merged, requests, how="outer", on=["RequestName"])
final = pd.merge(requests_merged, wc_sanction, how="inner", on=["SanctionName"])
final.to_csv('final_result.csv')
final = final.drop_duplicates(subset=['requestID', 'UID'], keep="first")
final_60 = final.loc[final["similarity"] >= 0.60]
final_60 = final_60.drop('lastName', 1)
final_60 = final_60.drop('firstName', 1)
final_60 = final_60.drop('wholeName', 1)
final_60 = final_60.drop('LAST_NAME', 1)
final_60 = final_60.drop('FIRST_NAME', 1)
final_60 = final_60.drop('SanctionNamePinYin', 1)
final_60 = final_60.drop('RequestNamePinYin', 1)
final_60.to_csv('final_result_60.csv')

from string_grouper import match_strings
pinyin_matches = match_strings(master = wc_sanction['SanctionNamePinYin'] ,
							   duplicates = requests['RequestNamePinYin'] ,
							   master_id = wc_sanction['UID'],
							   duplicates_id = requests['requestID'],
							   ignore_index=True, min_similarity = 0.9)
pinyin_matches.to_csv('pinyin_matches.csv')
pinyin_matches.columns = ['SanctionName', 'UID', 'boost_similarity', 'requestID', 'RequestName']
final_60_py = final_60.append(pinyin_matches)
final_60_py = final_60_py.drop_duplicates(subset=['requestID', 'UID'], keep="first")
final_60_py.to_csv('final_60_py_clean.csv')