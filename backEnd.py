#!/usr/bin/python3

import argparse
import bottle
import datetime
import logging    as LOG
import simplejson as json
import traceback
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


# TODO Remove this eventually
def enable_cors(fn):
    '''
    Used as decorator to add Cross Origin to headers
    '''
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        response.headers['Access-Control-Allow-Headers'] = 'Set-Cookie'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors


def getReqDict(requestJSON):
    """
    Validate request dict
    """
    try:
        print(requestJSON.body.read().decode("utf-8"))
        return json.loads(requestJSON.body.read().decode("utf-8"))
    except:
        print(requestJSON.body.read().decode("utf-8"))
        return False


@route('/insertAvailability', method=['POST'])
@enable_cors
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
    requestJSON      = getReqDict(request)
    if not requestJSON:
        return {"responseCode" : 1, "responseStatus" : "Unable to parse request" }

    mysqlSession = sessionGenerator()
    username     = requestJSON["username"]
    userid       = requestJSON["userid"]
    availability = requestJSON["availability"]

    # Commit to database
    try:
        for epochTimestamp in availability:
            mysqlSession.add( UserAvailability( username=username, userid=userid,
                                                inserted=datetime.datetime.fromtimestamp(int(epochTimestamp/1000))
                    ) )
        mysqlSession.commit()
        LOG.info("Commit successful for user:%s"%(username))
    except:
        LOG.error("Failed writing to database for: %s\n%s"%(username, traceback.format_exc()))
        mysqlSession.rollback()
        return {"responseCode": 2, "responseStatus" : "Error saving state to database, please resubmit"}

    return {"responseCode" : 0, "responseStatus":"All ok"}

def main():
    app = default_app()
    app.run(host = "0.0.0.0", port = 6767, quiet= False)

if __name__ == "__main__":
    main()
