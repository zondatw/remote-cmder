import hashlib

from remote_cmder.modules.cmder import CmderResponse
from remote_cmder.core.enums import ResponseType


def hash_md5(filename, data, *args, **kwargs):
    m = hashlib.md5()
    m.update(data)
    h = m.hexdigest()
    return CmderResponse(
        result=True,
        data=f"{filename}: {h}",
        type=ResponseType.Plain,
    )


def hash_sha1(filename, data, *args, **kwargs):
    m = hashlib.sha1()
    m.update(data)
    h = m.hexdigest()
    return CmderResponse(
        result=True,
        data=f"{filename}: {h}",
        type=ResponseType.Plain,
    )


cmd_map = {
    "md5": hash_md5,
    "sha1": hash_sha1,
}
