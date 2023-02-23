from remote_cmder.modules.cmder import Cmder
from remote_cmder.modules.cmd import default_cmd_map


class TestCmder:
    def setup_class(self):
        self.cmder = Cmder()
        self.cmder.registers(default_cmd_map)

    def test_cmder_supported(self):
        test_cases = [
            "md5",
            "sha1",
        ]
        for test_case in test_cases:
            assert self.cmder.is_cmd_supported(test_case) is True

    def test_cmder_nonsupported(self):
        test_cases = [
            "lala",
        ]
        for test_case in test_cases:
            assert self.cmder.is_cmd_supported(test_case) is False

    def test_cmd_md5(self):
        exec_result = self.cmder.execute("md5", "test", "123".encode())
        assert exec_result == (
            True,
            "test: 202cb962ac59075b964b07152d234b70",
        )

    def test_cmd_sha1(self):
        exec_result = self.cmder.execute("sha1", "test", "123".encode())
        assert exec_result == (
            True,
            "test: 40bd001563085fc35165329ea1ff5c5ecbdbbeef",
        )
