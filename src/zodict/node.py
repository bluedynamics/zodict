# Copyright 2009, BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2 or later

import uuid
import inspect
from threading import Lock
from odict.pyodict import _nil
from zodict import zodict
from zope.interface import implements
from zope.location import LocationIterator
from interfaces import INode

class TreeLock(object):
    
    def __init__(self, node):
        root = node.root
        self.lock = getattr(root, '_treelock', None)
        if self.lock is None:
            self.lock = root._treelock = Lock()
            
    def __enter__(self):
        self.lock.acquire()
        
    def __exit__(self, type, value, traceback):
        self.lock.release()    


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
        if inspect.isclass(val):
            raise ValueError, u"It isn't allowed to use classes as values."
        has_children = False
        for key in val.iterkeys():
            has_children = True
            break
        if has_children:
            keys = set(self._index.keys())
            if keys.intersection(val._index.keys()):
                raise ValueError, u"Node with uuid already exists"
        with TreeLock(self):  
            val.__name__ = key
            val.__parent__ = self
            self._index.update(val._index)
            val._index = self._index
            zodict.__setitem__(self, key, val)
            
    def _del_from_index(self):
        for childkey in self:
            self[childkey]._del_from_index()
        iuuid = int(self.uuid)
        del self._index[iuuid]
        self._index = { iuuid: self }

    def __delitem__(self, key):
        with TreeLock(self):
            self[key]._del_from_index()
            zodict.__delitem__(self, key)

    def _get_uuid(self):
        return self._uuid
    
    def _set_uuid(self, uuid):
        iuuid = uuid is not None and int(uuid) or None
        if iuuid in self._index and self._index[iuuid] is not self:
            raise ValueError, u"Given uuid was already used for another Node"
        with TreeLock(self):  
            siuuid = self._uuid is not None and int(self._uuid) or None
            if siuuid in self._index:
                del self._index[siuuid]
            self._index[iuuid] = self
            self._uuid = uuid

    uuid = property(_get_uuid, _set_uuid)

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
        return self._index.get(int(uuid))

    def filtereditems(self, interface):
        for node in self.values():
            if interface.providedBy(node):
                yield node
    
    def insertbefore(self, newnode, refnode):
        with TreeLock(self):  
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
        with TreeLock(self):  
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
            raise ValueError, u"Given node has no __name__ set."
        if self.node(newnode.uuid) is not None:
            raise KeyError, u"Given node already contained in tree."
        index = self._nodeindex(refnode)
        if index is None:
            raise ValueError, u"Given reference node not child of self."
    
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