import interfaces
import aliaser
import composition
import events
import locking
import testing
import _zodict
import _node
from node.utils import (
    Zodict,
    ReverseMapping,
    AttributeAccess,
)
from node.base import (
    Node,
    AttributedNode,
    LifecycleNode,
)
from node.composition import Composition
#BBB - will be removed with 2.x release 
import sys
sys.modules['zodict.zodict'] = _zodict
sys.modules['zodict.node'] = _node