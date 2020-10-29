from tests.utils import remove_file
from photomanager.lib.pmconst import PMDBNAME
from photomanager.commands.index import CommandIndex
from photomanager.commands.update import CommandUpdate
from photomanager.db.dbutils import get_db_session, close_db_session
from photomanager.db.models import ImageMeta

cmd_inx_test_root = 'tests/data'


class TestDisplayImg(object):

    @classmethod
    def setup_class(cls):
        cls._clear()
        cls._do_index()

    @classmethod
    def teardown_class(cls):
        cls._clear()
        db_filename = cmd_inx_test_root + '/' + PMDBNAME
        remove_file(db_filename)

    @staticmethod
    def _clear():
        db_filename = cmd_inx_test_root + '/' + PMDBNAME
        close_db_session(db_filename)

    @staticmethod
    def _do_index():
        command_index = CommandIndex(cmd_inx_test_root, {})
        cnt = command_index.do()

    def setup_method(self):
        self._clear()

    def teardown_method(self):
        self._clear()


    def test_update_address_by_geoinfo(self):
        command_update = CommandUpdate(cmd_inx_test_root, {"geoinfo": True})
        command_update.do()
        test2_meta = command_update.handler.session.query(ImageMeta).filter(ImageMeta.filename == "test2.jpg").first()
        assert ("汝城" in test2_meta.address)
