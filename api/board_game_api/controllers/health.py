from datetime import datetime
from flask import Blueprint, Response, current_app
from board_game_api import repos

MOD = Blueprint('health', __name__, url_prefix='')


@MOD.route('/health')
def health():
    # TODO: Figure out how to health check the database connection
    conn = current_app.arango_conn
    db = repos.get_database(conn, 'BoardGameDB')
    col = repos.get_collection(db, 'health')
    doc = repos.get_document_by_key(db, col, 'health-check')
    if doc:
        doc.delete()
    doc = {
        'ts': datetime.utcnow()
    }
    col.createDocument(doc)

    if '_key' in doc:
        return Response('OK', status=200)
    else:
        return Response('ERROR: 101', status=500)
