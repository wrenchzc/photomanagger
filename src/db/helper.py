from src.db.models import ImageMeta
from src.imageutils import ImageInfo

def exif_to_model(image_info):
    assert isinstance(image_info, ImageInfo)

    image_meta = ImageMeta()
    image_meta.filename = image_info.filename
    file_info = image_info.fileinfo

    image_meta.uuid = file_info.uuid
    image_meta.md5 = file_info.md5
    image_meta.file_createtime = file_info.create_time
    image_meta.file_size = file_info.size

    tags = image_info.tags


    image_meta.image_width = tags.get("EXIF ExifImageWidth", None)
    image_meta.image_height = tags.get("EXIF ExifImageLength", None)
    image_meta.image_datetime = tags.get("Image DateTime", None)
    image_meta.origin_datetime = tags.get("EXIF DateTimeOriginal", None)
    image_meta.digital_datetime = tags.get("EXIF DateTimeDigitized", None)
    image_meta.camera_brand = tags.get("Image Make", None)
    image_meta.camera_type = tags.get("Image Model", None)
    image_meta.focal_length = tags.get("EXIF FocalLength", None)
    image_meta.flash = tags.get("EXIF Flash", None)
    image_meta.fnumber = tags.get("EXIF FNumber", None)
    image_meta.aperture = tags.get("EXIF ApertureValue", None)
    image_meta.exposure_time = tags.get("EXIF ExposureTime", None)
    image_meta.exposure_bias = tags.get("EXIF ExposureBiasValue", None)
    image_meta.exposure_mode = tags.get("EXIF ExposureMode", None)
    image_meta.ISO_speed_rating = tags.get("EXIF ISOSpeedRatings", None)
    image_meta.white_balance = tags.get("EXIF WhiteBalance", None)

    return image_meta
