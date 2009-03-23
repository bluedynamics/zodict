
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

This is a zodict which provides a location.::

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

Changes
=======

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