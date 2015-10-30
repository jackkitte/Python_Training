#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kakeru_tamashiro
#
# Created:     13/10/2015
# Copyright:   (c) kakeru_tamashiro 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
import urllib2
import codecs
import htmlentitydefs
import re
import csv
import os
import time
import random

#sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
#sys.stdout = codecs.EncodedFile(sys.stdout, 'utf_8')
#sys.stdin = codecs.getreader('utf_8')(sys.stdin)
def htmlentity2unicode(text):
    reference_regex = re.compile(u'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
    num16_regex = re.compile(u'#x\d+', re.IGNORECASE)
    num10_regex = re.compile(u'#\d+', re.IGNORECASE)

    result = u''
    i = 0
    while True:
        match = reference_regex.search(text, i)
        if match is None:
            result += text[i:]
            break

        if i == 0:
            result += "[content]\r\n"
        else:
            result += text[i:match.start()]
        i = match.end()
        name = match.group(1)

        # 実体参照
        if name in htmlentitydefs.name2codepoint.keys():
            result += unichr(htmlentitydefs.name2codepoint[name])

        # 文字参照
        elif num16_regex.match(name):
            # 16進数
            result += unichr(int(u'0'+name[1:], 16))

        elif num10_regex.match(name):
            # 10進数
            result += unichr(int(name[1:]))

    return result

def main():
    favorite_song_file = "favorite_songs/mutou_favorite_song.txt"
    f_favorite = open(favorite_song_file, "rb")
    favorite_lines = f_favorite.readlines()
    num = 0
    name_meta = "meta/mutou_favorite_song_meta.csv"
    f_meta = open(name_meta, "wb")
    csv_writer = csv.writer(f_meta)
    for favorite_line in favorite_lines:
        rand_num = random.randint(1,10)
        print u"sleep time : %d" % rand_num
        time.sleep(rand_num)
        url = favorite_line
        response = urllib2.urlopen(url)
        html = response.read()
        name = "music_html.txt"
        f = open(name, "wb")
        f.write(html)
        f.close()

        f = open(name, "rb")
        lines = f.readlines()
        f.close()
        name_2 = "analysis_data/mutou_favorite_song/music_content_%2d.txt" % num
        f = open(name_2, "wb")
        row = 0
        list_data_tag = []
        list_data = []
        for line in lines:
            if "<h1>" in line:
                name = line.decode('utf_8')
                replace_name = re.sub(r'(\t|</h1>|<h1>)', "", name)
                list_data_tag.append("[title]")
                list_data.append(replace_name.encode("shift_jis", 'ignore'))
            elif "<th>歌手</th>" in line:
                singer = lines[row+3].decode('utf_8')
                replace_singer = re.sub(r'(\t|</a>|<a>)', "", singer)
                list_data_tag.append("[singer]")
                list_data.append(replace_singer.encode("shift_jis", 'ignore'))
            elif "<th>作詞者</th>" in line:
                lyric_writer = lines[row+3].decode('utf_8')
                replace_lyric_writer = re.sub(r'(\t|</a>|<a>)', "", lyric_writer)
                list_data_tag.append("[lyric_writer]")
                list_data.append(replace_lyric_writer.encode("shift_jis", 'ignore'))
            elif "<th>作曲者</th>" in line:
                composer = lines[row+3].decode('utf_8')
                replace_composer = re.sub(r'(\t|</a>|<a>)', "", composer)
                list_data_tag.append("[composer]")
                list_data.append(replace_composer.encode("shift_jis", 'ignore'))
            elif "var lyrics " in line:
                phrase = htmlentity2unicode(line)
                phrase_uni = phrase.encode('shift_jis', 'ignore')
                replace_phrase = re.sub(r'<br>', "\r\n", phrase_uni)
                f.write(replace_phrase)
            row += 1

        if num == 0:
            csv_writer.writerow(list_data_tag)
            csv_writer.writerow(list_data)
        else:
            csv_writer.writerow(list_data)
        num += 1
        f.close()

    f_meta.close()


if __name__ == '__main__':
    main()
