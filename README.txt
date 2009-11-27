zodict
======

Ordered dictionary which implements the corresponding
``zope.interface.common.mapping`` interface.::

  >>> from zope.interface.common.mapping import IFullMapping
  >>> from zodict import zodict
  >>> zod = zodict()
  >>> IFullMapping.providedBy(zod)
  True

Node
====

This is a ``zodict`` which provides a location. Location the zope way means
each item in the node-tree knows its parent and its own name.::

  >>> from zope.location.interface import ILocation
  >>> from zodict.node import Node
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

The ``filtereditems`` function.::

  >>> from zope.interface import Interface
  >>> from zope.interface import alsoProvides
  >>> class IMarker(Interface): pass
  >>> alsoProvides(root['child']['subchild'], IMarker)
  >>> IMarker.providedBy(root['child']['subchild'])
  True

  >>> for item in root['child'].filtereditems(IMarker):
  ...     print item.path
  ['root', 'child', 'subchild']

UUID related operations on Node.::

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

  >>> root.uuid = object()
  Traceback (most recent call last):
    ...
  AssertionError: arg <object object at ...> does not match <class 'uuid.UUID'>

Node insertion (an insertafter function exist as well)::

  >>> root['child1'] = Node()
  >>> root['child2'] = Node()
  
  >>> node = Node('child3')
  >>> root.insertbefore(node, root['child2'])
  >>> root.printtree()
  <class 'zodict.node.Node'>: root
    <class 'zodict.node.Node'>: child1
    <class 'zodict.node.Node'>: child3
    <class 'zodict.node.Node'>: child2

Nodes can not be moved. Therefor you have to read it, delete it from tree and 
add it elsewhere again.:

  >>> node = root['child2']
  >>> del root['child2']
  >>> root.values()
  [<Node object 'child1' at ...>, <Node object 'child3' at ...>]
  
  >>> root.insertbefore(node, root['child1'])
  >>> root.printtree()
  <class 'zodict.node.Node'>: root
      <class 'zodict.node.Node'>: child2
      <class 'zodict.node.Node'>: child1
      <class 'zodict.node.Node'>: child3

Changes
=======

Version 1.5.0 (svn)
-------------
 
  -add ``insertbefore`` and ``insertafter`` function.
   rnix, 2009-11-27
  
  -fix printtree if Node.__name__ is None.
   rnix, 2009-11-20

  -add printtree debug helper function to Node.
   rnix, 2009-11-09

  -define own Traverser interface and reduce dependencies
   rnix, 2009-10-28

  -removed import of tests from zodicts init. this caused import errors if 
   interlude wasnt installed.
   jensens, 2009-07-16

Version 1.4.0
-------------

  -Don't allow classes as values of a Node. Attribute ``__name__`` conflicts.
   jensens, 2009-05-06 

  -repr(nodeobj) now returns the real classname and not fixed ``<Node object``
   this helps a lot while testing and using classes inheriting from Node!
   jensens, 2009-05-06 

  -Make tests run with ``python setup.py test``.
   Removed superflous dependency on ``zope.testing``.
   jensens, 2009-05-06 

Version 1.3.3 (svn)
-------------

  -Fix ITraverser interface import including BBB.

Version 1.3.2
-------------

  -Add ``root`` property to ``Node``.
   thet, 2009-04-24

Version 1.3.1
-------------

  -Add ``__delitem__`` function to ``Node``.
   rnix, 2009-04-16

Version 1.3
-----------

  -Add ``uuid`` Attribute and ``node`` function to ``Node``.
   rnix, 2009-03-23

Version 1.2
-----------

  -Add ``filtereditems`` function to ``Node``.
   rnix, 2009-03-22

Version 1.1
-----------

  -Add ``INode`` interface and implementation.
   rnix, 2009-03-18

Credits
=======

  -Written by Robert Niederreiter <rnix@squarewave.at> (2009-03-17)