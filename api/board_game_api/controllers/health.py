from datetime import datetime
from flask import Blueprint, Response, current_app
from board_game_api import repos

MOD = Blueprint('health', __name__, url_prefix='/health')


@MOD.route('')
def health():
    try:
        conn = current_app.arango_conn
        db = repos.get_database(conn, 'BoardGameDB')
        col = repos.get_collection(db, 'health')
        doc = repos.get_document_by_key(db, col, 'health-check')

        if doc:
            doc.delete()

        doc = col.createDocument({
            '_key': 'health-check',
            'ts': datetime.utcnow()
        })
        doc.save()

        return Response('OK', status=200)
    except Exception as ex:
        # TODO: internally log this
        print(str(ex))
        return Response('ERROR: 101', status=500)
