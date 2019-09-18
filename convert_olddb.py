import sqlalchemy
import os
from photomanager.db.dbutils import get_db_session
from photomanager.db.models import ImageMeta


def do_convert(db_name):
  db_session = get_db_session(db_name)

  image_metas = db_session.query(ImageMeta)
  for meta in image_metas:
      filename = meta.filename
      dirname = os.path.dirname(filename)
      basename = os.path.basename(filename)
      print(f"{filename} split to {dirname} and {basename}")
      meta.folder = dirname
      meta.filename = basename

  db_session.commit()



do_convert("/home/zhangchi/data/Photos/pmindex.db")
