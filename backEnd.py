#!/usr/bin/python3

import argparse
import bottle
import datetime
import logging    as LOG
import simplejson as json
import yaml

from bottle import run, post, request, response, route, default_app
from schemaCustom   import prepareBase, getMetaData, serializeUserAvailability

from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker, mapper, scoped_session

# ARGPARSE code
parser = argparse.ArgumentParser(description = "A small server serving kickfooter front end")
parser.add_argument('file', help="Takes a valid configuration json file to db variables")
args   = parser.parse_args()

LOG.basicConfig(format='%(asctime)s  %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='server.log', filemode='a', level=LOG.DEBUG)

config_file = open(args.file)
getconfig   = yaml.load(config_file)

userdbIP       = getconfig["userdbIP"]
userdbPort     = getconfig["userdbPort"]
userdbUname    = getconfig["userdbUname"]
userdbPassword = getconfig["userdbPassword"]

userdbConnectionString = "mysql+pymysql://{}:{}@{}:{}".format(userdbUname, userdbPassword, userdbIP, userdbPort)
userdbEngine           = create_engine("{}/{}".format(userdbConnectionString, "userdb"))

SessionClass     = sessionmaker(bind = userdbEngine)
sessionGenerator = scoped_session(SessionClass)

# Get ORM Mapped base instance
metadata         = getMetaData()
UserAvailability = prepareBase(metadata).classes.user_availability

def getReqDict(request):
    """
    Validate request dict
    """
    try:
        print(request.body.read().decode("utf-8"))
        return json.loads(request.body.read().decode("utf-8"))
    except:
        print(request.body.read().decode("utf-8"))
        return False


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
    request      = getReqDict(request)
    if not request:
        return {"responseCode" : 1, "responseStatus" : "Unable to parse request" }

    mysqlSession = sessionGenerator()
    username     = request["username"]
    userid       = request["userid"]
    availability = request["availability"]

    # Commit to database
    try:
        for epochTimestamp in availability:
            mysqlSession.add( UserAvailability( username=username, userid=userid,
                                                inserted=datetime.datetime.fromtimestamp(int(epochTimestamp/1000))
                    ) )
        mysqlSession.commit()
        LOG.info("Commit successful for user:%s"%(username))
    except:
        LOG.error("Failed writing to database for: %s"%(username))
        mysqlSession.rollback()
        return {"responseCode": 2, "responseStatus" : "Error saving state to database, please resubmit"}

    return {"responseCode" : 0, "responseStatus":"All ok"}

def main():
    app = default_app()
    app.run(host = "0.0.0.0", port = 6767, quiet= False)

if __name__ == "__main__":
    main()
