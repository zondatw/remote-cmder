import argparse
import http.server
import socketserver
import io
import cgi
import logging
import hashlib

import settings

logger = logging.getLogger(__name__)


class Cmder:
    def __init__(self):
        self.__cmd_map = {
            "md5": self.md5,
        }

    def execute(self, cmd, filename, data, *args, **kwargs):
        return self.__cmd_map[cmd](filename, data, *args, **kwargs)

    def is_cmd_supported(self, cmd):
        return cmd in self.__cmd_map.keys()

    def md5(self, filename, data, *args, **kwargs):
        m = hashlib.md5()
        m.update(data)
        h = m.hexdigest()
        return (
            True,
            f"{filename}: {h}",
        )


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.cmder = Cmder()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        ret, info = self.post_cmder()
        logger.info(f"{ret} {info} by {self.client_address}: {self.path}")
        with io.BytesIO() as f:
            http_status = 400
            if ret:
                f.write(f"{info}\n".encode())
                http_status = 200
            else:
                f.write(f"Failed: {info}\n".encode())
                http_status = 400
            length = f.tell()
            f.seek(0)
            self.send_response(http_status)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-Length", str(length))
            self.end_headers()
            self.copyfile(f, self.wfile)

    def post_cmder(self):
        cmd = self.path[1:]
        if not self.cmder.is_cmd_supported(cmd):
            return (False, "Cmd doesn't supported")

        ctype, _ = cgi.parse_header(self.headers["Content-Type"])
        msg = ""
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
                        filename = record.name
                        file_content = record.file.read()
                        msg += self.__cmd_response(cmd, filename, file_content)
                else:
                    filename = form["file"].name
                    file_content = form["file"].file.read()
                    msg += self.__cmd_response(cmd, filename, file_content)
            except IOError:
                return (
                    False,
                    "Can't create file to write, do you have permission to write?",
                )
        return (True, msg)

    def __cmd_response(self, cmd, filename, file_content):
        msg = ""
        msg += f" {filename} ".center(40, "=") + "\n"
        ret, result = self.cmder.execute(cmd, filename, file_content)
        if ret:
            msg += result
        else:
            msg += "- cmder failed -"
        msg += "\n"
        return msg


parser = argparse.ArgumentParser()

parser.add_argument("--port", type=int, default=8888)

args = parser.parse_args()
port = args.port

if __name__ == "__main__":
    Handler = CustomHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        logger.info("serving at port: %s", port)
        httpd.serve_forever()
