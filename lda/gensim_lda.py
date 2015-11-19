#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kakeru_tamashiro
#
# Created:     16/11/2015
# Copyright:   (c) kakeru_tamashiro 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from gensim import corpora, models, similarities

def main():
    documents = ["Human machine interface for lab abc computer applications",
                 "A survey of user opinion of computer system response time",
                 "The EPS user interface management system",
                 "System and human system engineering testing of EPS",
                 "Relation of user perceived response time to error measurement",
                 "The generation of random binary unordered trees",
                 "The intersection graph of paths in trees",
                 "Graph minors IV Widths of trees and well quasi ordering",
                 "Graph minors A survey"]

    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
    # remove words that appear only once
    all_tokens = sum(texts, [])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once] for text in texts]

    dictionary = corpora.Dictionary(texts)
    dictionary.save('./deerwester.dict')
    # store the dictionary, for future reference
    # バイナリではなくテキストとして保存する場合
    dictionary.save_as_text('./deerwester_text.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]
    # store to disk, for later use
    corpora.MmCorpus.serialize('./deerwester.mm', corpus)
    index = similarities.docsim.SparseMatrixSimilarity(corpus, num_features=len(dictionary))
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=3)
    corpus_lsi = lsi[corpus_tfidf]
    print(lsi.print_topics(3))
    for doc in corpus_lsi:
        print(doc)

if __name__ == '__main__':
    main()
