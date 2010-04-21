# Copyright 2009, BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

import uuid
import inspect
from odict.pyodict import _nil
from zope.interface import implements
from zope.interface.common.mapping import IReadMapping
try:
    from zope.app.location import LocationIterator # BBB
except ImportError, e:
    from zope.location import LocationIterator
try:
    from zope.app.event.objectevent import objectEventNotify # BBB
except ImportError, e:
    from zope.component.event import objectEventNotify
from zodict import Zodict
from zodict.interfaces import (
    INode,
    INodeAttributes,
    ILifecycleNode,
)
from zodict.events import (
    NodeCreatedEvent,
    NodeAddedEvent,
    NodeRemovedEvent,
    NodeModifiedEvent,
    NodeDetachedEvent,
)
    
class NodeIndex(object):
    implements(IReadMapping)
    
    def __init__(self, index):
        self._index = index
    
    def __getitem__(self, key):
        return self._index[int(key)]
    
    def get(self, key, default=None):
        return self._index.get(int(key), default)
    
    def __contains__(self, key):
        return int(key) in self._index

class Node(Zodict):
    implements(INode)

    def __init__(self, name=None):
        """
        ``name``
            optional name used for ``__name__`` declared by ``ILocation``.
        """  
        Zodict.__init__(self)
        self.__parent__ = None
        self.__name__ = name
        self._index = dict()
        self._uuid = None
        self.uuid = uuid.uuid4()

    def __setitem__(self, key, val):
        if inspect.isclass(val):
            raise ValueError, u"It isn't allowed to use classes as values."
        has_children = False
        for valkey in val.iterkeys():
            has_children = True
            break
        if has_children:
            keys = set(self._index.keys())
            if keys.intersection(val._index.keys()):
                raise ValueError, u"Node with uuid already exists"
        val.__name__ = key
        val.__parent__ = self
        self._index.update(val._index)
        val._index = self._index
        Zodict.__setitem__(self, key, val)
                                                       
    def _to_delete(self):
        todel = [int(self.uuid)]
        for childkey in self:
            todel += self[childkey]._to_delete()
        return todel

    def __delitem__(self, key):
        val = self[key]
        for iuuid in self[key]._to_delete():
            del self._index[iuuid]
        Zodict.__delitem__(self, key)

    def _get_uuid(self):
        return self._uuid
    
    def _set_uuid(self, uuid):
        iuuid = uuid is not None and int(uuid) or None
        if iuuid in self._index and self._index[iuuid] is not self:
            raise ValueError, u"Given uuid was already used for another Node"
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
        return NodeIndex(self._index)

    def node(self, uuid):
        return self._index.get(int(uuid))

    def filtereditems(self, interface):
        for node in self.values():
            if interface.providedBy(node):
                yield node
    
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
    
    def _index_nodes(self):
        for node in self.values():
            self._index[int(node.uuid)] = node
            node._index = self._index
            node._index_nodes() 

    def detach(self, key):
        node = self[key]
        del self[key]
        node._index = { int(node.uuid): node }
        node._index_nodes()
        return node
            
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

class NodeAttributes(dict):
    implements(INodeAttributes)
    
    def __init__(self, node):
        super(NodeAttributes, self).__init__()
        object.__setattr__(self, '_node', node)
        object.__setattr__(self, 'changed', False)
    
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value
    
    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
        object.__setattr__(self, 'changed', True)
        node = object.__getattribute__(self, '_node')
        if node._notify_suppress: 
            return
        objectEventNotify(node.events['modified'](node))
    
    def __delitem__(self, key):
        dict.__delitem__(self, key)
        object.__setattr__(self, 'changed', True)
        node = object.__getattribute__(self, '_node')
        if self._node._notify_suppress: 
            return
        if node._notify_suppress: 
            return
        objectEventNotify(node.events['modified'](node))
        
    def __copy__(self):
        _new = NodeAttributes(object.__getattribute__(self, '_node'))
        for key, value in self.items():
            _new[key] = value
        _new.changed = object.__getattribute__(self, 'changed')
        return _new

class LifecycleNode(Node):
    implements(ILifecycleNode)
    
    events = {
        'created': NodeCreatedEvent,
        'added': NodeAddedEvent,
        'modified': NodeModifiedEvent,
        'removed': NodeRemovedEvent,
        'detached': NodeDetachedEvent,
    }
    attributes_factory = NodeAttributes
    
    @property
    def attrs(self):
        if not hasattr(self, '_attributes'):
            self._attributes = self.attributes_factory(self)
        return self._attributes
    
    # BBB
    attributes = attrs
    
    def __init__(self, name=None):
        super(LifecycleNode, self).__init__(name=name)
        self._notify_suppress = False        
        objectEventNotify(self.events['created'](self))
    
    def __setitem__(self, key, val):
        super(LifecycleNode, self).__setitem__(key, val)
        if self._notify_suppress: 
            return
        objectEventNotify(self.events['added'](val, newParent=self, 
                                               newName=key))
        
    def __delitem__(self, key):
        delnode = self[key]
        super(LifecycleNode, self).__delitem__(key)
        if self._notify_suppress: 
            return
        objectEventNotify(self.events['removed'](delnode, oldParent=self, 
                                                 oldName=key))

    def detach(self, key):
        notify_before = self._notify_suppress
        self._notify_suppress = True
        node = super(LifecycleNode, self).detach(key)
        self._notify_suppress = False
        objectEventNotify(self.events['detached'](node, oldParent=self, 
                                                  oldName=key))
        return node