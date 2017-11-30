# -*- coding: utf-8 -*-

import os
import os.path
import json
from collections import OrderedDict

from slackbot.bot import respond_to
import requests
from bs4 import BeautifulSoup

from botmessage import botsend, botwebapi

WEATHER_URL = 'http://weather.livedoor.com/forecast/webservice/json/v1?city={}'
CODE_URL = 'http://weather.livedoor.com/forecast/rss/primary_area.xml'

WEATHER_EMOJI = {
    '晴れ': ':sunny:',
    '晴のち曇': ':mostly_sunny:',
    '曇のち晴': ':mostly_sunny:',
    '曇時々晴': ':partly_sunny:',
    '晴時々曇': ':partly_sunny:',
    '雨時々曇': ':rain_cloud:',
    '雨のち曇': ':rain_cloud:',
    '曇のち雨': ':rain_cloud:',
    '曇り': ':cloud:',
    '曇時々雨': ':rain_cloud:',
    '雨': ':umbrella:',
    '雪': ':snowman:',
    '雪のち曇': ':snow_cloud:',
    '曇時々雪': ':snow_cloud:',
    }

CITY_CODE_FILE = 'city_code.json'

def get_city_code():

    city_dict = OrderedDict()
    city_code_file = os.path.join(os.path.dirname(__file__), CITY_CODE_FILE)

    if os.path.exists(city_code_file):
        with open(city_code_file) as f:
            city_dict = json.load(f, object_pairs_hook=OrderedDict)
    else:
        r = requests.get(CODE_URL)
        soup = BeautifulSoup(r.content, 'html.parser')

        for city in soup.findAll('city'):
            city_dict[city['title']] = city['id']

            with open(city_code_file, 'w') as f:
                json.dump(city_dict, f, indent=2, ensure_ascii=False)

    return city_dict

city_dict = get_city_code()

def _get_forecast_text(forecast):

    date = forecast['dateLabel']
    telop = forecast['telop']
    temp = forecast['temperature']

    text = '{} は {}{}'.format(date, WEATHER_EMOJI.get(telop,''), telop)
    if temp['min']:
        text += ' 最低気温{}℃ '.format(temp['min']['celsius'])
    if temp['max']:
        text += ' 最高気温{}℃ '.format(temp['max']['celsius'])

    return text

@respond_to('^(weather|天気)$')
@respond_to('^(weather|天気)\s+(.*)')
def weather(message, command, place='東京'):

    if place in ('help', 'list'):
        return

    code = city_dict.get(place)

    if code is None:
        botsend(message, '指定された地域は存在しません')
        return

    r = requests.get(WEATHER_URL.format(code))
    data = r.json()

    city = data['location']['city']
    link = data['link']
    text = _get_forecast_text(data['forecasts'][0]) + '\n'
    text += _get_forecast_text(data['forecasts'][1])


    attachments = [{
        'fallback': '{}の天気予報'.format(city), 
        'pretext': '<{}|{}の天気予報>'.format(link, city),
        'text': text,
        }]

    botwebapi(message, attachments)

@respond_to('^(weather|天気)\s+list')
def weather_lsit(message, command):

    reply = ' '.join(['`{}`'.format(x) for x in city_dict])
    botsend(message, '指定可能な地域: {}'.format(reply))

@respond_to('^(weather|天気)\s+help')
def weather_help(message, command):

    botsend(message, '''`$weather` `$天気`: 東京の天気予報を返す
    `$weather 釧路` `$天気 釧路`: 指定した地域の天気予報を返す
    `$weather list` `$天気 list`: 指定可能な地域の一覧を返す
    ''')
