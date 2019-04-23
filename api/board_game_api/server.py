import importlib
import glob
import os.path as path

import flask
import waitress
import yaml
import pyArango.connection

CURRENT_DIR = path.abspath(__file__).replace('.pyc', '.py').replace(
    'server.py', '')


def register_blueprints(app):
    modules = glob.glob(CURRENT_DIR + 'controllers/*.py')
    raw_mods = [path.basename(f)[:-3] for f in modules if path.isfile(f)]

    for mod in raw_mods:
        controller = importlib.import_module(
            'board_game_api.controllers.' + mod)
        if hasattr(controller, 'MOD'):
            app.register_blueprint(controller.MOD)


def build_app(override_config=None):
    """Builds the flask application

    :param override_config: Path to a configuration that overrides the defaults
    :type override_config: str

    :return: flask application
    :rtype: flask.Flask
    """
    app = flask.Flask('BoardGameApi')
    config = yaml.load(open(CURRENT_DIR + 'config.yaml'),
                       Loader=yaml.FullLoader)

    if override_config:
        # TODO: Verify this merges child items of dictionaries
        cfg = yaml.load(open(override_config))
        config.update(cfg)

    register_blueprints(app)

    app.app_config = config

    return app


def setup_arango_connection(app):
    config = app.app_config  # type: dict
    conn = pyArango.connection.Connection(
        arangoURL=config.get('arango', {}).get('url', 'http://127.0.0.1:8529'),
        username=config.get('arango', {}).get('user', 'root'),
        password=config.get('arango', {}).get('pass', '')
    )
    app.arango_conn = conn


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response


def start_server(override_config=None):
    app = build_app(override_config)
    setup_arango_connection(app)

    app.after_request(after_request)

    config = app.app_config  # type: dict

    host = config.get('flask', {}).get('host', '0.0.0.0')
    port = config.get('flask', {}).get('port', 5000)

    if config.get('flask', {}).get('debug', False):
        app.run(host=host,
                port=port,
                debug=True)
    else:
        waitress.serve(app,
                       host=host,
                       port=port)

