import json
import requests


def testInsertAvailability():
    requestJSON = { "username" : "somename",
                  "userid"   : 123,
                  "availability" : [ 1482065422000, 1482065429022, ]
                }
    responseJSON = requests.post(url = "http://127.0.0.1:6767/insertAvailability", json = requestJSON)
    print("responseJSON ", json.dumps(responseJSON.json()))

def testDisplayAvailability():
    requestJSON = {
        "queryTime" : 1482090557000
    }
    responseJSON = requests.post(url = "http://127.0.0.1:6767/displayAvailability", json = requestJSON)
    print("responseJSON ", json.dumps(responseJSON.json()))


#testInsertAvailability()
testDisplayAvailability()
