# Copyright 2009, BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2 or later

import uuid
import inspect
from odict.pyodict import _nil
from zodict import zodict
from zope.interface import implements
from zope.location import LocationIterator
from interfaces import INode

class Node(zodict):
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
            raise ValueError(u"Node with uuid already exists")
        if inspect.isclass(val):
            raise ValueError(u"It isn't allowed to use classes as values.")
        val.__name__ = key
        val.__parent__ = self
        val._index = self._index
        self._index[val.uuid] = val
        zodict.__setitem__(self, key, val)

    def __delitem__(self, key):
        todelete = self[key]
        childkeys = todelete.keys()
        if childkeys:
            for childkey in childkeys:
                del todelete[childkey]
        del self._index[todelete.uuid]
        zodict.__delitem__(self, key)

    def set_uuid(self, uuid):
        if uuid in self._index.keys() and self._index[uuid] is not self:
            raise ValueError(u"Given uuid was already used for another Node")
        if self._uuid in self._index.keys():
            del self._index[self._uuid]
        self._index[uuid] = self
        self._uuid = uuid

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

    @property
    def root(self):
        root = None
        for parent in LocationIterator(self):
            root = parent
        return root
    
    @property
    def index(self):
        return self._index

    def node(self, uuid):
        return self._index.get(uuid)

    def filtereditems(self, interface):
        for node in self.values():
            if interface.providedBy(node):
                yield node
    
    def insertbefore(self, newnode, refnode):
        self._validateinsertion(newnode, refnode)
        nodekey = newnode.__name__
        refkey = refnode.__name__
        index = self._nodeindex(refnode)
        prevnode = None
        prevkey = None
        if index > 0:
            prevkey = self.keys()[index - 1]
            prevnode = dict.__getitem__(self, prevkey)
        if prevnode is not None:
            dict.__getitem__(self, prevkey)[2] = nodekey
            newnode = [prevkey, newnode, refkey]
        else:
            self.lh = nodekey
            newnode = [_nil, newnode, refkey]
        dict.__getitem__(self, refkey)[0] = nodekey
        dict.__setitem__(self, nodekey, newnode)
        self[nodekey] = newnode[1]
    
    def insertafter(self, newnode, refnode):
        self._validateinsertion(newnode, refnode)
        nodekey = newnode.__name__
        refkey = refnode.__name__
        index = self._nodeindex(refnode)
        nextnode = None
        nextkey = None
        keys = self.keys()
        if index < len(keys) - 1:
            nextkey = self.keys()[index + 1]
            nextnode = dict.__getitem__(self, nextkey)
        if nextnode is not None:
            dict.__getitem__(self, nextkey)[0] = nodekey
            newnode = [refkey, newnode, nextkey]
        else:
            self.lt = nodekey
            newnode = [refkey, newnode, _nil]
        dict.__getitem__(self, refkey)[2] = nodekey
        dict.__setitem__(self, nodekey, newnode)
        self[nodekey] = newnode[1]
    
    def _validateinsertion(self, newnode, refnode):
        nodekey = newnode.__name__
        if nodekey is None:
            raise ValueError(u"Given node has no __name__ set.")
        if self.node(newnode.uuid) is not None:
            raise KeyError(u"Given node already contained in tree.")
        index = self._nodeindex(refnode)
        if index is None:
            raise ValueError(u"Given reference node not child of self.")
    
    def _nodeindex(self, node):
        index = 0
        for key in self.keys():
            if key == node.__name__:
                return index
            index += 1
        return None
            
    @property
    def noderepr(self): 
        name = str(self.__name__)
        return str(self.__class__) + ': ' + name[name.find(':') + 1:]
    
    def printtree(self, indent=0):
        print "%s%s" % (indent * ' ', self.noderepr)
        for node in self.values():
            node.printtree(indent+2)        

    def __repr__(self):
        return "<%s object '%s' at %s>" % (self.__class__.__name__,
                                           str(self.__name__),
                                           hex(id(self))[:-1])

    __str__ = __repr__