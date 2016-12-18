#!/usr/bin/python3

import argparse
import bottle
import simplejson as json
import yaml

from bottle import run, post, request, response, route, default_app


def getReqDict(request):
    try:
    #print(request.body.read().decode("utf-8"))
        return json.loads(request.body.read().decode("utf-8"))
    except:
        #print(request.body.read().decode("utf-8"))
        return {"responseCode" : 1, "responseStatus" : "Unable to parse request" }



@route('/insertAvailability', method=['POST'])
def insertAvailability():
    """
    Request:
        {
            "username" : "somename"
            "userid"   : 123,
            "availability" : [ 1482065422000, 1482065429022, ]
        }

        {
            "responseCode" : 0,
            "responseStatus" : "All ok"
        }
    """
    request = getReqDict(request)
    return request

def main():
    app = default_app()
    app.run(host = "0.0.0.0", port = 6767, quiet= False)

if __name__ == "__main__":
    main()
