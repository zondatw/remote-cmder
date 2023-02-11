import argparse
import http.server
import socketserver
import io
import cgi
import logging

import settings

logger = logging.getLogger(__name__)


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        ret, info = self.deal_post_data()
        logger.info(f"{ret} {info} by {self.client_address}")
        with io.BytesIO() as f:
            if ret:
                f.write(b"Success\n")
            else:
                f.write(b"Failed\n")
            length = f.tell()
            f.seek(0)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-Length", str(length))
            self.end_headers()
            self.copyfile(f, self.wfile)

    def deal_post_data(self):
        ctype, pdict = cgi.parse_header(self.headers["Content-Type"])
        pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
        pdict["CONTENT-LENGTH"] = int(self.headers["Content-Length"])
        if ctype == "multipart/form-data":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers["Content-Type"],
                },
            )
            try:
                if isinstance(form["file"], list):
                    for record in form["file"]:
                        with open(f"./{record.filename}", "wb") as f:
                            f.write(record.file.read())
                else:
                    with open(f"./{form['file'].filename}", "wb") as f:
                        f.write(form["file"].file.read())
            except IOError:
                return (
                    False,
                    "Can't create file to write, do you have permission to write?",
                )
        return (True, "Files uploaded")


parser = argparse.ArgumentParser()

parser.add_argument("--port", type=int, default=8888)

args = parser.parse_args()
port = args.port

if __name__ == "__main__":
    Handler = CustomHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        logger.info("serving at port: %s", port)
        httpd.serve_forever()
