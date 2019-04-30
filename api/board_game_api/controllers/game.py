from datetime import datetime
from flask import Blueprint, Response, current_app, request, jsonify
from board_game_api import repos
import json

MOD = Blueprint('game', __name__, url_prefix='/game')


@MOD.route('/add', methods=['POST'])
def add_game():
    try:
        conn = current_app.arango_conn
        db = repos.get_database(conn, 'BoardGameDB')
        col = repos.get_collection(db, 'games')

        data = request.get_json()
        issues = _validate_add_game(data)
        if issues:
            resp_obj = {"errors": issues}
            return Response(json.dumps(resp_obj),
                            mimetype='application/json',
                            status=400)
        else:
            doc = col.createDocument({
                '_key': repos.keyify_value(data['title']),
                'title': data['title'],
                'minPlayers': data['minPlayers'],
                'maxPlayers': data['maxPlayers'],
                'added': datetime.utcnow()
            })
            doc.save()
            return Response('OK', status=200)
    except Exception as ex:
        # TODO: internally log this
        print(str(ex))
        return Response('ERROR: 101', status=500)


@MOD.route('/<key>/delete', methods=['DELETE'])
def delete_game(key):
    try:
        conn = current_app.arango_conn
        db = repos.get_database(conn, 'BoardGameDB')
        col = repos.get_collection(db, 'games')

        data_key = repos.keyify_value(key)
        data_item = repos.get_document_by_key(db, col, data_key,
                                              raw_results=False,
                                              scrub_results=False)

        if data_item:
            data_item.delete()
            resp_obj = {"status": "deleted"}
            return Response(json.dumps(resp_obj),
                            mimetype='application/json',
                            status=200)
        else:
            resp_obj = {"errors": ["not found"]}
            return Response(json.dumps(resp_obj),
                            mimetype='application/json',
                            status=404)

    except Exception as ex:
        # TODO: internally log this
        print(str(ex))
        return Response('ERROR: 101', status=500)


@MOD.route('/<key>')
def get_game(key):
    try:
        conn = current_app.arango_conn
        db = repos.get_database(conn, 'BoardGameDB')
        col = repos.get_collection(db, 'games')

        data_key = repos.keyify_value(key)
        data_item = repos.get_document_by_key(db, col, data_key,
                                              raw_results=True,
                                              scrub_results=True)

        if data_item:
            return Response(json.dumps(data_item),
                            mimetype='application/json',
                            status=200)
        else:
            resp_obj = {"errors": ["not found"]}
            return Response(json.dumps(resp_obj),
                            mimetype='application/json',
                            status=404)
    except Exception as ex:
        # TODO: internally log this
        print(str(ex))
        return Response('ERROR: 101', status=500)


@MOD.route('')
def search_games():
    try:
        search_title = request.args.get('title')
        search_min_player = request.args.get('minPlayer')
        search_max_player = request.args.get('maxPlayer')

        conn = current_app.arango_conn
        db = repos.get_database(conn, 'BoardGameDB')
        col = repos.get_collection(db, 'games')

        results = repos.search_documents(db, col,
                                         raw_result=True,
                                         scrub_result=True,
                                         **request.args)

        if results:
            return Response(json.dumps({"data": results}),
                            mimetype='application/json',
                            status=200)
        else:
            resp_obj = {"data": []}
            return Response(json.dumps(resp_obj),
                            mimetype='application/json',
                            status=200)
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
        elif not data[key]:
            issues.append('Key "{0}" cannot have blank value'.format(key))

    if 'title' in data:
        data_key = repos.keyify_value(data['title'])
        data_item = repos.get_document_by_key(db, col, data_key)
        if data_item:
            issues.append('Cannot add game as it already exists.')

    return issues
