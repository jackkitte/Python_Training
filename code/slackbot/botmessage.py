# -*- coding: utf-8 -*-

import json

def botsend(message, text):

    if 'thread_st' in message.body:
        message.send(text, thread_ts=message.thread_ts)
    else:
        message.send(text, thread_ts=None)

def botreply(message, text):

    if 'thread_st' in message.body:
        message.reply(text, in_thread=True)
    else:
        message.reply(text)

def botwebapi(message, attachments):

    if not isinstance(attachments, str):
        attachments = json.dumps(attachments)

    if 'thread_ts' in message.body:
        message.send_webapi('', attachments, thread_ts=message.thread_ts)
    else:
        message.send_webapi('', attachments)
