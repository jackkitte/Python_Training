# -*- coding: utf-8 -*-

import argparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = '/home/tamashiro/AI/GoogleAnalytics/Analytics_API/Google-Analytics-python-3b34a4a4112c.p12'
SERVICE_ACCOUNT_EMAIL = 'shouene-com-analytics@tsuuken-ad-sys5.iam.gserviceaccount.com'
VIEW_ID = '6540339'

def initialize_analyticsreporting():

  credentials = ServiceAccountCredentials.from_p12_keyfile(
    SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

  return analytics

def get_report(analytics, body, view_id=VIEW_ID):

  return analytics.reports().batchGet(body=body).execute()

def main():

  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  print_response(response)

if __name__ == '__main__':
  main()
