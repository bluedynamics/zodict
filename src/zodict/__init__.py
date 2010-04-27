from zodict._zodict import Zodict
from zodict.node import Node
from zodict.node import AttributedNode
from zodict.node import LifecycleNode

#BBB - will be removed with 2.x release 
import sys
sys.modules['zodict.zodict'] = _zodict