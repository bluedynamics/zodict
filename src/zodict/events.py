# Copyright 2009, BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2 or later

import zope.lifecycleevent
from zope.interface import implements
from interfaces import (
    INodeCreatedEvent,
    INodeAddedEvent,
    INodeRemovedEvent,
    INodeDetachedEvent,
)

class NodeCreatedEvent(zope.lifecycleevent.ObjectCreatedEvent):
    """A Node has been created."""
    implements(INodeCreatedEvent)
    
class NodeAddedEvent(zope.lifecycleevent.ObjectAddedEvent):
    """A Node has been added to its parent"""
    implements(INodeAddedEvent)

class NodeRemovedEvent(zope.lifecycleevent.ObjectRemovedEvent):
    """A Node was removed from it parent."""               
    implements(INodeRemovedEvent)

class NodeDetachedEvent(zope.lifecycleevent.ObjectRemovedEvent):
    """A Node was detached from its parent."""
    implements(INodeDetachedEvent)