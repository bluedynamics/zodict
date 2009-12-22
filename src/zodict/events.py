# Copyright 2009, BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

import zope.lifecycleevent
from zope.interface import implements
from zodict.interfaces import (
    INodeCreatedEvent,
    INodeAddedEvent,
    INodeModifiedEvent,
    INodeRemovedEvent,
    INodeDetachedEvent,
)

class NodeCreatedEvent(zope.lifecycleevent.ObjectCreatedEvent):
    """A Node has been created.
    """
    implements(INodeCreatedEvent)
    
class NodeAddedEvent(zope.lifecycleevent.ObjectAddedEvent):
    """A Node has been added to its parent.
    """
    implements(INodeAddedEvent)

class NodeModifiedEvent(zope.lifecycleevent.ObjectModifiedEvent):
    """An Node has been modified.
    """
    implements(INodeModifiedEvent)

class NodeRemovedEvent(zope.lifecycleevent.ObjectRemovedEvent):
    """A Node was removed from it parent.
    """               
    implements(INodeRemovedEvent)

class NodeDetachedEvent(zope.lifecycleevent.ObjectRemovedEvent):
    """A Node was detached from its parent.
    """
    implements(INodeDetachedEvent)