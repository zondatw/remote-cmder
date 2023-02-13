import hashlib


class Cmder:
    def __init__(self):
        self.__cmd_map = {
            "md5": self.__cmd_md5,
            "sha1": self.__cmd_sha1,
        }

    def execute(self, cmd, filename, data, *args, **kwargs):
        return self.__cmd_map[cmd](filename, data, *args, **kwargs)

    def is_cmd_supported(self, cmd):
        return cmd in self.__cmd_map

    def __cmd_md5(self, filename, data, *args, **kwargs):
        m = hashlib.md5()
        m.update(data)
        h = m.hexdigest()
        return (
            True,
            f"{filename}: {h}",
        )

    def __cmd_sha1(self, filename, data, *args, **kwargs):
        m = hashlib.sha1()
        m.update(data)
        h = m.hexdigest()
        return (
            True,
            f"{filename}: {h}",
        )
