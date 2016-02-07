import os
import sys
import logging
from flask import Flask, Blueprint, redirect

from orange.simpleapp.conf import config
from orange.simpleapp.common.helper import init_flask_logger, \
    jsonify_status_string


general = Blueprint('general', __name__)


@general.route('/test/', methods=['GET'])
def api_fortestonly():
    return jsonify_status_string(message="Success", status='success')


@general.route('/', methods=['GET'])
def index():
    return redirect('index.html')


LOG_FILE_PATH = config.getpath('app', 'LOG_FILE_PATH')
STATIC_PATH = config.getpath('app', 'STATIC_PATH')
API_URL_PREFIX = config.get('app', 'API_URL_PREFIX')

BLUEPRINTS = [
    (general, ''),
]


def register_blueprints(app, blueprints):
    for blueprint in blueprints:
        prefix = API_URL_PREFIX
        if isinstance(blueprint, tuple):
            blueprint, prefix = blueprint
        app.register_blueprint(blueprint, url_prefix=prefix)


def init_app_config(app, config):
    class CFG(object):
        pass

    cfg = CFG()
    for name in config.options('app'):
        setattr(cfg, name.upper(), config.get('app', name))

    cfg.PORT = config.getint('app', 'PORT')
    cfg.HOST = config.get('app', 'HOST')
    cfg.MAX_CONTENT_LENGTH = config.getint('app', 'MAX_CONTENT_LENGTH')
    cfg.DEBUG = config.getboolean('app', 'DEBUG')
    server_name = os.getenv('ORANGEAPP_SERVER_URL', '')
    if server_name:
        cfg.SERVER_NAME = server_name
        config.set('app', 'SERVER_NAME', server_name)

    app.config.from_object(cfg)


def init_logger(app):
    log_format = config.get('app', 'LOG_FORMAT')
    log_root_level = config.get('app', 'LOG_ROOT_LEVEL')
    log_file_path = config.get('app', 'LOG_FILE_PATH')
    log_file_log_level = config.get('app', 'LOG_FILE_LOG_LEVEL')
    init_flask_logger(app, log_format, log_root_level, log_file_path,
                      log_file_log_level)

    if config.getboolean('app', 'DEBUG'):
        app.logger.addHandler(logging.StreamHandler(sys.stderr))


def create_app(config):

    app = Flask(__name__, static_url_path='', static_folder=STATIC_PATH)
    init_app_config(app, config)
    init_logger(app)

    app.url_map.strict_slashes = False

    register_blueprints(app, BLUEPRINTS)

    return app
