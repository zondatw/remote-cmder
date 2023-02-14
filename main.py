import argparse
import logging
import socketserver

from remote_cmder.settings import init_settings
from remote_cmder.modules.server import CmderHTTPRequestHandler

init_settings()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--port", type=int, default=8888)

    args = parser.parse_args()
    port = args.port

    Handler = CmderHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        logger.info(f"serving at port: {port}")
        httpd.serve_forever()
