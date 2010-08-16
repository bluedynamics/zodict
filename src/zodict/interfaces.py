# Copyright 2009, Blue Dynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

from zope.interface import Interface, Attribute
from zope.interface.common.mapping import (
    IEnumerableMapping,
    IWriteMapping,
    IFullMapping,
)
try:
    from zope.location.interfaces import ILocation
except ImportError, e:
    from zope.app.location.interfaces import ILocation # BBB
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
    aliases = Attribute(u"zope.interface.common.mapping.IEnumerableMapping "
                        u"implementation defining key aliases or callable "
                        u"accepting Node as argument. If aliases is None, "
                        u"this feature is disables.")

    def node(uuid):
        """Return node by uuid located anywhere in this nodetree.
        """

    def filtereditems(interface):
        """Return filtered child nodes by interface.
        """

    def insertbefore(newnode, refnode):
        """Insert newnode before refnode.

        __name__ on newnode must be set.

        This function only supports adding of new nodes before the given
        refnode. If you want to move nodes you have to detach them from the
        tree first.
        """

    def insertafter(newnode, refnode):
        """Insert newnode after refnode.

        __name__ on newnode must be set.

        This function only supports adding of new nodes after the given
        refnode. If you want to move nodes you have to detach them from the
        tree first.
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
    aliases = Attribute(u"zope.interface.common.mapping.IEnumerableMapping "
                        u"implementation defining attr name aliases or "
                        u"callable accepting NodeAttributes as argument. If "
                        u"aliases is None, this feature is disables. "
                        u"Serves as Whitelist.")

    def __init__(node):
        """Initialize object.

        Takes attributes refering node at creation time.
        """

class IAttributedNode(INode):
    """Node which care about its attributes.
    """
    attributes = Attribute(u"``INodeAttributes`` implementation.")
    attributes_factory = Attribute(u"``INodeAttributes`` implementation class")

class ILifecycleNode(IAttributedNode):
    """Node which care about its lifecycle.
    """
    events = Attribute(u"Dict with lifecycle event classes to use for "
                       u"notification.")

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
