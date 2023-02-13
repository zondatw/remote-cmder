import hashlib


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
