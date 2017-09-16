import os
from src.db.dbutils import IndexDB
from src.db.imagehandler import ImageDBHandler


def test_init_db():
    if os.path.exists('pmindex.db'):
        os.remove('pmindex.db')

    values = _do_init_db()
    assert values[0] == (1,)
    values = _do_init_db()
    assert values[0] == (1,)

    os.remove('pmindex.db')


def _do_init_db():
    inx_db = IndexDB(".")
    query_sql = "SELECT COUNT(*) FROM sqlite_master where type='table' and name='{table_name}'".format(
        table_name="tbl_images")
    values = inx_db.query(query_sql)
    return values


def test_single_image():
    inx_db = IndexDB(".")
    image_handler = ImageDBHandler(inx_db)
    files = ["data/test1.jpg", "data/test4.jpg"]
    image_handler.do_index(files)
    query_sql = "SELECT * from tbl_images"
    values = inx_db.query(query_sql)
    assert len(values) == 2
    assert values[0][0] == 1
    assert values[0][2] == u'data/test1.jpg'
    assert values[0][6] == 1200
    assert values[0][7] == 1600
    assert values[1][0] == 2
    assert values[1][2] == u'data/test4.jpg'
    assert values[1][6] == 1057
    assert values[1][7] == 1123
