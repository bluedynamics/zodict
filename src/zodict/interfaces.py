# Copyright 2009, Blue Dynamics Alliance - http://bluedynamics.com
# GNU General Public Licence Version 2 or later

from zope.interface import Interface, Attribute
from zope.interface.common.mapping import IFullMapping
from zope.location.interfaces import ILocation

class INode(ILocation, IFullMapping):
    """A node.
    """
    
    uuid = Attribute(u"``uuid.UUID`` of this node.")
    
    path = Attribute(u"Path of node as list")
    
    root = Attribute(u"Root node")
    
    index = Attribute(u"The tree node index")
    
    def node(uuid):
        """Return node by uuid located anywhere in this nodetree.
        """
    
    def filtereditems(interface):
        """Return filtered child nodes by interface.
        """
    
    def insertbefore(newnode, refnode):
        """Insert newnode before refnode.
        
        __name__ on newnode must be set.
        
        This function only supports adding of new nodes, for moving nodes,
        read node to move, delete it from tree and re-add it elsewhere.
        """
    
    def insertafter(newnode, refnode):
        """Insert newnode after refnode.
        
        __name__ on newnode must be set.
        
        This function only supports adding of new nodes, for moving nodes,
        read node to move, delete it from tree and re-add it elsewhere.
        """
    
    def detach(key):
        """Detach child Node. needed for Node movement.
        """
    
    def printtree():
        """Debugging helper.
        """