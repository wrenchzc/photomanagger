import re
import typing
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import func, or_, and_

from photomanager.lib.errors import FilterError, FilterInvalidError
from photomanager.db.models import ImageMeta

FILTER_FIELD_DATE = "date"


class FilterParser(object):

    def __init__(self, condition: str):
        self.condition = condition

    def parse(self) -> BinaryExpression:
        pattern = "(.*?)\.(.*?):(.*)"
        matched = re.match(pattern, self.condition)
        if not matched:
            raise FilterError

        if len(matched.groups()) != 3:
            raise FilterError()

        field, operator, val = matched.groups()
        if field == FILTER_FIELD_DATE:
            val = self.standard_date_str(val)
            return self.do_parse_time_field(operator, val)

    def do_parse_time_field(self, operator: str, val: str) -> BinaryExpression:
        # date is a sqlite function
        # must use Model.field == None, not Model.field is None, because the operator "==" override by sqlalchemy
        if operator == "eq":
            return or_(func.date(ImageMeta.origin_datetime) == val,
                       and_(func.date(ImageMeta.file_createtime) == val,
                            ImageMeta.origin_datetime == None))
        elif operator == "gt":
            return or_(func.date(ImageMeta.origin_datetime) > val,
                       and_(func.date(ImageMeta.file_createtime) > val,
                            ImageMeta.origin_datetime == None))
        elif operator == "gte":
            return or_(func.date(ImageMeta.origin_datetime) >= val,
                       and_(func.date(ImageMeta.file_createtime) >= val,
                            ImageMeta.origin_datetime == None))
        elif operator == "lt":
            return or_(func.date(ImageMeta.origin_datetime) < val,
                       and_(func.date(ImageMeta.file_createtime) < val,
                            ImageMeta.origin_datetime == None))
        elif operator == "lte":
            return or_(func.date(ImageMeta.origin_datetime) <= val,
                       and_(func.date(ImageMeta.file_createtime) <= val,
                            ImageMeta.origin_datetime == None))

    def standard_date_str(self, val: str):
        if len(val) < 8 or len(val) > 10:
            raise FilterInvalidError

        return_val = val
        if len(val) == 8:  # such as 20201005
            return_val = val[0:4] + "-" + val[4:6] + '-' + val[6:]

        return return_val


class FiltersParser(object):
    def __init__(self, conditions: typing.List[str]):
        self.conditions = conditions

    def parse(self):
        expr = None
        for cond in self.conditions:
            cur_expr = FilterParser(cond).parse()
            if expr is not None:
                expr = and_(expr, cur_expr)
            else:
                expr = cur_expr

        return expr
