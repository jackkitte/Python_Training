#-------------------------------------------------------------------------------
# Name:        python_wakati
# Purpose:
#
# Author:      kakeru_tamashiro
#
# Created:     16/11/2015
# Copyright:   (c) kakeru_tamashiro 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import MeCab

def extractiveKeyword(text):
    """textを形態素解析して、名詞のみのリストを返す"""
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text.encode('utf-8'))
    keywords = []
    noun = "名詞"
    while node:
        if node.feature.split(",")[0] == noun:
            if node.feature.split(",")[6] != "*":
                keywords.append(node.feature.split(",")[6])
            else:
                keywords.append(node.surface)
        node = node.next

    return keywords

def main():
    text = 'PythonからMeCabの形態素解析機能を使ってみました。'
    text_utf8 = text.decode('utf-8', 'ignore')
    keywords = extractiveKeyword(text_utf8)
    for w in keywords:
        print(w.decode('utf-8'))

if __name__ == '__main__':
    main()
