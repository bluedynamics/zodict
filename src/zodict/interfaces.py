# Copyright 2009, Blue Dynamics Alliance - http://bluedynamics.com
# GNU General Public Licence Version 2 or later

from zope.interface import Interface, Attribute
from zope.interface.common.mapping import IFullMapping
from zope.location.interfaces import ILocation

class INode(ILocation, IFullMapping):
    """A node.
    """
    
    uuid = Attribute(u"UUID of this node.")
    
    path = Attribute(u"Path of target element as list")
    
    root = Attribute(u"Root node")
    
    def node(uuid):
        """Return node by uuid located anywhere in this nodetree.
        """
    
    def filtereditems(interface):
        """Return filtered child nodes by interface.
        """
    
    def printtree():
        """Debugging helper.
        """

_RAISE_KEYERROR = object()

class INodeTraverser(Interface):
    """Same interface as zope.traversing.interfaces.ITraverser.
    
    Changed due to huge dependency tail of zope.traversing.
    """

    def traverse(path, default=_RAISE_KEYERROR):
        """Traverse Node(s).
        """