# Copyright 2009, BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2 or later

import uuid
from zodict import zodict
from zope.interface import implements
from zope.location import LocationIterator
from interfaces import INode
from deco import accepts, returns

class Node(zodict):
    """Base node implementation.
    """
    implements(INode)
    
    def __init__(self, name=None):
        zodict.__init__(self)
        self.__parent__ = None
        self.__name__ = name
        self._index = dict()
        self._uuid = None
        self.uuid = uuid.uuid4()
    
    def __setitem__(self, key, val):
        if val.uuid in self._index.keys():
            raise ValeError(u"Node with uuid already exists")
        val.__name__ = key
        val.__parent__ = self
        val._index = self._index
        self._index[val.uuid] = val
        zodict.__setitem__(self, key, val)
    
    @accepts(object, uuid.UUID)
    def set_uuid(self, uuid):
        if uuid in self._index.keys() and self._index[uuid] is not self:
            raise ValueError(u"Given uuid was already used for another Node")
        if self._uuid in self._index.keys():
            del self._index[self._uuid]
        self._index[uuid] = self
        self._uuid = uuid
    
    @returns(uuid.UUID)
    def get_uuid(self):
        return self._uuid
    
    uuid = property(get_uuid, set_uuid)
    
    @property
    def path(self):
        path = list()
        for parent in LocationIterator(self):
            path.append(parent.__name__)
        path.reverse()
        return path
    
    def node(self, uuid):
        return self._index.get(uuid)
    
    def filtereditems(self, interface):
        for node in self.values():
            if interface.providedBy(node):
                yield node
    
    def __repr__(self):
        return '<Node object \'%s\' at %s>' % (self.__name__,
                                               hex(id(self))[:-1])
    
    __str__ = __repr__