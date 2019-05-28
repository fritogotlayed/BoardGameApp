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
                'minPlayers': int(data['minPlayers']),
                'maxPlayers': int(data['maxPlayers']),
                'added': datetime.utcnow()
            })
            doc.save()
            return Response('OK', status=200)
    except Exception as ex:
        # TODO: internally log this
        print(str(ex))
        return Response('ERROR: 101', status=500)


@MOD.route('<key>/edit', methods=['POST'])
def edit_game(key):
    try:
        conn = current_app.arango_conn
        db = repos.get_database(conn, 'BoardGameDB')
        col = repos.get_collection(db, 'games')

        data = request.get_json()
        issues = _validate_edit_game(data)
        if issues:
            resp_obj = {"errors": issues}
            return Response(json.dumps(resp_obj),
                            mimetype='application/json',
                            status=400)
        else:
            data_key = repos.keyify_value(key)
            data_item = repos.get_document_by_key(db, col, data_key,
                                                  raw_results=False,
                                                  scrub_results=False)

            data_item['minPlayers'] = data['minPlayers']
            data_item['maxPlayers'] = data['maxPlayers']
            data_item['updated'] = datetime.utcnow()
            data_item.save()
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
        search_min_player = request.args.get('minPlayers')
        search_max_player = request.args.get('maxPlayers')

        conn = current_app.arango_conn
        db = repos.get_database(conn, 'BoardGameDB')
        col = repos.get_collection(db, 'games')

        args = {}
        if search_title:
            args['title'] = {
                'value': search_title,
                'op': 'like'
            }
        if search_min_player:
            args['minPlayers'] = {
                'value': int(search_min_player),
                'op': 'gt-eq'
            }
        if search_max_player:
            args['maxPlayers'] = {
                'value': int(search_max_player),
                'op': 'lt-eq'
            }

        results = repos.search_documents(db, col,
                                         raw_result=True,
                                         scrub_result=True,
                                         **args)

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
    required_keys = ['title', 'minPlayers', 'maxPlayers']
    issues = _validate_game_data(data, required_keys)
    _validate_game_players_values(data, issues)
    return issues


def _validate_edit_game(data):
    """

    :type data: dict
    :rtype: list
    """
    required_keys = ['minPlayers', 'maxPlayers']
    issues = _validate_game_data(data, required_keys)
    _validate_game_players_values(data, issues)
    return issues


def _validate_game_players_values(data, issues):
    min_players = -1
    max_players = -1
    try:
        min_players = int(data['minPlayers'])
    except ValueError:
        issues.append('Could not parse minPlayers')

    try:
        max_players = int(data['maxPlayers'])
    except ValueError:
        issues.append('Could not parse maxPlayers')

    if min_players != -1 and max_players != -1 and max_players < min_players:
        issues.append('minPlayers must equal to or less than max players')


def _validate_game_data(data, required_keys):
    """

    :type data: dict
    :rtype: list
    """
    issues = []
    conn = current_app.arango_conn
    db = repos.get_database(conn, 'BoardGameDB')
    col = repos.get_collection(db, 'games')

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
