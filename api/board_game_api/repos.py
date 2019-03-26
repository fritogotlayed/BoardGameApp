from pyArango.connection import Connection
from pyArango.collection import Collection
from pyArango.database import Database
from pyArango.document import Document


def keyify_value(value):
    """

    :type value: str
    :return:
    """
    return value.lower().replace(' ', '-').replace("'", "-")


def scrub_db_specific_data(document):
    """

    :type document: dict
    :return:
    """
    document.pop('_id', None)
    document.pop('_rev', None)
    return document


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


def get_document_by_key(db, col, key, raw_results=False, scrub_results=False):
    """Gets a document by the given key from the collection

    :type db: Database
    :type col: Collection
    :type key: str
    :type raw_results: bool
    :type scrub_results: bool
    :rtype: Document
    """

    aql = 'FOR d in ' + col.name + ' FILTER d._key == @key RETURN d'
    params = {
        'key': key
    }

    result = db.AQLQuery(aql, bindVars=params, rawResults=raw_results)

    if len(result) > 0:
        if scrub_results:
            return scrub_db_specific_data(result[0])
        else:
            return result[0]
    return None


def search_documents(db, col, raw_result=False, scrub_result=False, **kwargs):
    """Gets a document by the given key from the collection

    :type db: Database
    :type col: Collection
    :type raw_result: bool
    :type scrub_result: bool
    :type kwargs: dict
    :rtype: Document
    """
    aql = 'FOR d in ' + col.name
    if kwargs:
        aql += ' FILTER '
        count = 0
        for key in kwargs:
            if count > 0:
                aql += ' AND '

            if isinstance(kwargs[key], str):
                aql += ('TRIM(UPPER(d.' + key +
                        ')) == TRIM(UPPER(@' + key + '))')
            else:
                aql += 'd.' + key + ' == @' + key

            count = count + 1

    aql += ' RETURN d'

    result = db.AQLQuery(aql, bindVars=kwargs, rawResults=raw_result)

    if scrub_result:
        new_result = []
        for r in result:
            new_result.append(scrub_db_specific_data(r))
        result = new_result

    return result
