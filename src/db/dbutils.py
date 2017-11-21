import sqlite3
import os
from src.pmconst import PMDBNAME
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.db.models import Base

class IndexDBRaw:
    @staticmethod
    def __ensure_slahs(dir):
        if dir[-1] != os.path.sep:
            dir = dir + os.path.sep
        return dir

    def __init__(self, rootdir):
        self._dbname = self.__ensure_slahs(rootdir) + PMDBNAME
        self.connection = sqlite3.connect(self._dbname)
        self.init()

    def close(self):
        self.connection.close()

    def execute_multi(self, sqls):
        [self.execute(sql, do_commit=False) for sql in sqls]
        self.connection.commit()

    def execute(self, sql, params=(), do_commit=True):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            if do_commit:
                self.connection.commit()
        finally:
            cursor.close()

    def query(self, sql):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql)
            values = cursor.fetchall()
        finally:
            cursor.close()
        return values

    def init(self):
        sql_init_tables = "CREATE TABLE IF NOT EXISTS tbl_images " \
                          "(" \
                          "id integer PRIMARY KEY AUTOINCREMENT, " \
                          "uuid varchar(32)," \
                          "filename varchar(128), " \
                          "file_size int," \
                          "md5 varchar(32)," \
                          "file_createtime datetime," \
                          "image_width int," \
                          "image_height int," \
                          "origin_datetime datetime," \
                          "digit_datetime datetime," \
                          "camera_brand varchar(32), " \
                          "camera_type varchar(32), " \
                          "focal_length float, " \
                          "flash float, " \
                          "fnumber float, " \
                          "aperture float, " \
                          "exposure_time float, " \
                          "exposure_bias float, " \
                          "exposure_mode float, " \
                          "iso_speed_rating float," \
                          "latitude varchar(32)," \
                          "longitude varchar(32), " \
                          "altitude varchar(32), " \
                          "country varchar(32), " \
                          "province varchar(32), " \
                          "city varchar(32) " \
                          ");" \
                          "CREATE TABLE IF NOT EXISTS tbl_tags" \
                          "(" \
                          "id integer primary key AUTOINCREMENT," \
                          "image_id integer, " \
                          "tag varchar(32)" \
                          ");" \
                          "CREATE TABLE IF NOT EXISTS tbl_options" \
                          "(" \
                          "id integer primary key AUTOINCREMENT," \
                          "name varchar(32)," \
                          "value varchar(128)" \
                          ");"

        sql_init_index = "CREATE INDEX IF NOT EXISTS inx_images_md5 on tbl_images(md5); " \
                         "CREATE UNIQUE INDEX IF NOT EXISTS inx_images_uuid on tbl_images(uuid); " \
                         "CREATE UNIQUE INDEX IF NOT EXISTS inx_images_filename on tbl_images(filename); " \
                         "CREATE INDEX IF NOT EXISTS inx_images_camara_type on tbl_images(camera_brand);" \
                         "CREATE INDEX IF NOT EXISTS inx_images_country on tbl_images(country);" \
                         "CREATE INDEX IF NOT EXISTS inx_images_province on tbl_images(province);" \
                         "CREATE INDEX IF NOT EXISTS inx_images_city on tbl_images(city);"
        sql_init_values = "INSERT INTO tbl_options (name, value) values ('version', '1');"

        sql_version_1 = str(sql_init_tables + sql_init_index + sql_init_values).split(";")
        self.execute_multi(sql_version_1 )


def get_db_session(full_db_name):
    full_db_name = os.path.expanduser(full_db_name)
    engine = create_engine('sqlite:///{dbname}'.format(dbname=full_db_name))
    Base.metadata.create_all(engine)
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    return session