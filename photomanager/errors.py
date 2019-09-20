class PhotoManagerError(Exception):
    pass


class MultiFileError(PhotoManagerError):
    error_message = "can not do action because of multi file shoted"
