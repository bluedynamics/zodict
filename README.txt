.. contents:: **Table of Contents**

Requires
========

- Python2.4+

Usage
=====

Zodict
------

Ordered dictionary which implements the corresponding
``zope.interface.common.mapping`` interface.
::

    >>> from zope.interface.common.mapping import IFullMapping
    >>> from zodict import Zodict
    >>> zod = Zodict()
    >>> IFullMapping.providedBy(zod)
    True

Node
----

This is a ``zodict`` which provides a location. Location the zope way means
each item in the node-tree knows its parent and its own name.
::

    >>> from zope.location.interface import ILocation
    >>> from zodict import Node
    >>> root = Node('root')
    >>> ILocation.providedBy(Node)
    True
    
    >>> root['child'] = Node()
    >>> root['child'].path
    ['root', 'child']
    
    >>> child = root['child']
    >>> child.__name__
    'child'
    
    >>> child.__parent__
    <Node object 'root' at ...>

The ``filtereditems`` function.
::

    >>> from zope.interface import Interface
    >>> from zope.interface import alsoProvides
    >>> class IMarker(Interface): pass
    >>> alsoProvides(root['child']['subchild'], IMarker)
    >>> IMarker.providedBy(root['child']['subchild'])
    True
    
    >>> for item in root['child'].filtereditems(IMarker):
    ...     print item.path
    ['root', 'child', 'subchild']

UUID related operations on Node.
::

    >>> uuid = root['child']['subchild'].uuid
    >>> uuid
    UUID('...')
    
    >>> root.node(uuid).path
    ['root', 'child', 'subchild']
    
    >>> root.uuid = uuid
    Traceback (most recent call last):
      ...
    ValueError: Given uuid was already used for another Node
    
    >>> import uuid
    >>> newuuid = uuid.uuid4()
    
    >>> root.uuid = newuuid
    >>> root['child'].node(newuuid).path
    ['root']

Node insertion (an insertafter function exist as well).
::

    >>> root['child1'] = Node()
    >>> root['child2'] = Node()
    
    >>> node = Node('child3')
    >>> root.insertbefore(node, root['child2'])
    >>> root.printtree()
    <class 'zodict.node.Node'>: root
      <class 'zodict.node.Node'>: child1
      <class 'zodict.node.Node'>: child3
      <class 'zodict.node.Node'>: child2

Move a node. Therefor we first need to detach the node we want to move from
tree. Then insert the detached node elsewhere. In general, you can insert the
detached node or subtree to a complete different tree.
::

    >>> len(root._index.keys())
    6
    
    >>> node = root.detach('child4')
    >>> node
    <Node object 'child4' at ...>
    
    >>> len(node._index.keys())
    1
    >>> len(root._index.keys())
    5
    
    >>> len(root.values())
    4
    
    >>> root.insertbefore(node, root['child1'])
    >>> root.printtree()
    <class 'zodict.node.Node'>: root
      <class 'zodict.node.Node'>: child4
      <class 'zodict.node.Node'>: child1
      <class 'zodict.node.Node'>: child3
      <class 'zodict.node.Node'>: child5
      <class 'zodict.node.Node'>: child2

Merge 2 Node Trees.
::

    >>> tree1 = Node()
    >>> tree1['a'] = Node()
    >>> tree1['b'] = Node()
    >>> tree2 = Node()
    >>> tree2['d'] = Node()
    >>> tree2['e'] = Node()
    >>> tree1._index is tree2._index
    False
  
    >>> len(tree1._index.keys())
    3
    
    >>> tree1.printtree()
    <class 'zodict.node.Node'>: None
      <class 'zodict.node.Node'>: a
      <class 'zodict.node.Node'>: b
    
    >>> len(tree2._index.keys())
    3
    
    >>> tree2.printtree()
    <class 'zodict.node.Node'>: None
      <class 'zodict.node.Node'>: d
      <class 'zodict.node.Node'>: e
    
    >>> tree1['c'] = tree2
    >>> len(tree1._index.keys())
    6
    
    >> sorted(tree1._index.values(), key=lambda x: x.__name__)
    
    >>> tree1._index is tree2._index
    True
    
    >>> tree1.printtree()
    <class 'zodict.node.Node'>: None
      <class 'zodict.node.Node'>: a
      <class 'zodict.node.Node'>: b
      <class 'zodict.node.Node'>: c
        <class 'zodict.node.Node'>: d
        <class 'zodict.node.Node'>: e
        
