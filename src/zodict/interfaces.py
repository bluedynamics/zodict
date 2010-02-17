# Copyright 2009, Blue Dynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

from zope.interface import Interface, Attribute
from zope.interface.common.mapping import (
    IEnumerableMapping,                            
    IWriteMapping,
    IFullMapping,
)
try:
    from zope.app.location.interfaces import ILocation # BBB
except ImportError, e:
    from zope.location.interfaces import ILocation
try:
    from zope.lifecycleevent import (
        IObjectCreatedEvent,
        IObjectAddedEvent,
        IObjectModifiedEvent,
        IObjectRemovedEvent,
    )
except ImportError, e: # BBB
    from zope.app.event.interfaces import IObjectEvent
    class IObjectCreatedEvent(IObjectEvent): pass
    class IObjectAddedEvent(IObjectEvent): pass
    class IObjectModifiedEvent(IObjectEvent): pass
    class IObjectRemovedEvent(IObjectEvent): pass

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
        you first have to detach it from the tree.
        """
    
    def insertafter(newnode, refnode):
        """Insert newnode after refnode.
        
        __name__ on newnode must be set.
        
        This function only supports adding of new nodes, for moving nodes,
        you first have to detach it from the tree.
        """
    
    def detach(key):
        """Detach child Node. needed for Node movement.
        """
    
    def printtree():
        """Debugging helper.
        """

class IRoot(INode):
    """Marker for a root node.
    """

class ILeaf(INode):
    """A node without children.
    """

class ICallableNode(INode):
    """Node which implements the ``__call__`` function.
    """
    
    def __call__():
        """Expose the tree contents to an output channel.
        """

class INodeAttributes(IEnumerableMapping, IWriteMapping):
    """Interface describing the attributes of a (lifecycle) Node.
    
    Promise to throw modification related events when calling IWriteMapping
    related functions.
    
    You do not instanciate this kind of object directly. This is done due to
    ``LifecycleNode.attributes`` access. You can provide your own
    ``INodeAttributes`` implementation by setting
    ``LifecycleNode.attributes_factory``. 
    """
    changed = Attribute(u"Flag indicating if attributes were changed or not.")
    
    def __init__(node):
        """Initialize object.
        
        Takes attributes refering node at creation time.
        """

class ILifecycleNode(INode):
    """Node which care about its lifecycle.
    """
    events = Attribute(u"Dict with lifecycle event classes to use for "
                       u"notification.")
    attributes = Attribute(u"``INodeAttributes`` implementation.")
    attributes_factory = Attribute(u"``INodeAttributes`` implementation class")

class INodeCreatedEvent(IObjectCreatedEvent):
    """An new Node was born.
    """        

class INodeAddedEvent(IObjectAddedEvent):
    """An Node has been added to its parent.
    """        

class INodeModifiedEvent(IObjectModifiedEvent):
    """An Node has been modified.
    """

class INodeRemovedEvent(IObjectRemovedEvent):
    """An Node has been removed from its parent.
    """

class INodeDetachedEvent(IObjectRemovedEvent):
    """An Node has been detached from its parent.
    """