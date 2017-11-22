import exifread
import os
import uuid

from PIL import Image

from src.pmconst import SUPPORT_EXTS
from src.helper import get_file_md5


class ImageInfo:
    def __init__(self, filename):
        self.filename = filename
        self.tags = TagInfo(filename)
        self.fileinfo = FileInfo(filename)


class TagInfo:
    def _init_props_by_exif_tags(self):
        self.image_width = self._get_tag_item(self.tags.get("EXIF ExifImageWidth", None))
        self.image_height = self._get_tag_item(self.tags.get("EXIF ExifImageLength", None))
        self.image_datetime = self._get_tag_item(self.tags.get("Image DateTime", None))
        self.origin_datetime = self._get_tag_item(self.tags.get("EXIF DateTimeOriginal", None))
        self.digital_datetime = self._get_tag_item(self.tags.get("EXIF DateTimeDigitized", None))
        self.camera_brand = self._get_tag_item(self.tags.get("Image Make", None))
        self.camera_type = self._get_tag_item(self.tags.get("Image Model", None))
        self.focal_length = self._get_tag_item(self.tags.get("EXIF FocalLength", None))
        self.flash = self._get_tag_item(self.tags.get("EXIF Flash", None))
        self.fnumber = self._get_tag_item(self.tags.get("EXIF FNumber", None))
        self.aperture = self._get_tag_item(self.tags.get("EXIF ApertureValue", None))
        self.exposure_time = self._get_tag_item(self.tags.get("EXIF ExposureTime", None))
        self.exposure_bias = self._get_tag_item(self.tags.get("EXIF ExposureBiasValue", None))
        self.exposure_mode = self._get_tag_item(self.tags.get("EXIF ExposureMode", None))
        self.ISO_speed_rating = self._get_tag_item(self.tags.get("EXIF ISOSpeedRatings", None))
        self.white_balance = self._get_tag_item(self.tags.get("EXIF WhiteBalance", None))

    def _get_tag_item(self, tag):
        if tag:
            values = tag.values
            if isinstance(values, list):
                if isinstance(values[0], exifread.utils.Ratio):
                    return tag.printable
                else:
                    return values[0]
            elif isinstance(values, str):
                return values.strip()
            elif isinstance(values, bytes):
                return str(values).strip()
            else:
                return values

    def _init_props_by_pil(self, f):
        try:
            img = Image.open(f)
            self.image_width = img.width
            self.image_height = img.height
        except OSError as e:
            self.image_width = 0
            self.image_height = 0
            print("error when open image {filename} , message is {message}".format(filename=f.name, message=str(e)))

    def __init__(self, filename):
        self.tags = None
        self.has_exif = False

        with open(filename, "rb") as f:
            try:
                tags = exifread.process_file(f, details=True)
                self.has_exif = bool(tags)
                self.tags = tags
            except KeyError:
                print("can not read exif from {filename} ".format(filename=filename))
            except TypeError:
                print("can not read exif from {filename} ".format(filename=filename))
            except IndexError:
                print("can not read exif from {filename} ".format(filename=filename))

            if self.tags:
                self._init_props_by_exif_tags()
            else:
                self._init_props_by_pil(f)

    def info(self):
        return dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__'))


class FileInfo:
    def __init__(self, filename):
        self.size = os.path.getsize(filename)
        self.modify_time = os.path.getmtime(filename)
        self.create_time = os.path.getctime(filename)
        self.md5 = get_file_md5(filename)
        self.uuid = str(uuid.uuid1())


def get_folder_image_files(folder):
    files = []
    for fpath, dirs, fs in os.walk(folder):
        files = files + [
            "{path}{sep}{filename}".format(path=fpath, sep=os.sep, filename=f)[len(folder + os.sep):].replace(os.sep,
                                                                                                              "/") for f
            in fs if os.path.splitext(f)[1].lower().strip(".") in SUPPORT_EXTS]
    return files
