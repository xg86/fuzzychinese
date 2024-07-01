import pandas as pd
import logging
import logging
import pandas as pd
import numpy as np
import datetime
from fuzzychinese import FuzzyChineseMatch

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)
logging.basicConfig(level=logging.DEBUG)

demo_file = 'C://git//fuzzychinese//corp.csv'
wc_sanction = pd.read_csv(demo_file, encoding='utf-8')
print("sanction with rows", len(wc_sanction))
wc_sanction['SanctionName'] = wc_sanction['enterprise_name']
import companynameparser
import re
companynameparser.set_custom_split_file('./new_custom_name_split.csv')
wc_sanction['SanctionPlace'] = wc_sanction['SanctionName'].apply(lambda x: companynameparser.parse(x).get('place'))
wc_sanction['SanctionBrand'] = wc_sanction['SanctionName'].apply(lambda x: companynameparser.parse(x).get('brand'))
wc_sanction['SanctionTrade'] = wc_sanction['SanctionName'].apply(lambda x: companynameparser.parse(x).get('trade'))
wc_sanction['SanctionPlace'] = wc_sanction['SanctionPlace'].apply(lambda x: re.sub('[,]', '', x))
wc_sanction['SanctionBrand'] = wc_sanction['SanctionBrand'].apply(lambda x: re.sub('[,]', '', x))
wc_sanction['SanctionTrade'] = wc_sanction['SanctionTrade'].apply(lambda x: re.sub('[,]', '', x))
wc_sanction.to_csv('wc_sanction_corp_parse.csv')

request_file= 'C://git//fuzzychinese//cn_request_corps.csv'
requests = pd.read_csv(request_file, encoding='utf-8')
print("request with rows", len(requests))

requests['RequestName'] = requests['RequestName'].apply(lambda x: re.sub('[!/&）（]', '', x))
requests['RequestPlace'] = requests['RequestName'].apply(lambda x: companynameparser.parse(x).get('place'))
requests['RequestBrand'] = requests['RequestName'].apply(lambda x: companynameparser.parse(x).get('brand'))
requests['RequestTrade'] = requests['RequestName'].apply(lambda x: companynameparser.parse(x).get('trade'))
requests['RequestPlace'] = requests['RequestPlace'].apply(lambda x: re.sub('[,]', '', x))
requests['RequestBrand'] = requests['RequestBrand'].apply(lambda x: re.sub('[,]', '', x))
requests['RequestTrade'] = requests['RequestTrade'].apply(lambda x: re.sub('[,]', '', x))
#raw_word = requests['RequestName']
fcm = FuzzyChineseMatch(ngram_range=(3, 3), analyzer='radical')
#requests.to_csv('C://git//ssc//requests-code.csv')

def fuzzy_match(fcm: FuzzyChineseMatch,
                sanction_items: pd.Series,
                request_items: pd.Series,
                top_n_matched: int,
                RequestColName: str,
                SanctionColName: str,
                similarityColName: str,
                watermark_similarity: float =0.25
                ):

    fcm.fit(sanction_items)
    results = fcm.transform(request_items, n=top_n_matched)

    results_df = pd.DataFrame(results.T, columns=request_items.array)
    results_df_melt = pd.melt(results_df)
    results_df_melt.columns = [RequestColName, SanctionColName]
    results_df_melt.to_csv('results_df_melt_corp.csv')
    similarity_score_df = pd.DataFrame(fcm.get_similarity_score().T, columns=request_items.array)
    similarity_score_melt = pd.melt(similarity_score_df)
    similarity_score_melt.columns = [RequestColName, similarityColName]
    similarity_score_melt = similarity_score_melt.drop(columns=RequestColName)
    similarity_score_melt.to_csv('similarity_score_melt_corp.csv')
    merged = pd.merge(results_df_melt, similarity_score_melt, left_index=True, right_index=True)
    merged.to_csv('merged_corp.csv')
    requests_merged = pd.merge(merged, requests, how="outer", on=[RequestColName])
    final = pd.merge(requests_merged, wc_sanction, how="inner", on=[SanctionColName])
    #final.to_csv('final_result_corp.csv')
    above_watermark = final.loc[final[similarityColName] >= watermark_similarity]
    return above_watermark


