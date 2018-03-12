# -*- coding: utf-8 -*-

import GoogleAnalyticsAPIv4
from elasticsearch import Elasticsearch

# Google Analytics API v4 へアクセスするためのパラメーター
view_id = "6540339"
dateRanges = [{"startDate": "2016-10-01", "endDate": "2017-09-30"}]
dimensions = [{"name": "ga:region"}, {"name": "ga:date"}]
dimensionFilterClauses = [{"operator": "AND",
                           "filters":[{"dimensionName": "ga:country",
                                       "not": "false",
                                       "operator": "REGEXP",
                                       "expressions": ["Japan"],
                                       "caseSensitive": "false",}],
                           }]
metrics = [{"expression": "ga:sessions", "formattingType": "INTEGER"}]
pageSize = 10000
body = {"reportRequests": []}
body["reportRequests"].append({"viewId": view_id,
                                "dateRanges": dateRanges,
                                "dimensions": dimensions,
                                "dimensionFilterClauses": dimensionFilterClauses,
                                "metrics": metrics,
                                "pageSize": pageSize,
                               })

# Elasticssearchのインデックスのマッピング
index = "googleanalytics"
mapping = {"mappings": {"都道府県別セッション": {"properties": {}}}}
ga_date = {"type": "date", "format": "yyyyMMdd"}
mapping["mappings"]["都道府県別セッション"]["properties"]["ga:date"] = ga_date

def elasticsearch_index_create(index, mapping):

    es = Elasticsearch()
    es.indices.delete(index=index)
    es.indices.create(index=index, body=mapping)

    return es

def elasticsearch_register(es, response_list):

    doc = {}
    id = 0
    for response in response_list:
        for report in response.get("reports", []):
            columnHeader = report.get("columnHeader", {})
            dimensionHeaders = columnHeader.get("dimensions", [])
            metricHeaders = columnHeader.get("metricHeader", {}).get("metricHeaderEntries", [])
            rows = report.get("data", {}).get("rows", [])
    
            for row in rows:
                dimensions = row.get("dimensions", [])
                metrics = row.get("metrics", [])
    
                for header, dimension in zip(dimensionHeaders, dimensions):
                    doc[header] = dimension
    
                for values in metrics:
                    for metricHeader, value in zip(metricHeaders, values.get("values")):
                        doc[metricHeader.get("name")] = int(value)
    
                es.index(index="googleanalytics", doc_type="都道府県別セッション", id=id+1, body=doc)
                id += 1

def main():

    analytics = GoogleAnalyticsAPIv4.initialize_analyticsreporting()
    response = GoogleAnalyticsAPIv4.get_report(analytics, body)
    response_list = []
    response_list.append(response)

    while response.get("reports", [])[0].get("nextPageToken"):
        body["reportRequests"][0]["pageToken"] = response.get("reports", [])[0].get("nextPageToken")
        response = GoogleAnalyticsAPIv4.get_report(analytics, body)
        response_list.append(response)

    es = elasticsearch_index_create(index, mapping)
    elasticsearch_register(es, response_list)

if __name__ == "__main__":
    main()
