import os.path

from remote_cmder import settings


def storage_upload(filename, data, *args, **kwargs):
    if not os.path.exists(settings.STORAGE_DIR_PATH):
        os.makedirs(settings.STORAGE_DIR_PATH, exist_ok=True)

    stored_path = os.path.join(f"{settings.STORAGE_DIR_PATH}/", filename)
    with open(stored_path, "wb") as f:
        f.write(data)

    return (
        True,
        f"{filename} is stored in {stored_path}",
    )


cmd_map = {
    "upload": storage_upload,
}
