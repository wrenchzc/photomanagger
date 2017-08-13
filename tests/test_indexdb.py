import os
from src.db.dbutils import IndexDB


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
