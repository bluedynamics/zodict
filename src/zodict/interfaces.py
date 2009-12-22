# Copyright 2009, Blue Dynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

from zope.interface import Interface, Attribute
from zope.interface.common.mapping import IFullMapping
from zope.location.interfaces import ILocation
import zope.lifecycleevent

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

class ILifecycleNode(INode):
    """Node which care about its lifecycle.
    """
    
    attributes = Attribute(u"``zodict.node.NodeAttributes`` object.")

class INodeCreatedEvent(zope.lifecycleevent.IObjectCreatedEvent):
    """An new Node was born.
    """        

class INodeAddedEvent(zope.lifecycleevent.IObjectAddedEvent):
    """An Node has been added to its parent.
    """        

class INodeModifiedEvent(zope.lifecycleevent.IObjectModifiedEvent):
    """An Node has been modified.
    """

class INodeRemovedEvent(zope.lifecycleevent.IObjectRemovedEvent):
    """An Node has been removed from its parent.
    """

class INodeDetachedEvent(zope.lifecycleevent.IObjectRemovedEvent):
    """An Node has been detached from its parent.
    """