from sqlalchemy import Column, String, INTEGER, DATETIME, FLOAT, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ImageMeta(Base):
    __tablename__ = 'tbl_images'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    uuid = Column(String(32))
    filename = Column(String(256), unique=True)
    file_size = Column(INTEGER)
    md5 = Column(String(32), index=True)
    file_createtime = Column(DATETIME)
    image_width = Column(INTEGER)
    image_height = Column(INTEGER)
    origin_datetime = Column(DATETIME)
    digit_datetime = Column(DATETIME)
    camera_brand = Column(String(32))
    camera_type = Column(String(32))
    focal_length = Column(FLOAT)
    flash = Column(FLOAT)
    fnumber = Column(FLOAT)
    aperture = Column(FLOAT)
    exposure_time = Column(FLOAT)
    exposure_bias = Column(FLOAT)
    exposure_mode = Column(FLOAT)
    iso_speed_rating = Column(FLOAT)
    latitude = Column(String(32))
    longitude = Column(String(32))
    altitude = Column(String(32))
    country = Column(String(32))
    province = Column(String(32))
    city = Column(String(32))


class Tag(Base):
    __tablename__ = "tbl_tags"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    image_id = Column(INTEGER)
    tag = Column(String(32))
    value = Column(String(32))


class Option(Base):
    __tablename__ = "tbl_options"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(32), unique=True)
    value = Column(String(32))

class Person(Base):
    __tablename__ = "tbl_person"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(32), unique=True)
    sex = Column(String(8))
    img_list = Column(Text)
