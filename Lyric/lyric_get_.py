#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kakeru_tamashiro
#
# Created:     22/10/2015
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

def main():
    favorite_song_file = "favorite_songs/yamaguchi_favorite_song.txt"
    f_favorite = open(favorite_song_file, "rb")
    favorite_lines = f_favorite.readlines()
    num = 0
    name_meta = "meta/yamaguchi_favorite_song_meta.csv"
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
        name_2 = "analysis_data/yamaguchi_favorite_song/music_content_%2d.txt" % num
        f = open(name_2, "wb")
        row = 0
        list_data_tag = []
        list_data = []
        for line in lines:
            if "<div id='lyricBlock'>" in line:
                name = lines[row+1].decode('utf_8')
                replace_name = re.sub(r'(<div class=\'caption\'>|<h2>|</h2>|</div>)', "", name)
                list_data_tag.append("[title]")
                list_data.append(replace_name.encode("shift_jis", 'ignore'))
            elif "<a href='/artist/" in line:
                singer = line.decode('utf_8')
                replace_singer = re.sub(r'(^<td.*/\'>|</a>|</td>)', "", singer)
                list_data_tag.append("[singer]")
                list_data.append(replace_singer.encode("shift_jis", 'ignore'))
            elif "align='center'>作詞：" in line:
                lyric_writer = line.decode('utf_8')
                replace_lyric_writer = re.sub(r'(<td width=\'.*\%\' align=\'center\'>|</td>)', "", lyric_writer)
                list_data_tag.append("[lyric_writer]")
                list_data.append(replace_lyric_writer.encode("shift_jis", 'ignore'))
            elif "align='center'>作曲：" in line:
                composer = line.decode('utf_8')
                replace_composer = re.sub(r'(<td width=\'.*\%\' align=\'center\'>|</td>)', "", composer)
                list_data_tag.append("[composer]")
                list_data.append(replace_composer.encode("shift_jis", 'ignore'))
            elif "<p id='lyricBody'>" in line:
                count = 0
                f.write("[content]\r\n")
                while True:
                    if "</div>" in lines[row+count]:
                        break
                    count += 1
                    cont = lines[row+count].decode('utf_8')
                    replace_cont = re.sub(r'(<br />|</p>)', "", cont)
                    if "</div>" in replace_cont:
                        pass
                    else:
                        f.write(replace_cont.encode('shift_jis', 'ignore'))

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
