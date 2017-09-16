from src.imageutils import ImageInfo


def quote_str(s):
    return '"{s}"'.format(s=s)


class ImageDBHandler:
    def __init__(self, index_db):
        """
        :param index_db: instance of src.dbutils.Indexdb
        :param filenames: list of image filenames
        """
        self.index_db = index_db

    def do_index(self, filenames):
        [self.index_image(filename) for filename in filenames]

    def index_image(self, filename):
        image_info = ImageInfo(filename)
        file_info = image_info.fileinfo
        file_tags = image_info.tags

        if file_tags.has_exif:
            self._insert_with_exif(file_info, file_tags, filename)
        else:
            self._insert_without_exif(file_info, file_tags, filename)

    def _insert_with_exif(self, file_info, file_tags, filename):
        sql = "INSERT OR REPLACE INTO tbl_images" \
              "(uuid, filename, file_size, md5, file_createtime, " \
              "image_width, image_height, origin_datetime, digit_datetime, camera_brand, camera_type, focal_length, " \
              "flash, fnumber, aperture, exposure_time, exposure_bias, exposure_mode, iso_speed_rating)" \
              "values" \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values = (file_info.uuid, filename, file_info.size, file_info.md5, file_info.create_time,
                  file_tags.image_width, file_tags.image_height, file_tags.origin_datetime, file_tags.digital_datetime,
                  file_tags.camera_brand, file_tags.camera_type, file_tags.focal_length,
                  file_tags.flash, file_tags.fnumber, file_tags.aperture, file_tags.exposure_time,
                  file_tags.exposure_bias, file_tags.exposure_mode, file_tags.ISO_speed_rating)
        self.index_db.execute(sql, values)

    def _insert_without_exif(self, file_info, file_tags, filename):
        sql = "INSERT OR REPLACE INTO tbl_images" \
              "(uuid, filename, file_size, md5, file_createtime, " \
              "image_width, image_height)" \
              "values" \
              "(?, ?, ?, ?, ?, ?, ?)"
        values = (file_info.uuid, filename, file_info.size, file_info.md5, file_info.create_time,
                  file_tags.image_width, file_tags.image_height)
        self.index_db.execute(sql, values)
