import logging
import typing as t

from .. import not_set
from .. import utils
from ..types_ import StrList
from ..types_ import StrListType
from .handlers import Handler


class Logger(not_set.Logger):
    level: t.Optional[str] = utils.get_level_name(logging.DEBUG)
    handlers: t.Optional[StrListType] = StrList(root=[Handler.NAME])
