import os
import pytest
from src.db.dbutils import IndexDBRaw, get_db_session
from src.db.models import ImageMeta
from src.db.imagehandler import ImageDBHandler
from src.imageutils import get_folder_image_files
from src.pmconst import PMDBNAME


@pytest.fixture()
def image_handler():
    session = get_db_session(PMDBNAME)
    return ImageDBHandler(".", session)


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


def test_option_todo_index(image_handler):
    image_handler.todo_index = 129
    assert image_handler.todo_index == 129
    image_handler.todo_index = 139
    assert image_handler.todo_index == 139


def test_single_image(image_handler):
    files = ["tests/data/test1.jpg", "tests/data/test4.jpg"]
    image_handler.do_index(files)
    query = image_handler.session.query(ImageMeta)
    image_metas = query.all()

    assert len(image_metas) == 2
    assert image_metas[0].id == 1
    assert image_metas[0].filename == u'./tests/data/test1.jpg'
    assert image_metas[0].image_width == 1200
    assert image_metas[0].image_height == 1600
    assert image_metas[1].id == 2
    assert image_metas[1].filename == u'./tests/data/test4.jpg'
    assert image_metas[1].image_width == 1057
    assert image_metas[1].image_height == 1123


def test_folder_files():
    files = get_folder_image_files('tests/data')
    assert len(files) == 6
    assert "noexif.jpg" in files
    assert "subdir/dlrb.jpg" in files


def test_option_values(image_handler):
    value = image_handler.get_option_value("NO_FIELD")
    assert value is None

    image_handler.set_option_value("TEST_FIELD", "test")
    value = image_handler.get_option_value("TEST_FIELD")
    assert value == "test"
