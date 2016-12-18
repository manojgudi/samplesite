from sqlalchemy import Table, Column, Integer, String, MetaData, BigInteger, DECIMAL
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, ENUM, BIGINT, DATETIME, MEDIUMTEXT
from sqlalchemy.ext.automap import automap_base

from pytz import timezone
localTimezone = timezone("Asia/Kolkata")

metadata = MetaData()
user_availability = Table( "user_availability", metadata,
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column("username", String(64), nullable=False),
        Column("userid", Integer, primary_key = True, nullable=False),
        Column("available", DATETIME, nullable=False)
    )

def getMetaData():
    return metadata

def prepareBase(metadata):
    """
    Populates auto reflected instances from database
    :param metadata:
    :return: Instance of automap_base
    """
    base = automap_base(metadata=metadata)
    # calling prepare() just sets up mapped classes and relationships.
    base.prepare()
    return base

def serializeUserAvailability(row):
    """
    Serialize CRS Evaluation Row to a dictionary
    used by /udcmTracking API
    """
    userInfo = {}
    columnNames = [ x.name for x in row.__table__.columns ]
    for columnName in columnNames:
        userInfo[columnName] = getattr(row, columnName)

    # Send Epoch times in millis to avoid timezone pains
    userInfo["available"] = int(userInfo["available"].timestamp() * 1000)

    return userInfo
