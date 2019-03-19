from datetime import datetime
from flask import Blueprint, Response, current_app, request
from board_game_api import repos

MOD = Blueprint('game', __name__, url_prefix='/game')


@MOD.route('/add', methods=['POST'])
def add_game():
    try:
        conn = current_app.arango_conn
        db = repos.get_database(conn, 'BoardGameDB')
        col = repos.get_collection(db, 'games')
        # doc = repos.get_document_by_key(db, col, 'health-check')
        #
        # if doc:
        #     doc.delete()
        #
        # doc = col.createDocument({
        #     '_key': 'health-check',
        #     'ts': datetime.utcnow()
        # })
        # doc.save()

        data = request.get_json()
        issues = _validate_add_game(data)
        if issues:
            return Response(issues, status=403)
        else:
            return Response('', status=200)
    except Exception as ex:
        # TODO: internally log this
        print(str(ex))
        return Response('ERROR: 101', status=500)


def _validate_add_game(data):
    """

    :type data: dict
    :rtype: list
    """
    issues = []
    conn = current_app.arango_conn
    db = repos.get_database(conn, 'BoardGameDB')
    col = repos.get_collection(db, 'games')

    required_keys = ['title', 'minPlayers', 'maxPlayers']

    # Validate minimum data for payload
    for key in required_keys:
        if key not in data:
            issues.append('Key "{0}" missing.'.format(key))

    if 'title' in data:
        data_key = data['title'].lower().replace(' ', '-')
        data_item = repos.get_document_by_key(db, col, data_key)
        if data_item:
            issues.append('Cannot add game as it already exists.')

    return issues
