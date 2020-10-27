import exifread
import os
import uuid

from PIL import Image

from photomanager.lib.pmconst import SUPPORT_EXTS, SKIP_LIST, PATH_SEP
from photomanager.lib.helper import get_file_md5, get_timestamp_from_str


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


def get_folder_image_files(folder: str, last_index_time_str: str = None) -> list:
    files = []
    for fpath, dirs, fs in os.walk(folder):
        files = files + [
            "{path}{sep}{filename}".format(path=fpath, sep=PATH_SEP, filename=f)[len(folder + PATH_SEP):] for f
            in fs if _ext_is_supported(f) and not _filename_is_blocked(f)]

    last_time_stamp = get_timestamp_from_str(last_index_time_str)
    if last_time_stamp > 0:
        return _filter_file_by_mtime(folder, files, last_time_stamp)
    else:
        return files


def _ext_is_supported(filename: str) -> bool:
    return os.path.splitext(filename)[1].lower().strip(".") in SUPPORT_EXTS


def _filename_is_blocked(filename: str) -> bool:
    for skip in SKIP_LIST:
        if skip in filename:
            return True

    return False


def _filter_file_by_mtime(folder: str, files: list, last_time_stamp: float) -> list:
    filter_files = []
    for file_name in files:
        try:
            file_mtime = os.path.getmtime(folder + PATH_SEP + file_name)
        except OSError:
            file_mtime = 0

        if file_mtime > last_time_stamp:
            filter_files.append(file_name)
    return filter_files
