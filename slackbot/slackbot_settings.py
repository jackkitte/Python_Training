# -*- coding: utf-8 -*-

import os

API_TOKEN = os.environ.get('SLACK_API_KEY', '') #"xoxb-274829026134-wCYnLBrvETGcHiTizMZIMLiv"

DEFAULT_REPLY = "コマンドは不明です。ヘルプを参照して下さい https://github.com/pyconjp/pyconjpbot#commands"

PLUGINS = ["plugins"]

ALIASES = '$'
