from remote_cmder.modules.cmder import Cmder


class TestCmder:
    def setup_class(self):
        self.cmder = Cmder()

    def test_cmder_supported(self):
        test_cases = [
            "md5",
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
        result = self.cmder._Cmder__cmd_md5("test", "123".encode())
        assert result == (
            True,
            "test: 202cb962ac59075b964b07152d234b70",
        )

        exec_result = self.cmder.execute("md5", "test", "123".encode())
        assert exec_result == (
            True,
            "test: 202cb962ac59075b964b07152d234b70",
        )
