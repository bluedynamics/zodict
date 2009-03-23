# Copyright 2009, Blue Dynamics Alliance - http://bluedynamics.com
# GNU General Public Licence Version 2 or later

from zope.interface import Attribute
from zope.interface.common.mapping import IFullMapping
from zope.location.interfaces import ILocation

class INode(ILocation, IFullMapping):
    """A node.
    """
    
    uuid = Attribute(u"UUID of this node.")
    
    path = Attribute(u"Path of target element as list")
    
    def node(uuid):
        """Return node by uuid located anywhere in this nodetree.
        """
    
    def filtereditems(interface):
        """Return filtered child nodes by interface.
        """