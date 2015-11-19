﻿#-------------------------------------------------------------------------------
# Name:        gensim_lda_japanese
# Purpose:
#
# Author:      kakeru_tamashiro
#
# Created:     16/11/2015
# Copyright:   (c) kakeru_tamashiro 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
from gensim import corpora, models, similarities
import MeCab

def extractiveKeyword(text):
    """textを形態素解析して、名詞のみのリストを返す"""
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text.encode('utf-8'))
    stoplist = set('こと する なる ある ます のみ これ それ あれ せる いう いる しれる 的 や'.split())
    keywords = []
    noun = "名詞"
    verb = "動詞"
    adjective = "形容詞"
    while node:
        feature = node.feature.split(",")
        if feature[0] == noun or feature[0] == verb or feature[0] == adjective:
            if feature[6] != "*":
                keywords.append(node.feature.split(",")[6])
            else:
                keywords.append(node.surface)
        node = node.next

    texts = [word for word in keywords if word not in stoplist]
    tokens_once = set(word for word in set(texts) if texts.count(word) == 1)
    texts = [word for word in texts if word not in tokens_once]
    return texts

def main():
    files_of_YahooNews = os.listdir('C:\Users\kakeru_tamashiro\UBIC\lda\YahooNews')
    group_of_keywords = []
    while files_of_YahooNews:
        name_of_YahooNews = files_of_YahooNews.pop()
        file_of_YahooNews = 'C:\Users\kakeru_tamashiro\UBIC\lda\YahooNews\\' + name_of_YahooNews
        f = open(file_of_YahooNews, "rb")
        texts = f.read()
        keywords = extractiveKeyword(texts.decode('utf-8', 'ignore'))
        group_of_keywords.append(keywords)

    f.close()
    name_of_YahooNews_test = './yahooIndustryNews11.txt'
    f = open(name_of_YahooNews_test, 'rb')
    test_text = f.read()
    f.close()
    test_keywords = []
    test_keywords.append(extractiveKeyword(test_text.decode('utf-8', 'ignore')))
    dictionary = corpora.Dictionary(group_of_keywords)
    dictionary_test = corpora.Dictionary(test_keywords)
    dictionary.save('./YahooNews.dict')
    dictionary_test.save('./YahooNews_test.dict')
    corpus = [dictionary.doc2bow(keywords) for keywords in group_of_keywords]
    test_corpus = [dictionary_test.doc2bow(test_keyword) for test_keyword in test_keywords]
    corpora.MmCorpus.serialize('./YahooNews.mm', corpus)
    corpora.MmCorpus.serialize('./YahooNews_test.mm', test_corpus)

    f = open('LDA_Data.txt', 'ab')
    lda = models.ldamodel.LdaModel(corpus=corpus, num_topics=1, id2word=dictionary)

    for topic in lda.show_topics(-1):
        topic_list = list(topic)
        topic_str = str(topic_list[0]) + "：" + topic_list[1].encode('utf-8', 'ignore') + "\r\n"
        f.write(topic_str)

    for topics_per_document in lda[test_corpus]:
        print(topics_per_document)
        for topic_doc in topics_per_document:
            topic_li = list(topic_doc)
            topics_per_document_li = str(topic_li[0]) + "：" + str(topic_li[1]) + "\r\n"
            f.write(topics_per_document_li)

    f.close()
if __name__ == '__main__':
    main()
