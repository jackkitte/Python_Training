#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kakeru_tamashiro
#
# Created:     24/11/2015
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
    f_stop = open('stopwords.txt','rb')
    stopwords = f_stop.read()
    #stoplist = set('- / . の こと する なる ある ます のみ これ それ あれ せる いう いる しれる 的 や'.split())
    stoplist = set(stopwords.split())
    keywords = []
    noun = "名詞"
    verb = "動詞"
    adjective = "形容詞"
    while node:
        feature = node.feature.split(",")
        if feature[0] == noun or feature[0] == verb: #or feature[0] == adjective:
            if feature[6] != "*":
                keywords.append(node.feature.split(",")[6])
            else:
                keywords.append(node.surface)
        node = node.next

    texts = [word for word in keywords if word not in stoplist]
    tokens_once = set(word for word in set(texts) if texts.count(word) == 1)
    texts = [word.decode('utf-8','ignore') for word in texts if word not in tokens_once]
    return texts

def main():
    name_of_YahooNews_test = './YahooNews/yahooIndustryNews11.txt'
    #name_of_YahooNews_test = './test1.txt'
    f = open(name_of_YahooNews_test, 'rb')
    test_text = f.read()
    f.close()
    test_keywords = []
    test_keywords.append(extractiveKeyword(test_text.decode('utf-8', 'ignore')))
    dictionary_test = corpora.Dictionary(test_keywords)
    dictionary_test.save('./YahooNews_test.dict')
    test_corpus = [dictionary_test.doc2bow(test_keyword) for test_keyword in test_keywords]
    corpora.MmCorpus.serialize('./YahooNews_test.mm', test_corpus)

    f = open('./lda_result/sentence_/LDA_Data_Sentence_11.txt', 'ab')
    #lda = models.ldamodel.LdaModel(corpus=corpus, num_topics=7, id2word=dictionary, iterations=100, alpha='symmetric')
    lda = models.ldamodel.LdaModel.load('YahooNews_lda_topics15_.model')
    #lda.save('YahooNews_lda_topics7.model')

    for topic in lda.show_topics(-1):
        topic_list = list(topic)
        topic_str = str(topic_list[0]) + "：" + topic_list[1].encode('utf-8', 'ignore') + "\r\n"
        f.write(topic_str)

    for topics_per_document in lda[test_corpus]:
        sort_topic = sorted(topics_per_document, key=lambda x: x[1], reverse=True)
        for topic_doc in sort_topic:
            topic_li = list(topic_doc)
            topics_per_document_li = str(topic_li[0]) + "：" + str(topic_li[1]) + "\r\n"
            f.write(topics_per_document_li)
    f.close()

if __name__ == '__main__':
    main()