place_match = fuzzy_match(fcm = fcm,
            sanction_items = wc_sanction['SanctionPlace'],
            request_items = requests['RequestPlace'],
            top_n_matched = 10,
            RequestColName = 'RequestPlace',
            SanctionColName = 'SanctionPlace',
            similarityColName = 'similarityPlace',
            watermark_similarity = 0.6
)
place_match = place_match.drop(columns='RequestName')
place_match = place_match.drop(columns='RequestBrand')
place_match = place_match.drop(columns='RequestTrade')
place_match = place_match.drop(columns='enterprise_name')
place_match = place_match.drop(columns='SanctionName')
place_match = place_match.drop(columns='SanctionBrand')
place_match = place_match.drop(columns='SanctionTrade')
place_match = place_match.drop_duplicates(subset=['RequestId', 'enterprise_id'], keep="first")
place_match.to_csv('place_match.csv')

trade_match = fuzzy_match(fcm = fcm,
            sanction_items = wc_sanction['SanctionTrade'],
            request_items = requests['RequestTrade'],
            top_n_matched = 10,
            RequestColName = 'RequestTrade',
            SanctionColName = 'SanctionTrade',
            similarityColName = 'similarityTrade',
            watermark_similarity = 0.6
)
trade_match = trade_match.drop(columns='RequestName')
trade_match = trade_match.drop(columns='RequestPlace')
trade_match = trade_match.drop(columns='RequestBrand')
trade_match = trade_match.drop(columns='enterprise_name')
trade_match = trade_match.drop(columns='SanctionName')
trade_match = trade_match.drop(columns='SanctionBrand')
trade_match = trade_match.drop(columns='SanctionPlace')
trade_match = trade_match.drop_duplicates(subset=['RequestId', 'enterprise_id'], keep="first")
trade_match.to_csv('trade_match.csv')

brand_match = fuzzy_match(fcm = fcm,
            sanction_items = wc_sanction['SanctionBrand'],
            request_items = requests['RequestBrand'],
            top_n_matched = 10,
            RequestColName = 'RequestBrand',
            SanctionColName = 'SanctionBrand',
            similarityColName = 'similarityBrand'
)
#brand_match = brand_match.drop(columns='RequestName')
brand_match = brand_match.drop(columns='RequestPlace')
brand_match = brand_match.drop(columns='RequestTrade')
brand_match = brand_match.drop(columns='enterprise_name')
#brand_match = brand_match.drop(columns='SanctionName')
brand_match = brand_match.drop(columns='SanctionPlace')
brand_match = brand_match.drop(columns='SanctionTrade')
brand_match = brand_match.drop_duplicates(subset=['RequestId', 'enterprise_id'], keep="first")
brand_match.to_csv('brand_match.csv')

brand_trade = pd.merge(brand_match, trade_match, how="outer", on=["RequestId", "enterprise_id"])
brand_trade_place = pd.merge(brand_trade, place_match, how="outer", on=["RequestId", "enterprise_id"])
#brand_trade_place = brand_trade_place.drop_duplicates(subset=['RequestId', 'enterprise_id'], keep="first")
brand_trade_place = brand_trade_place[brand_trade_place['similarityBrand'].notna()]
brand_trade_place.similarityTrade = brand_trade_place.similarityTrade.fillna(0)
brand_trade_place.similarityPlace = brand_trade_place.similarityPlace.fillna(0)
def calculate(row):
    if row['similarityTrade'] > 0 and row['similarityPlace'] > 0:
        return row['similarityBrand']*0.8 + row['similarityTrade']*0.1 + row['similarityPlace']*0.1
    if row['similarityTrade'] > 0:
        return row['similarityBrand']*0.9 + row['similarityTrade']*0.1
    if row['similarityPlace'] > 0.0:
        return row['similarityBrand']*0.9 + row['similarityPlace']*0.1
    return row['similarityBrand']
brand_trade_place['boost_similarity'] = brand_trade_place.apply(lambda row: calculate(row), axis=1)
    #brand_trade_place['similarityBrand']*0.8 + brand_trade_place['similarityTrade']*0.1 + brand_trade_place['similarityPlace']*0.1
brand_trade_place.to_csv('brand_trade_place.csv')
final_result = brand_trade_place.loc[brand_trade_place['boost_similarity'] >= 0.6]
final_result.to_csv('brand_trade_place_final.csv')
final_result_RequestId = final_result.RequestId.unique()
not_found_ids = requests[~requests['RequestId'].isin(final_result_RequestId)]
print(not_found_ids)
not_found_RequestId = not_found_ids.RequestId.unique()
supplement = brand_trade_place[brand_trade_place['RequestId'].isin(not_found_RequestId)]
print(supplement)
supplement.reset_index(inplace=True)
max_index = supplement["boost_similarity"].idxmax()
max_row = supplement.iloc[[max_index]]
final_result_max = final_result.append(max_row)
final_result_max.to_csv('brand_trade_place_final_max.csv')