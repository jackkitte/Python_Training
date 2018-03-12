# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request as req
import re
import pandas as pd
from pykakasi import kakasi
import matplotlib
import matplotlib.pyplot as plt

def scraping_with_regular_expression(url, css_selector, pattern):

    res = req.urlopen(url)
    soup = BeautifulSoup(res, "html.parser")
    li_list = soup.select(css_selector)
    repattern = re.compile(pattern)
    income_list = []
    todouhuken_list = []
    kakasi_ = kakasi()
    kakasi_.setMode("H", "a")
    kakasi_.setMode("K", "a")
    kakasi_.setMode("J", "a")
    conv = kakasi_.getConverter()
    
    for li in li_list:
        todouhuken = li("td")[1].get_text()
        income = li("td")[2].get_text()
        if None != repattern.search(income):
            income_string = repattern.search(income).group()
            income_string = income_string.replace(",", "")
            income_string = income_string.replace(".", "")
            income_int = int(income_string + "00")
            income_list.append(income_int)
            todouhuken_list.append(conv.do(todouhuken))

    return todouhuken_list, income_list

def list_to_dictionary(list1, list2):

    dic = {}

    for key, val in zip(list1, list2):
        dic[key] = val

    return dic

def dataframe_with_dic_to_dic(dataframe, dic):

    session_income = {}
    i = 0

    for value in dataframe["地域"]:
        value_lower = value.split()[0].lower()
        if "tokyo" == value_lower:
            value_lower = "toukyouto"
        elif "hokkaido" == value_lower:
            value_lower = "hokkaidou"
        elif "kyoto" == value_lower:
            value_lower = "kyoutofu"
        elif "osaka" == value_lower:
            value_lower = "oosakafu"
        elif "hyogo" == value_lower:
            value_lower = "hyougoken"
        elif "hiroshima" == value_lower:
            value_lower = "koushimaken"
        elif "kagoshima" == value_lower:
            value_lower = "shikajishimaken"
        elif "oita" == value_lower:
            value_lower = "ooitaken"
        elif "kochi" == value_lower:
            value_lower = "kouchiken"
        else:
            value_lower = value_lower + "ken"
        session_income[value_lower] = [dataframe.loc[[i]]["セッション"].values[0], dic[value_lower]]
        i += 1

    return session_income

def plot_scatter(dic):

    font = {"family": "TakaoGothic"}
    matplotlib.rc('font', **font)
    dic_pd = pd.DataFrame.from_dict(dic).T
    dic_pd.columns = ["セッション", "平均所得"]
    plt.rcParams["font.size"] = 18
    plt.figure(figsize=(15, 10))
    plt.scatter(dic_pd["セッション"], dic_pd["平均所得"])
    plt.xlabel("セッション数")
    plt.ylabel("サラリーマン平均年収")
    plt.savefig("セッション_平均年収の相関.png")
    #plt.show()
    dic_pd.corr()
    #nd = (dic_pd - dic_pd.min()) / (dic_pd.max() - dic_pd.min())
    #plt.scatter(nd["セッション"], nd["平均所得"])
    #nd.plot()
    #plt.show()

    return dic_pd.corr()
    
if __name__ == "__main__":

    url = "http://grading.jpn.org/kyalnensyu.html"
    css_selector = "body > div.body > div.content > div:nth-of-type(4) > table > tbody > tr"
    pattern = r"\d+,\d+\.\d"
    csv_path = "shouene_地域.csv"
    shouene = pd.read_csv(csv_path)
    shouene = shouene.drop([47, 48])

    todouhuken_list, income_list = scraping_with_regular_expression(url, css_selector, pattern)
    todouhuken_income_dic = list_to_dictionary(todouhuken_list, income_list)
    session_income = dataframe_with_dic_to_dic(shouene, todouhuken_income_dic)
    corr = plot_scatter(session_income)

    print(corr)
