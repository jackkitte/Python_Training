#-------------------------------------------------------------------------------
# Name:         join_document
# Purpose:
#
# Author:      kakeru_tamashiro
#
# Created:     12/11/2015
# Copyright:   (c) kakeru_tamashiro 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
import os
import codecs
import re

def main():
    files_of_comment = os.listdir('C:\Users\kakeru_tamashiro\Documents\GitHub\Python_Training\Lyric_comment\comments')
    files_of_lyric = os.listdir('C:\Users\kakeru_tamashiro\Documents\GitHub\Python_Training\Lyric_comment\songs')

    while files_of_comment or files_of_lyric:
        name_of_comment = files_of_comment.pop()
        folder_of_comment = os.listdir('C:\Users\kakeru_tamashiro\Documents\GitHub\Python_Training\Lyric_comment\comments\\' + name_of_comment)
        name_of_lyric = files_of_lyric.pop()
        folder_of_lyric = os.listdir('C:\Users\kakeru_tamashiro\Documents\GitHub\Python_Training\Lyric_comment\songs\\' + name_of_lyric)
        while folder_of_comment or folder_of_lyric:
            comment = folder_of_comment.pop()
            lyric = folder_of_lyric.pop()
            f_of_comment = open('C:\Users\kakeru_tamashiro\Documents\GitHub\Python_Training\Lyric_comment\comments\\' + name_of_comment + '\\' + comment, 'rb')
            f_of_lyric = open('C:\Users\kakeru_tamashiro\Documents\GitHub\Python_Training\Lyric_comment\songs\\' + name_of_lyric + '\\' + lyric, 'ab')
            data_of_comment = f_of_comment.read()
            f_of_lyric.write("\r\n")
            f_of_lyric.write(data_of_comment)
            f_of_lyric.close()
            f_of_comment.close()

if __name__ == '__main__':
    main()
