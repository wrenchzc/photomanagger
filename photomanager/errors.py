class PhotoManagerError(Exception):
    error_code = 0
    

class MultiFileError(PhotoManagerError):
    error_code = 0
    message = "can not do action because of multi file shoted"


class RemoveImageError(PhotoManagerError):
    error_code = 40000


class RemoveImageIndexOutofRangeError(RemoveImageError):
    error_code = 40001
    message = "can not do action because of multi file shoted"
    
class RemoveImageCannotRemoveAllError(RemoveImageError):
    error_code = 40002
    message = "can not remove all duplicate files"

    

