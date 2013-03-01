# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sqlalchemy
from mozpool import config
import threading
import logging
import socket

# global for convenience
engine = None
logger = logging.getLogger('db.sql')

def _checkout_listener(dbapi_con, con_record, con_proxy):
    try:
        cursor = dbapi_con.cursor()
        cursor.execute("SELECT 1")
    except dbapi_con.OperationalError, ex:
        if ex.args[0] in (2006, 2013, 2014, 2045, 2055):
            raise sqlalchemy.exc.DisconnectionError()
        raise

# mysql connect listeners

def _pymysql_connect_listener(dbapi_con, connection_record):
    # apply SO_KEEPALIVE to the socket.
    # see https://github.com/petehunt/PyMySQL/issues/139
    # and https://bugzilla.mozilla.org/show_bug.cgi?id=817762
    sock = dbapi_con.socket
    logger.debug("setting SO_KEEPALIVE on MySQL socket %d" % sock.fileno())
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

def _mysqldb_connect_listener(dbapi_con, connection_record):
    logger.warning("Cannot set SO_KEEPALIVE on MySQL sockets with MySQLdb; expect hung DB connections")


_get_engine_lock = threading.Lock()
def get_engine():
    """
    Get a database engine object.
    """
    with _get_engine_lock:
        global engine
        if engine is None:
            engine_url = config.get('database', 'engine')

            # optimistically recycle connections after 10m
            engine = sqlalchemy.create_engine(engine_url, pool_recycle=600)
            # and pessimistically check connections before using them
            sqlalchemy.event.listen(engine.pool, 'checkout', _checkout_listener)

            # set sqlite to WAL mode to avoid weird concurrency issues
            if engine.dialect.name == 'sqlite':
                try:
                    engine.execute("pragma journal_mode = wal")
                except:
                    pass # oh well..

            if engine.dialect.name == 'mysql':
                driver = engine.driver
                listener = globals().get("_%s_connect_listener" % driver)
                if listener:
                    sqlalchemy.event.listen(engine.pool, 'connect', listener)

        return engine

def get_conn():
    """
    Get a database connection object.
    """
    return get_engine().connect()
