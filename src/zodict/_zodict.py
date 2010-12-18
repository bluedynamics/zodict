from node.utils import (
    Zodict,
    ReverseMapping,
    AttributeAccess,
)

zodict = Zodict
from zope.deprecation import deprecated
deprecated('zodict', "``zodict`` has been renamed to ``Zodict``. Please "
                     "modify your code and import to use: "
                     "``from node.utils import Zodict``")