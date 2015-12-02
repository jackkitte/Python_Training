#-------------------------------------------------------------------------------
# Name:        Retty_demo
# Purpose:
#
# Author:      kakeru_tamashiro
#
# Created:     17/11/2015
# Copyright:   (c) kakeru_tamashiro 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv

def main():
    name = 'tukishima_Hot_5.csv'
    f = open(name, 'rb')
    data_reader = csv.reader(f)
    list_1 = []
    list_2 = []

    for line in data_reader:
        line1 = line[0:2]
        line2 = line[2]
        list_1.append(line1)
        list_2.append(line2)

    f.close()
    num = 0
    cnt = 0
    f = open('./Hot5_1000_extractive_meta.csv', 'w')
    writer1 = csv.writer(f, lineterminator='\n')
    for content in list_2:
        name = './comments/Hot5_1000/extractive_comment%02d.txt' %(num)
        f_txt = open(name, 'ab')
        if cnt == 0:
            header = "[" + content + "]"
            header_utf8 = header.decode('utf-8','ignore')
            header_sjis = header_utf8.encode('shift-jis', 'ignore')
            f_txt.write(header_sjis)
            f_txt.write("\r\n")
            writer1.writerow(list_1[cnt])
            cnt += 1
            writer1.writerow(list_1[cnt])
            restaurant_id = list_1[cnt][1]
            f_txt.close()
        else:
            if list_1[cnt][1] == restaurant_id:
                content_utf8 = content.decode('utf-8','ignore')
                content_sjis = content_utf8.encode('utf-8','ignore')
                name_txt = './comments/Hot5_1000/extractive_comment%02d.txt' %(num)
                f_comment = open(name_txt, 'rb')
                data_comment = f_comment.read()
                f_comment.close()
                if len(data_comment.decode('utf-8','ignore')) < 1000:
                    name = './comments/Hot5_1000/extractive_comment%02d.txt' %(num)
                    f_txt = open(name, 'ab')
                    f_txt.write(content)
                    f_txt.write('\r\n')
                    f_txt.close()
                cnt += 1
            else:
                num += 1
                name = './comments/Hot5_1000/extractive_comment%02d.txt' %(num)
                writer1.writerow(list_1[cnt])
                f_txt = open(name, 'ab')
                f_txt.write(header_sjis)
                f_txt.write("\r\n")
                restaurant_id = list_1[cnt][1]
                f_txt.write(content)
                f_txt.close()
                cnt += 1

    f_txt.close()
    f.close()


if __name__ == '__main__':
    main()
