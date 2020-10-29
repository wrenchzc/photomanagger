from photomanager.commands.base import Command
from photomanager.db.imagehandler import ImageDBHandler
from photomanager.db.models import ImageMeta
from photomanager.utils.geoutils import get_address_by_lat_lng
from photomanager.utils.logger import logger


class CommandUpdate(Command):
    def __init__(self, folder, params):
        Command.__init__(self, folder, params)
        self.update_geoinfo = params.get("geoinfo", False)
        self.handler = ImageDBHandler(folder, self.db_session, skip_existed=False)

    def do(self):
        if self.update_geoinfo:
            self._update_address_by_geoinfo()

    def _update_address_by_geoinfo(self):
        items = self.db_session.query(ImageMeta).filter(ImageMeta.latitude != None, ImageMeta.longitude != None,
                                                        ImageMeta.address == None).all()
        totol_count = len(items)
        for inx, item in enumerate(items):
            logger.info(f"update geoinfo, {inx + 1}/{totol_count}")
            self._update_item_address(item)

    def _update_item_address(self, item: ImageMeta):
        logger.info(f"update address by geoinfo, folder is {item.folder}, filename is {item.filename}")
        lat = item.latitude
        lng = item.longitude
        logger.info(f"lat is {lat}, lng is {lng}, locate to address")
        address = get_address_by_lat_lng(lat, lng)
        logger.info(f"lat is {lat}, lng is {lng}, address is {address}")
        if address:
            item.address = address
            self.db_session.add(item)
            self.db_session.commit()
