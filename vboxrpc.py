#!/usr/bin/env python
import argparse
from flask import Flask
import logging

from lib.config import load_config, config
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
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.settings:
        load_config(args.settings)

    required = 'iso-dir', 'hdd-dir', 'vms-dir'
    for row in required:
        if not config(row):
            log.error('The %r value is missing in your configuration! '
                      'Please provide it and run VBoxRPC again.', row)
            exit(1)

    app = create_app(debug=args.debug)
    app.run(host=args.host, port=args.port)
