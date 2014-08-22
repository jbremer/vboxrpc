#!/usr/bin/env python
import argparse
from flask import Flask
import logging

from lib.config import load_config
from views.api import ApiView

log = logging.getLogger(__name__)


def create_app(debug=False):
    app = Flask('vboxrpc', static_folder='static',
                template_folder='templates')
    app.debug = debug

    ApiView.register(app)

    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debugging mode. Do *NOT* do this on production systems as it allows RCE.')
    parser.add_argument('--host', default='0.0.0.0', type=str, help='Host to listen on.')
    parser.add_argument('--port', default=9002, type=int, help='Port to listen on.')
    parser.add_argument('-s', '--settings', type=str, help='Settings file.')

    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    if args.settings:
        load_config(args.settings)

    app = create_app(debug=args.debug)
    app.run(host=args.host, port=args.port)
