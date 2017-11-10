# -*- coding: utf-8 -*-

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
import HelloAnalytics
from elasticsearch import Elasticsearch

view_id = "6540339"

def main():

    es = Elasticsearch()
    analytics = HelloAnalytics.initialize_analyticsreporting()
    response = HelloAnalytics.get_report(analytics, view_id)
#    mapping = {
#               "mappings": {
#               "todouhuken": {
#                                        "properties": {
#                                                       "todouhuken": {"type": "keyword","index": "not_analyzed"},
#                                                       "session": {"type": "integer"}
#                                                      }
#                                       }
#              }
#              }
    es.indices.delete(index="googleanalytics")
    es.indices.create(index="googleanalytics")#, body=mapping)
    #es.indices.put_mapping(index="googleanalytics", doc_type="todouhuken_session", body=mapping)

    for report in response.get("reports", []):
        rows = report.get("data", {}).get("rows", [])

        for id, row in enumerate(rows):
            dimensions = row.get("dimensions", [])
            metrics = row.get("metrics", [])

            for dimension in dimensions:
                print("地名 : {0}".format(dimension))
                todouhuken = dimension

            for values in metrics:
                print("セッション : {0}".format(values.get("values")))
                session = int(values.get("values")[0])

            doc = { "todouhuken" : todouhuken, "session" : session }
            es.index(index="googleanalytics", doc_type="todouhuken_session", id=id+1, body=doc)

if __name__ == "__main__":
    main()