LifecycleNode
-------------

The ``LifecycleNode`` is able to send out notifies with object-events based on 
``zope.lifecycleevent`` subclasses.  

Creation of Node
    ``zodict.events.NodeCreatedEvent`` implementing 
    ``zodict.interfaces.INodeCreatedEvent``. 

Adding childs to Node
    ``zodict.events.NodeAddedEvent`` implementing 
    ``zodict.interfaces.INodeAddedEvent``. 

Deleting childs from Node
    ``zodict.events.NodeRemovedEvent`` implementing 
    ``zodict.interfaces.INodeRemovedEvent``. 

Detaching childs from Node
    ``zodict.events.NodeDetachedEvent`` implementing 
    ``zodict.interfaces.INodeDetachedEvent``.
  
In subclasses of Node the event classes can be exchanged by modifying the
class attribute ``events`` on the node. It is a dictionary with the keys:
``['created', 'added', 'removed', 'detached']`` 

Thread safe Locking of a Tree
-----------------------------

Not ``Node`` nor ``LifecycleNode`` are thread safe. Application-builder are
responsible for this. Major reason: Acquiring and releasing locks is an 
expensive operation.

The module ``zodict.locking`` provides a mechanism to lock the whole tree 
thread safe. A class and a decorator is provided. The class is intended to be 
used standalone with some Node, the decorator to be used on subclasses of
``Node`` or ``LifecycleNode``.

``zodict.locking.TreeLock`` is a adapter like class on a Node. It can be used 
in Python > 2.6 within the ``with`` statement.
::

    >>> node = Node()
    >>> with TreeLock(node):
    >>>     # do something on the locked tree
    >>>     node['foo'] = Node()
    
Alternative it can be used in older Python version with in a try: finally.
::     

    >>> from zodict.locking import TreeLock
    >>> lock = TreeLock(node)
    >>> lock.acquire()
    >>> try:
    >>>     # do something on the locked tree
    >>>     node['bar'] = Node()
    >>> finally:
    >>>     lock.release()    
            
``zodict.locking.locktree`` Decorator for methods of a (sub-)class of ``Node``.     
::
       
    >>> from zodict.locking import locktree
    >>> class LockedNode(Node):
    ...
    ...     @locktree
    ...     def __setitem__(self, key, val):
    ...         super(LockedNode, self).__setitem__(key, val)        

Changes
=======

Version 1.9.1
-------------

- Add test for bool evaluation
  [rnix, 2010-04-21]

- Add ``__setattr__`` and ``__getattr__`` to ``NodeAttributes`` object.
  [rnix, 2010-04-21]

- BBB compatibility for zope2.9
  [rnix, jensens, 2010-02-17]

Version 1.9.0
-------------

- Make zodict compatible with python 2.4 again, BBB
  [jensens, 2009-12-23]

- Add locking test
  [rnix, 2009-12-23]

- Refactor locking, remove tree-locking from Node base implementations. 
  Add easy to use locking class and a decorator intended to be used in 
  applications and subclasses of ``Node``.
  [jensens, 2009-12-23]

- Introduce ``ICallableNode``, ``ILeaf`` and ``IRoot`` interfaces.
  [rnix, 2009-12-23]

- Change Lisence to PSF
  [rnix, 2009-12-22]

- Add ``zodict.node.NodeAttributes`` object.
  [rnix, 2009-12-22]

- Add ``attributes`` Attribute to ``LifecycleNode``.
  [rnix, 2009-12-22]

