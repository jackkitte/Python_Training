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
    #url = "http://www.kasi-time.com/item-76807.html"
    #response = urllib2.urlopen(url)
    #html = response.read()
    name = "music_test.txt"
    #f = open(name, "wb")
    #f.write(html)
    #f.close()

    f = open(name, "rb")
    lines = f.readlines()
    f.close()
    name_2 = "music_phrase.txt"
    f = open(name_2, "wb")
    num = 0
    for line in lines:
        if "<h1>" in line:
            name = line.decode('utf_8')
            replace_name = re.sub(r'[\t</h1>]', "", name)
            f.write("[title]\r\n")
            f.write(replace_name.encode("shift_jis"))
            f.write("\r\n\r\n")
        elif "<th>歌手</th>" in line:
            singer = lines[num+3].decode('utf_8')
            replace_singer = re.sub(r'[\t</a>]', "", singer)
            f.write("[singer]\r\n")
            f.write(replace_singer.encode("shift_jis"))
            f.write("\r\n\r\n")
        elif "<th>作詞者</th>" in line:
            lyric_writer = lines[num+3].decode('utf_8')
            replace_lyric_writer = re.sub(r'[\t</a>]', "", lyric_writer)
            f.write("[lyric_writer]\r\n")
            f.write(replace_lyric_writer.encode("shift_jis"))
            f.write("\r\n\r\n")
        elif "<th>作曲者</th>" in line:
            composer = lines[num+3].decode('utf_8')
            replace_composer = re.sub(r'[\t</a>]', "", composer)
            f.write("[composer]\r\n")
            f.write(replace_composer.encode("shift_jis"))
            f.write("\r\n\r\n")
        elif "var lyrics " in line:
            phrase = htmlentity2unicode(line)
            phrase_uni = phrase.encode('shift_jis')
            replace_phrase = re.sub(r'<br>', "\r\n", phrase_uni)
            f.write(replace_phrase)
        num += 1

    f.close()


if __name__ == '__main__':
    main()
