# Copyright 2009, BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

import zope.lifecycleevent
from zope.interface import implements
from zope.lifecycleevent import (
    ObjectCreatedEvent,
    ObjectAddedEvent,
    ObjectModifiedEvent,
    ObjectRemovedEvent,
)
from zodict.interfaces import (
    INodeCreatedEvent,
    INodeAddedEvent,
    INodeModifiedEvent,
    INodeRemovedEvent,
    INodeDetachedEvent,
)

class NodeCreatedEvent(ObjectCreatedEvent):
    implements(INodeCreatedEvent)
    
class NodeAddedEvent(ObjectAddedEvent):
    implements(INodeAddedEvent)

class NodeModifiedEvent(ObjectModifiedEvent):
    implements(INodeModifiedEvent)

class NodeRemovedEvent(ObjectRemovedEvent):              
    implements(INodeRemovedEvent)

class NodeDetachedEvent(ObjectRemovedEvent):
    implements(INodeDetachedEvent)