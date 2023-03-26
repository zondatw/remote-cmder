from remote_cmder.modules.cmd import hash
from remote_cmder.modules.cmder import CmderResponse
from remote_cmder.core.enums import ResponseType


class TestCmdHash:
    def test_md5(self):
        result = hash.hash_md5("test", "123".encode())
        assert result == CmderResponse(
            result=True,
            data="test: 202cb962ac59075b964b07152d234b70",
            type=ResponseType.Plain,
        )

    def test_sha1(self):
        result = hash.hash_sha1("test", "123".encode())
        assert result == CmderResponse(
            result=True,
            data="test: 40bd001563085fc35165329ea1ff5c5ecbdbbeef",
            type=ResponseType.Plain,
        )
