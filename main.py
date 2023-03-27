import argparse
import logging
import socketserver

from remote_cmder.settings import init_settings
from remote_cmder.modules.server import create_cmder_http_request_handler
from remote_cmder.modules.cmder import Cmder, CmderResponse
from remote_cmder.modules.cmd import default_cmd_map
from remote_cmder.core.enums import ResponseType

init_settings()
logger = logging.getLogger(__name__)


def cmd_demo_response_haha(filename, data, *args, **kwargs):
    response_data = "haha"
    return CmderResponse(
        result=True,
        data=f"Got {data} from {filename}, and get new word: {response_data}".encode(),
        type=ResponseType.Plain,
    )


def cmd_demo_file_response_haha(filename, data, *args, **kwargs):
    response_data = b""
    for i in range(256):
        response_data += i.to_bytes(1, "big")
    return CmderResponse(
        result=True,
        data=response_data,
        type=ResponseType.File,
    )


cmd_map = {
    "demo": cmd_demo_response_haha,
    "demo_file": cmd_demo_file_response_haha,
}


def main():
    """demo

    $ curl -F 'file=@test.txt' -F 'file=@test.txt' http://127.0.0.1:8888/demo
    =============== test.txt ===============
    Got b'123\n' from test.txt, and get new word: haha
    =============== test.txt ===============
    Got b'123\n' from test.txt, and get new word: haha
    $ curl -F 'file=@test.txt' http://127.0.0.1:8888/demo_file -o test.file
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100   846  100   512  100   334  89043  58086 --:--:-- --:--:-- --:--:--  165k
    $ xxd test.file
    00000000: 0001 0203 0405 0607 0809 0a0b 0c0d 0e0f  ................
    00000010: 1011 1213 1415 1617 1819 1a1b 1c1d 1e1f  ................
    00000020: 2021 2223 2425 2627 2829 2a2b 2c2d 2e2f   !"#$%&'()*+,-./
    00000030: 3031 3233 3435 3637 3839 3a3b 3c3d 3e3f  0123456789:;<=>?
    00000040: 4041 4243 4445 4647 4849 4a4b 4c4d 4e4f  @ABCDEFGHIJKLMNO
    00000050: 5051 5253 5455 5657 5859 5a5b 5c5d 5e5f  PQRSTUVWXYZ[\]^_
    00000060: 6061 6263 6465 6667 6869 6a6b 6c6d 6e6f  `abcdefghijklmno
    00000070: 7071 7273 7475 7677 7879 7a7b 7c7d 7e7f  pqrstuvwxyz{|}~.
    00000080: 8081 8283 8485 8687 8889 8a8b 8c8d 8e8f  ................
    00000090: 9091 9293 9495 9697 9899 9a9b 9c9d 9e9f  ................
    000000a0: a0a1 a2a3 a4a5 a6a7 a8a9 aaab acad aeaf  ................
    000000b0: b0b1 b2b3 b4b5 b6b7 b8b9 babb bcbd bebf  ................
    000000c0: c0c1 c2c3 c4c5 c6c7 c8c9 cacb cccd cecf  ................
    000000d0: d0d1 d2d3 d4d5 d6d7 d8d9 dadb dcdd dedf  ................
    000000e0: e0e1 e2e3 e4e5 e6e7 e8e9 eaeb eced eeef  ................
    000000f0: f0f1 f2f3 f4f5 f6f7 f8f9 fafb fcfd feff  ................
    00000100: 0001 0203 0405 0607 0809 0a0b 0c0d 0e0f  ................
    00000110: 1011 1213 1415 1617 1819 1a1b 1c1d 1e1f  ................
    00000120: 2021 2223 2425 2627 2829 2a2b 2c2d 2e2f   !"#$%&'()*+,-./
    00000130: 3031 3233 3435 3637 3839 3a3b 3c3d 3e3f  0123456789:;<=>?
    00000140: 4041 4243 4445 4647 4849 4a4b 4c4d 4e4f  @ABCDEFGHIJKLMNO
    00000150: 5051 5253 5455 5657 5859 5a5b 5c5d 5e5f  PQRSTUVWXYZ[\]^_
    00000160: 6061 6263 6465 6667 6869 6a6b 6c6d 6e6f  `abcdefghijklmno
    00000170: 7071 7273 7475 7677 7879 7a7b 7c7d 7e7f  pqrstuvwxyz{|}~.
    00000180: 8081 8283 8485 8687 8889 8a8b 8c8d 8e8f  ................
    00000190: 9091 9293 9495 9697 9899 9a9b 9c9d 9e9f  ................
    000001a0: a0a1 a2a3 a4a5 a6a7 a8a9 aaab acad aeaf  ................
    000001b0: b0b1 b2b3 b4b5 b6b7 b8b9 babb bcbd bebf  ................
    000001c0: c0c1 c2c3 c4c5 c6c7 c8c9 cacb cccd cecf  ................
    000001d0: d0d1 d2d3 d4d5 d6d7 d8d9 dadb dcdd dedf  ................
    000001e0: e0e1 e2e3 e4e5 e6e7 e8e9 eaeb eced eeef  ................
    000001f0: f0f1 f2f3 f4f5 f6f7 f8f9 fafb fcfd feff  ................
    """
    parser = argparse.ArgumentParser(
        description="Remote cmder\nexample:\n\tcurl -F 'file=@test.txt' -F 'file=@test.txt' http://127.0.0.1:8888/md5\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("--port", type=int, default=8888)

    args = parser.parse_args()
    port = args.port

    cmder = Cmder()
    cmder.registers(default_cmd_map)
    cmder.registers(cmd_map)
    cmder_http_request_handler = create_cmder_http_request_handler(cmder)
    with socketserver.TCPServer(("", port), cmder_http_request_handler) as httpd:
        logger.info(f"serving at port: {port}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
