from photomanager.db.models import Option
from sqlalchemy.orm import Session


class Config(object):

    def __init__(self, db_session: Session):
        self.session = db_session

    def set_value(self, name: str, value):
        option = self.session.query(Option).filter(Option.name == name).first()

        if not option:
            option = Option()
            option.name = name

        option.value = str(value)
        self.session.add(option)
        self.session.commit()

    def get_value(self, name) -> str:
        opt = self.session.query(Option).filter(Option.name == name).first()
        if opt:
            return opt.value