- Add ``ILifecycleNode`` and ``INodeAttributes`` interfaces.
  [rnix, 2009-12-22]

- Removed typo in private variable name. added notify-suppress to setitem of
  ``LifecycleNode``.
  [jensens, 2009-12-22]

Version 1.8.0
-------------

- Added ``zope.lifecycle`` events to the new ``LifecycleNode``. You can 
  easiely override them with your own events. 
  [jensens, 2009-12-21]

- Renamed class ``zodict`` to ``Zodict``, renamed module ``zodict.zodict`` to
  ``zodict._zodict``. This avoids ugly clashes on import (package vs. module 
  vs.class). BBB import is provided in the 1.x release series.
  [jensens, 2009-12-21]

Version 1.7.0
-------------

- Add ``Node.detach`` function. Needed for node or subtree moving. This is
  done due to performance reasons.
  [rnix, 2009-12-18]

- ``Node.index`` returns now a ``NodeIndex`` object, which implements
  ``zope.interface.common.mapping.IReadMapping``. This functions convert uuid 
  instances to integers before node lookup. So we still fit the contract of 
  returning nodes from index by uuid.
  [rnix, 2009-12-18]

- Change type of keys of ``Node._index`` to int. ``uuid.UUID.__hash__``
  function was called too often
  [jensens, rnix, 2009-12-18]

- make ``Node`` thread safe.
  [jensens, rnix, 2009-12-18]

Version 1.6.1
-------------

- make ``Node`` trees merge properly.
  [rnix, 2009-12-15]

- make getter and setter functions of ``uuid`` property private.
  [rnix, 2009-12-15]

Version 1.6.0
-------------

- remove the ``traverser`` module.
  [rnix, 2009-11-28]

- improve ``insertbefore`` and ``insertafter`` a little bit.
  [rnix, 2009-11-28]

- add ``index`` Attribute to ``Node``. Allows access to the internal 
  ``_index`` attribute.
  [rnix, 2009-11-28]
  
- remove ``@accept`` and ``@return`` decorators. Just overhead.
  [rnix, 2009-11-28]

Version 1.5.0
-------------
 
- add ``insertbefore`` and ``insertafter`` function to ``Node``.
  [rnix, 2009-11-27]
  
- fix ``printtree`` if ``Node.__name__`` is ``None``.
  [rnix, 2009-11-20]

- add ``printtree`` debug helper function to ``Node``.
  [rnix, 2009-11-09]

- define own Traverser interface and reduce dependencies.
  [rnix, 2009-10-28]

- removed import of tests from zodicts ``__init__``. this caused import errors
  if ``interlude`` wasnt installed.
  [jensens, 2009-07-16]

Version 1.4.0
-------------

- Don't allow classes as values of a ``Node``. Attribute ``__name__``
  conflicts.
  [jensens, 2009-05-06]

- ``repr(nodeobj)`` now returns the real classname and not fixed
  ``<Node object`` this helps a lot while testing and using classes inheriting
  from ``Node``!
  [jensens, 2009-05-06]

- Make tests run with ``python setup.py test``.
  Removed superflous dependency on ``zope.testing``.
  [jensens, 2009-05-06]

Version 1.3.3
-------------

- Fix ``ITraverser`` interface import including BBB.

Version 1.3.2
-------------

- Add ``root`` property to ``Node``.
  [thet, 2009-04-24]

Version 1.3.1
-------------

- Add ``__delitem__`` function to ``Node``.
  [rnix, 2009-04-16]

Version 1.3
-----------

- Add ``uuid`` Attribute and ``node`` function to ``Node``.
  [rnix, 2009-03-23]

Version 1.2
-----------

- Add ``filtereditems`` function to ``Node``.
  [rnix, 2009-03-22]

Version 1.1
-----------

- Add ``INode`` interface and implementation.
  [rnix, 2009-03-18]

Credits
=======

- Written by Robert Niederreiter <rnix@squarewave.at>
  
- Contributions and ideas by Jens Klein <jens@bluedynamics.com>
