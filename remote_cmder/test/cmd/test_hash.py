from remote_cmder.modules.cmd import hash


class TestCmdHash:
    def test_md5(self):
        result = hash.hash_md5("test", "123".encode())
        assert result == (
            True,
            "test: 202cb962ac59075b964b07152d234b70",
        )

    def test_sha1(self):
        result = hash.hash_sha1("test", "123".encode())
        assert result == (
            True,
            "test: 40bd001563085fc35165329ea1ff5c5ecbdbbeef",
        )
