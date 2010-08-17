from zodict._zodict import Zodict
from zodict._zodict import ReverseMapping
from zodict._zodict import AttributeAccess
from zodict.node import Node
from zodict.node import AttributedNode
from zodict.node import LifecycleNode
from zodict.composition import Composition

#BBB - will be removed with 2.x release 
import sys
sys.modules['zodict.zodict'] = _zodict
