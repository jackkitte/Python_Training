#!/usr/bin/env python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):

	def __init__(self):
		self.reset()
		# stripしたテキストを保存するバッファー
		self.fed = []

	def handle_data(self, d):
		# 任意のタグの中身のみを追加していく
		self.fed.append(d)

	def get_data(self):
		# バッファーを連結して返す
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()
