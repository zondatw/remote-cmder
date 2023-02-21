import argparse
import logging
import socketserver

from .settings import init_settings
from .modules.server import CmderHTTPRequestHandler

init_settings()
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Remote cmder\nexample:\n\tcurl -F 'file=@test.txt' -F 'file=@test.txt' http://127.0.0.1:8888/md5\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("--port", type=int, default=8888)

    args = parser.parse_args()
    port = args.port

    Handler = CmderHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        logger.info(f"serving at port: {port}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
