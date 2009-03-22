# Copyright 2009, BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2 or later

from zodict import zodict
from zope.interface import implements
from zope.location import LocationIterator
from interfaces import INode

class Node(zodict):
    """Base node implementation.
    """
    implements(INode)
    
    def __init__(self, name=None):
        zodict.__init__(self)
        self.__parent__ = None
        self.__name__ = name
    
    def __setitem__(self, key, val):
        val.__name__ = key
        val.__parent__ = self
        zodict.__setitem__(self, key, val)
    
    @property
    def path(self):
        path = list()
        for parent in LocationIterator(self):
            path.append(parent.__name__)
        path.reverse()
        return path
    
    def filtereditems(self, interface):
        for node in self.values():
            if interface.providedBy(node):
                yield node
    
    def __repr__(self):
        return '<Node object \'%s\' at %s>' % (self.__name__,
                                               hex(id(self))[:-1])
    
    __str__ = __repr__