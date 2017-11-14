import datetime
import time
from src.db.models import ImageMeta
from src.imageutils import ImageInfo

def fraction_to_float(fraction):
    if fraction is None:
        return float(0)

    if "/" in fraction:
        numerator, denominator = fraction.split("/")
    else:
        numerator, denominator = float(fraction), 1

    return float(numerator) / float(denominator)

def exif_to_model(image_info):
    assert isinstance(image_info, ImageInfo)

    image_meta = ImageMeta()
    image_meta.filename = image_info.filename
    file_info = image_info.fileinfo

    image_meta.uuid = file_info.uuid
    image_meta.md5 = file_info.md5
    str_create_time = time.strftime('%Y:%m:%d %H:%M:%S',time.localtime(file_info.create_time))
    image_meta.file_createtime = datetime.datetime.strptime(str_create_time, '%Y:%m:%d %H:%M:%S')

    image_meta.file_size = file_info.size

    tags = image_info.tags

    from src.imageutils import TagInfo
    assert isinstance(tags, TagInfo)
    image_meta.image_width = tags.image_width
    image_meta.image_height = tags.image_height
    if tags.has_exif:
        image_meta.origin_datetime = datetime.datetime.strptime(tags.origin_datetime, '%Y:%m:%d %H:%M:%S')
        image_meta.digital_datetime = datetime.datetime.strptime(tags.digital_datetime, '%Y:%m:%d %H:%M:%S')
        image_meta.camera_brand = tags.camera_brand
        image_meta.camera_type = tags.camera_type
        image_meta.focal_length = fraction_to_float(tags.focal_length)
        image_meta.flash = tags.flash
        image_meta.fnumber = fraction_to_float(tags.fnumber)
        image_meta.aperture = fraction_to_float(tags.aperture)
        image_meta.exposure_time = fraction_to_float(tags.exposure_time)
        image_meta.exposure_bias = tags.exposure_bias
        image_meta.exposure_mode = tags.exposure_mode
        image_meta.ISO_speed_rating = tags.ISO_speed_rating
        image_meta.white_balance = tags.white_balance

    return image_meta
