import os
from src.db.dbutils import IndexDBRaw, get_db_session
from src.db.models import ImageMeta
from src.db.imagehandler import ImageDBHandler
from src.imageutils import get_folder_image_files
from src.pmconst import PMDBNAME


def test_init_db():
    if os.path.exists(PMDBNAME):
        os.remove(PMDBNAME)

    values = _do_init_db()
    assert values[0] == (1,)
    values = _do_init_db()
    assert values[0] == (1,)

    os.remove(PMDBNAME)


def _do_init_db():
    inx_db = IndexDBRaw(".")
    query_sql = "SELECT COUNT(*) FROM sqlite_master where type='table' and name='{table_name}'".format(
        table_name="tbl_images")
    values = inx_db.query(query_sql)
    return values


def test_single_image():
    IndexDBRaw(".")
    session = get_db_session(PMDBNAME)
    image_handler = ImageDBHandler(".", session)
    files = ["data/test1.jpg", "data/test4.jpg"]
    image_handler.do_index(files)
    query = session.query(ImageMeta)
    image_metas = query.all()

    assert len(image_metas) == 2
    assert image_metas[0].id == 1
    assert image_metas[0].filename == u'./data/test1.jpg'
    assert image_metas[0].image_width == 1200
    assert image_metas[0].image_height == 1600
    assert image_metas[1].id == 2
    assert image_metas[1].filename == u'./data/test4.jpg'
    assert image_metas[1].image_width == 1057
    assert image_metas[1].image_height == 1123


def test_folder_files():
    files = get_folder_image_files('data')
    assert len(files) == 6
    assert "noexif.jpg" in files
    assert "subdir/dlrb.jpg" in files
