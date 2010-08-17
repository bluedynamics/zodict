# Copyright 2009, BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

import uuid
import inspect
from odict import odict
from odict.pyodict import _nil
from zope.interface import implements
from zope.interface.common.mapping import IReadMapping
try:
    from zope.location import LocationIterator
except ImportError, e:
    from zope.app.location import LocationIterator # BBB
try:
    from zope.component.event import objectEventNotify
except ImportError, e:
    from zope.app.event.objectevent import objectEventNotify # BBB
from zodict import Zodict
from zodict.interfaces import (
    INode,
    INodeAttributes,
    IAttributedNode,
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

class _Node(object):
    """Abstract node implementation. Subclass must mixin ``_node_impl()``.
    """
    implements(INode)
    
    def _node_impl(self):
        return None

    def __init__(self, name=None, index=True):
        """
        ``name``
            optional name used for ``__name__`` declared by ``ILocation``.
        ``index``
            flag wether node index is enabled or not.
        """
        super(self._node_impl(), self).__init__()
        self.__parent__ = None
        self.__name__ = name
        if index:
            self._index = dict()
            self._uuid = None
            self.uuid = uuid.uuid4()
        else:
            self._index = None
        self.allow_non_node_childs = False
        self.aliases = None

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        return True

    def _aliased(self, key):
        try:
            key = self.aliases.__getitem__(key)
        except AttributeError:
            # aliases is None
            pass
        return key

    def __getitem__(self, key):
        try:
            return self._node_impl().__getitem__(self, self._aliased(key))
        except KeyError:
            raise KeyError(key)

    def _aliased_iter(self):
        # XXX: secondary key could be used here, ie to implement a reverse dict
        for key in self._node_impl().__iter__(self):
            for k,v in self.aliases.items():
                if v == key:
                    yield k

    def __iter__(self):
        if self.aliases is None:
            return self._node_impl().__iter__(self)
        return self._aliased_iter()

    def keys(self):
        return [x for x in self]

    def __setitem__(self, key, val):
        if inspect.isclass(val):
            raise ValueError, u"It isn't allowed to use classes as values."
        if not isinstance(val, _Node) and not self.allow_non_node_childs:
            raise ValueError("Non-node childs are not allowed.")
        if isinstance(val, _Node):
            val.__name__ = key
            val.__parent__ = self
            has_children = False
            for valkey in val.iterkeys():
                has_children = True
                break
            if has_children and self._index is not None:
                keys = set(self._index.keys())
                if keys.intersection(val._index.keys()):
                    raise ValueError, u"Node with uuid already exists"
            if self._index is not None:
                self._index.update(val._index)
                val._index = self._index
        # XXX: Using the name our parent gives us seems more consistent, the
        # application needs to show whether its good or bad.
        key = self._aliased(key)
        self._node_impl().__setitem__(self, key, val)

    def _to_delete(self):
        todel = [int(self.uuid)]
        for childkey in self:
            try:
                todel += self[childkey]._to_delete()
            except AttributeError:
                # Non-Node values are not told about deletion
                continue
        return todel

    def __delitem__(self, key):
        key = self._aliased(key)
        val = self[key]
        if self._index is not None:
            for iuuid in self[key]._to_delete():
                del self._index[iuuid]
        self._node_impl().__delitem__(self, key)

    def _get_uuid(self):
        return self._uuid

    def _set_uuid(self, uuid):
        iuuid = uuid is not None and int(uuid) or None
        if self._index is not None \
          and iuuid in self._index \
          and self._index[iuuid] is not self:
            raise ValueError, u"Given uuid was already used for another Node"
        siuuid = self._uuid is not None and int(self._uuid) or None
        if self._index is not None and siuuid in self._index:
            del self._index[siuuid]
        if self._index is not None:
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
        if self._index is None:
            raise AttributeError(u"No index support configured on this Node.")
        return NodeIndex(self._index)

    def node(self, uuid):
        if self._index is None:
            raise ValueError(u"No index support configured on this Node.")
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
            try:
                uuid = int(node.uuid)
            except AttributeError:
                # non-Node values are a dead end, no magic for them
                continue
            self._index[uuid] = node
            node._index = self._index
            node._index_nodes()

    def detach(self, key):
        node = self[key]
        del self[key]
        if self._index is not None:
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
            try:
                node.printtree(indent+2)
            except AttributeError:
                # Non-Node values are just printed
                print "%s%s" % (indent * ' ', node)

    def __repr__(self):
        return "<%s object '%s' at %s>" % (self.__class__.__name__,
                                           str(self.__name__),
                                           hex(id(self))[:-1])

    __str__ = __repr__

class Node(_Node, Zodict):
    """Inherit from _Node and mixin Zodict.
    """
    def _node_impl(self):
        return Zodict

class NodeAttributes(dict):
    """
    If this would be a kind of Node, what would be?

    __parent__ -> node, whose attributes we would be
    __name__ our childs are all kind of root nodes 
    index=False

    attrs would be just another nodespace like the one behind self[]
    """
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

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        object.__setattr__(self, 'changed', True)

    def __copy__(self):
        _new = NodeAttributes(object.__getattribute__(self, '_node'))
        for key, value in self.items():
            _new[key] = value
        _new.changed = object.__getattribute__(self, 'changed')
        return _new

class AttributedNode(Node):
    """A node that has another nodespace behind self.attrs[]
    """
    implements(IAttributedNode)

    #attributes_factory = NodeAttributes
    attributes_factory = None

    # enable subclasses to override this
    _attrmap = None

    def __init__(self, name=None, attrmap=None, index=True):
        super(AttributedNode, self).__init__(name, index=index)
        if attrmap is not None:
            self._attrmap = attrmap

    @property
    def attrs(self):
        try:
            return self._attributes
        except AttributeError:
            _class = self.attributes_factory or self.__class__
            self._attributes = _class(self, index=False)
            self._attributes.allow_non_node_childs = True
            return self._attributes

    # BBB
    attributes = attrs


class LifecycleNodeAttributes(NodeAttributes):
    """XXX If we merge this into node, do we really need the event on the node?
    a) LifecycleNode current would trigger event on the attrs node
    b) we use to trigger only on the node not on us, shall we suppress us and
       trigger on node instead (imagine we are an LifecycleNode configured to be
       used for the attrs nodespace
    c) we raise an event on us (the attrs nodespace) and on our parent node, that
       keeps us in .attrs
    """

    def __setitem__(self, key, val):
        NodeAttributes.__setitem__(self, key, val)
        node = object.__getattribute__(self, '_node')
        if node._notify_suppress:
            return
        objectEventNotify(node.events['modified'](node))

    def __delitem__(self, key):
        NodeAttributes.__delitem__(self, key)
        node = object.__getattribute__(self, '_node')
        if self._node._notify_suppress:
            return
        if node._notify_suppress:
            return
        objectEventNotify(node.events['modified'](node))

class LifecycleNode(AttributedNode):
    implements(ILifecycleNode)

    events = {
        'created': NodeCreatedEvent,
        'added': NodeAddedEvent,
        'modified': NodeModifiedEvent,
        'removed': NodeRemovedEvent,
        'detached': NodeDetachedEvent,
    }

    #attributes_factory = LifecycleNodeAttributes
    attributes_factory = None # results in self.__class__

    def __init__(self, name=None, attrmap=None, index=True):
        super(LifecycleNode, self).__init__(name=name, attrmap=attrmap,
                                            index=index)
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
