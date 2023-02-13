import argparse
import logging
import socketserver

import settings
from remote_cmder.modules.server import CmderHTTPRequestHandler

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()

parser.add_argument("--port", type=int, default=8888)

args = parser.parse_args()
port = args.port

if __name__ == "__main__":
    Handler = CmderHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        logger.info("serving at port: %s", port)
        httpd.serve_forever()
