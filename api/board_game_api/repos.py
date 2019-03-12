from pyArango.connection import Connection
from pyArango.collection import Collection
from pyArango.database import Database
from pyArango.document import Document


def get_database(conn, name):
    """Gets an arangodb database safely

    Returns an instance of an Arango database. If the database does not exist
    a new one will be created.

    :type conn: Connection
    :type name: str
    :rtype: Database
    """

    if conn.hasDatabase(name) is False:
        return conn.createDatabase(name)

    return conn[name]


def get_collection(db, name):
    """Gets an arangodb collection safely

    Returns an instance of an arango collection. If the collection does not
    exist a new one will be created.

    :type db: Database
    :type name: str
    :rtype: Collection
    """

    if db.hasCollection(name) is False:
        return db.createCollection(name=name)

    return db[name]


def get_document_by_key(db, col, key):
    """Gets a document by the given key from the collection

    :type db: Database
    :type col: Collection
    :type key: str
    :rtype: Document
    """

    aql = 'FOR d in ' + col.name + ' FILTER d._key == @key RETURN d'
    params = {
        'key': key
    }

    result = db.AQLQuery(aql, bindVars=params)

    # if len(result) > 0:
    #     return result[0]
    # return None

    return None if len(result) <= 0 else result[0]
