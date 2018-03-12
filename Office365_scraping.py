# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import request
from time import sleep
from numpy.random import *
from MyHtmlStripper import MyHtmlStripper

def web_scraping(url, headers, css_selector):
    req = request.Request(url = url, headers = headers)
    res = request.urlopen(req)
    soup = BeautifulSoup(res, "html.parser")

    return soup.select(css_selector)

if __name__ == "__main__":
    url = "https://products.office.com/ja-jp/business/microsoft-office-365-frequently-asked-questions"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}
    with open("Office365FAQ.txt", "a") as f:
        for i in range(1, 31):
            css_selector_title = "#question_title_{}".format(i)
            css_selector_text = "#question_title_{}-content > div:nth-of-type(1)".format(i)
            html_title = web_scraping(url, headers, css_selector_title)
            html_text = web_scraping(url, headers, css_selector_text)
            f.write(MyHtmlStripper(str(html_title[0])).value + "\n")
            f.write(MyHtmlStripper(str(html_text[0])).value + "\n")
            sleep(randint(5,11))

    with open("Office365FAQ.txt", "a") as f:
        css_selector_title31 = "#question_title_31-title-1"
        css_selector_text31 = "#question_title_31-content"
        css_selector_title32 = "#question_title_32-title"
        css_selector_text32 = "#accordion-id-here4 > div:nth-of-type(2) > div:nth-of-type(10)"
        css_selector_title33 = "#question_title_31-title-2"
        css_selector_text33 = "#question_title_32-content-01"
        css_selector_title34 = "#question_title_31-title"
        css_selector_text34 = "#accordion-id-here4 > div:nth-of-type(2) > div:nth-of-type(12)"
        css_selector_title35 = "#question_title_41-title"
        css_selector_text35 = "#question_title_41-content"
        css_selector_title36 = "#question_title_41-title-last"
        css_selector_text36 = "#question_title_41-content-01"
        html_title31 = web_scraping(url, headers, css_selector_title31)
        html_text31 = web_scraping(url, headers, css_selector_text31)
        sleep(randint(5,11))
        html_title32 = web_scraping(url, headers, css_selector_title32)
        html_text32 = web_scraping(url, headers, css_selector_text32)
        sleep(randint(5,11))
        html_title33 = web_scraping(url, headers, css_selector_title33)
        html_text33 = web_scraping(url, headers, css_selector_text33)
        sleep(randint(5,11))
        html_title34 = web_scraping(url, headers, css_selector_title34)
        html_text34 = web_scraping(url, headers, css_selector_text34)
        sleep(randint(5,11))
        html_title35 = web_scraping(url, headers, css_selector_title35)
        html_text35 = web_scraping(url, headers, css_selector_text35)
        sleep(randint(5,11))
        html_title36 = web_scraping(url, headers, css_selector_title36)
        html_text36 = web_scraping(url, headers, css_selector_text36)
        f.write(MyHtmlStripper(str(html_title31[0])).value + "\n")
        f.write(MyHtmlStripper(str(html_text31[0])).value + "\n")
        f.write(MyHtmlStripper(str(html_title32[0])).value + "\n")
        f.write(MyHtmlStripper(str(html_text32[0])).value + "\n")
        f.write(MyHtmlStripper(str(html_title33[0])).value + "\n")
        f.write(MyHtmlStripper(str(html_text33[0])).value + "\n")
        f.write(MyHtmlStripper(str(html_title34[0])).value + "\n")
        f.write(MyHtmlStripper(str(html_text34[0])).value + "\n")
        f.write(MyHtmlStripper(str(html_title35[0])).value + "\n")
        f.write(MyHtmlStripper(str(html_text35[0])).value + "\n")
        f.write(MyHtmlStripper(str(html_title36[0])).value + "\n")
        f.write(MyHtmlStripper(str(html_text36[0])).value + "\n")
