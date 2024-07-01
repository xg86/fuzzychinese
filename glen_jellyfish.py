import jellyfish

levenshtein_distance = jellyfish.levenshtein_distance(u'ALBANIA - ALASP - Albanian State Police', u'Albanian')
print("levenshtein_distance", levenshtein_distance)

jaro_distance = jellyfish.jaro_distance(u'ALBANIA - ALASP - Albanian State Police', u'Albanian')
print("jaro_distance", jaro_distance)

damerau_levenshtein_distance = jellyfish.damerau_levenshtein_distance(u'ALBANIA - ALASP - Albanian State Police', u'Albanian')
print("damerau_levenshtein_distance", damerau_levenshtein_distance)

jaro_similarity = jellyfish.jaro_similarity(u'ALBANIA - ALASP - Albanian State Police', u'Albanian')
print("jaro_similarity", jaro_similarity)

jaro_winkler_similarity = jellyfish.jaro_winkler_similarity(u'ALBANIA - ALASP - Albanian State Police', u'Albanian')
print("jaro_winkler_similarity", jaro_winkler_similarity)

metaphone1 = jellyfish.metaphone(u'Wong')
print("metaphone1", metaphone1)
metaphone2 = jellyfish.metaphone(u'Huang')
print("metaphone2", metaphone2)
metaphone_jaro_w_S =  jellyfish.jaro_winkler_similarity(metaphone1,metaphone2);
print("metaphone_jaro_w_S", metaphone_jaro_w_S)

soundex1 = jellyfish.soundex(u'Kohl’s')
print("soundex1", soundex1)
soundex2 = jellyfish.soundex(u'Coles')
print("soundex2", soundex2)


nysiis1 = jellyfish.nysiis(u'Kohl’s')
print("nysiis1", nysiis1)
nysiis2 = jellyfish.nysiis(u'Coles')
print("nysiis2", nysiis2)

match1 = jellyfish.match_rating_codex(u'Kohl’s')
print("match1", match1)
match2 = jellyfish.match_rating_codex(u'Coles')
print("match2", match2)

import swalign
match = 2
mismatch = -1
scoring = swalign.NucleotideScoringMatrix(match, mismatch)

sw = swalign.LocalAlignment(scoring)  # you can also choose gap penalties, etc...
#datafile = "C://git//similarity-search-java//src//test//resources//world_check.csv"
datafile = "C://git//similarity-search-java//src//test//resources//company_name.csv"
#req = u'ALBAIA Albaian Polic'

req = u'JEFF   SIDNEY  TRUST FAMILY'
#alignment = sw.align(req, u'SIDNEY W SWARTZ 1982 FAMILY TRUST & JEFFREY B SWARTZ')
str = 'Dev Asia Bank (ABD)'
str_adb = 'ABD - Asian development Bank'
alignment = sw.align(str, str_adb)
jellyfish_jaro_w_s = jellyfish.jaro_winkler_similarity(req, u'SIDNEY W SWARTZ 1982 FAMILY TRUST & JEFFREY B SWARTZ')
alignment.dump()
#print("### jellyfish_jaro_w_S",jellyfish_jaro_w_s)


from pypinyin import pinyin, lazy_pinyin, Style
p = pinyin(u'中心')
print(p)
#p2 = [''.join(x) for x in p]

print(''.join(lazy_pinyin(u'中心')))
#print(''.join([''.join(x) for x in p]))
p2 = lazy_pinyin(u'中xin')
print('p2:', ''.join(p2))

import companynameparser

company_strs = [
    "武汉海明智业电子商务有限公司",
    "泉州益念食品有限公司",
    "常州途畅互联网科技有限公司合肥分公司",
    "昆明享亚教育信息咨询有限公司",
]
for name in company_strs:
    r = companynameparser.parse(name)
    print(r)

company_strs = [
    "武汉海明智业电子商务有限公司",
    "泉州益念食品有限公司",
    "常州途畅互联网科技有限公司合肥分公司",
    "昆明享亚教育信息咨询有限公司",
    "深圳光明区三晟股份有限公司",
    "东莞新乐天牙科器材有限公司",
]
for name in company_strs:
    r = companynameparser.parse(name)
    print(r)

print("*" * 42, ' enable word segment')
for name in company_strs:
    r = companynameparser.parse(name, pos_sensitive=False, enable_word_segment=True)
    print(r)

print("*" * 42, ' pos sensitive')
for name in company_strs:
    r = companynameparser.parse(name, pos_sensitive=True, enable_word_segment=False)
    print(r)

print("*" * 42, 'enable word segment and pos')
for name in company_strs:
    r = companynameparser.parse(name, pos_sensitive=True, enable_word_segment=True)
    print(r)

print("*" * 42, 'use custom name')
companynameparser.set_custom_split_file('./new_custom_name_split.csv')
for i in company_strs:
    r = companynameparser.parse(i)
    print(r)
'''
with open(datafile, encoding='utf8') as f:
    for line in f:
        #print(line.strip())
        alignment = sw.align(req,line)

        if alignment.score > 15:
            print("alignment.matches.identity", line, alignment.identity)
            alignment.dump()
            jellyfish_jaro_w_s = jellyfish.jaro_winkler_similarity(req, line);
            if jellyfish_jaro_w_s > 0.75:
                print("### jellyfish_jaro_w_S", line, jellyfish_jaro_w_s)
 
from LocalitySensitiveHashing import *
#datafile = "C://git//fuzzy-matcher//src//test//resources//test-data.csv"
datafile = "C://git//LocalitySensitiveHashing//Examples//data_for_lsh.csv"
lsh = LocalitySensitiveHashing(
                   datafile = datafile,
                   dim = 10,
                   r = 50,
                   b = 100,
                   expected_num_of_clusters = 10,
          )
lsh.get_data_from_csv()
lsh.initialize_hash_store()
lsh.hash_all_data()
similarity_groups = lsh.lsh_basic_for_neighborhood_clusters()
coalesced_similarity_groups = lsh.merge_similarity_groups_with_coalescence( similarity_groups )
merged_similarity_groups = lsh.merge_similarity_groups_with_l2norm_sample_based( coalesced_similarity_groups )
lsh.write_clusters_to_file( merged_similarity_groups, "clusters.txt" )
'''
import pandas as pd
a_dataframe = pd.DataFrame({"Letters": ["a", "b", "c"], "Numbers": [1, 4, 3]})
max_index = a_dataframe["Numbers"].idxmax()
max_row = a_dataframe.iloc[[max_index]]
print(max_row)












