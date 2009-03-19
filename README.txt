
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

Changes
=======

  -Add node interface and implementation
   rnix, 2009-03-18

Credits
=======

  -Written by Robert Niederreiter <rnix@squarewave.at> (2009-03-17)