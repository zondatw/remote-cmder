from remote_cmder.modules.cmder import Cmder, CmderResponse
from remote_cmder.modules.cmd import default_cmd_map


def register_func(filename, data, *args, **kwargs):
    return (True, f"filename: {filename}, data: {data}")


def registers_func(test_cmd):
    def func(filename, data, *args, **kwargs):
        return (True, f"[{test_cmd}] filename: {filename}, data: {data}")

    return func


class TestCmderRegister:
    def setup_class(self):
        self.cmder = Cmder()

    def test_register(self):
        test_cmd = "test_cmd"
        test_func = register_func
        self.cmder.register(test_cmd, test_func)
        assert self.cmder.is_cmd_supported(test_cmd) is True

        test_filename = "test_filename"
        test_data = "test_data"
        assert self.cmder.execute(test_cmd, "test_filename", "test_data") == (
            True,
            f"filename: {test_filename}, data: {test_data}",
        )

    def test_registers(self):
        test_cmd_1 = "test_cmd_1"
        test_func_1 = registers_func(test_cmd_1)
        test_cmd_2 = "test_cmd_2"
        test_func_2 = registers_func(test_cmd_2)
        test_cmd_map = {
            test_cmd_1: test_func_1,
            test_cmd_2: test_func_2,
        }
        test_cmd_list = [test_cmd_1, test_cmd_2]

        self.cmder.registers(test_cmd_map)
        assert self.cmder.is_cmd_supported(test_cmd_1) is True
        assert self.cmder.is_cmd_supported(test_cmd_2) is True

        for test_cmd in test_cmd_list:
            test_filename = "test_filename"
            test_data = "test_data"
            assert self.cmder.execute(test_cmd, "test_filename", "test_data") == (
                True,
                f"[{test_cmd}] filename: {test_filename}, data: {test_data}",
            )


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
        assert exec_result == CmderResponse(
            result=True,
            msg="test: 202cb962ac59075b964b07152d234b70",
        )

    def test_cmd_sha1(self):
        exec_result = self.cmder.execute("sha1", "test", "123".encode())
        assert exec_result == CmderResponse(
            result=True,
            msg="test: 40bd001563085fc35165329ea1ff5c5ecbdbbeef",
        )
