import http.server
import io
import cgi
import logging

from remote_cmder.core.enums import ResponseType

logger = logging.getLogger(__name__)


def create_cmder_http_request_handler(cmder):
    class CmderHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.cmder = cmder
            super().__init__(*args, **kwargs)

        def do_POST(self):
            ret, data, response_type = self.post_cmder()
            logger.info(f"{ret} {data} by {self.client_address}: {self.path}")
            with io.BytesIO() as f:
                http_status = 400
                if ret:
                    f.write(f"{data}\n".encode())
                    http_status = 200
                else:
                    f.write(f"Failed: {data}\n".encode())
                    http_status = 400
                length = f.tell()
                f.seek(0)

                if response_type == ResponseType.Plain:
                    self.send_response(http_status)
                    self.send_header("Content-type", "text/plain")
                    self.send_header("Content-Length", str(length))
                    self.end_headers()
                    self.copyfile(f, self.wfile)
                elif response_type == ResponseType.File:
                    self.send_response(http_status)
                    self.send_header("Content-type", "application/octet-stream")
                    self.send_header("Content-Length", str(length))
                    self.end_headers()
                    self.copyfile(f, self.wfile)
                else:
                    self.send_response(http_status)
                    self.send_header("Content-type", "text/plain")
                    self.send_header("Content-Length", str(length))
                    self.end_headers()
                    self.copyfile(f, self.wfile)

        def post_cmder(self):
            if not self.cmder:
                return (False, "Cmder doesn't created", ResponseType.Plain)

            cmd = self.path[1:]
            if not self.cmder.is_cmd_supported(cmd):
                return (False, "Cmd doesn't supported", ResponseType.Plain)

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
                    response_type = ResponseType.Plain
                    if isinstance(form["file"], list):
                        for record in form["file"]:
                            filename = record.filename
                            file_content = record.file.read()
                            msg += self.__cmd_response(cmd, filename, file_content)
                    else:
                        filename = form["file"].filename
                        file_content = form["file"].file.read()
                        msg += self.__cmd_response(cmd, filename, file_content)
                except IOError:
                    return (
                        False,
                        "Can't create file to write, do you have permission to write?",
                        ResponseType.Plain,
                    )
            return (True, msg, response_type)

        def __cmd_response(self, cmd, filename, file_content):
            msg = ""
            msg += f" {filename} ".center(40, "=") + "\n"
            cmder_response = self.cmder.execute(cmd, filename, file_content)
            if cmder_response.result:
                msg += cmder_response.data
            else:
                msg += "- cmder failed -"
            msg += "\n"
            return msg

    return CmderHTTPRequestHandler
