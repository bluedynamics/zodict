# Copyright BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

from odict import odict
from zope.interface import implements
from zope.interface.common.mapping import IEnumerableMapping, IFullMapping
from zodict.interfaces import IAttributeAccess

class Zodict(odict):
    """Mark ordered dict with corresponding interface.
    """
    implements(IFullMapping)
    
    def __init__(self, data=()):
        odict.__init__(self, data=data)

zodict = Zodict
from zope.deprecation import deprecated
deprecated('zodict', "'zodict' has been renamed to 'Zodict'. Please modify your"
                     " code and import to use: 'from zodict import Zodict'")

class ReverseMapping(object):
    """Reversed IEnumerableMapping.
    """
    
    implements(IEnumerableMapping)
    
    def __init__(self, context):
        """Object behaves as adapter for dict like object.
        
        ``context``: a dict like object.
        """
        self.context = context
    
    def __getitem__(self, key):
        """Get a value for a key

        A KeyError is raised if there is no value for the key.
        """
    
    def get(self, key, default=None):
        """Get a value for a key

        The default is returned if there is no value for the key.
        """

    def __contains__(self, key):
        """Tell if a key exists in the mapping."""
    
    def keys(self):
        """Return the keys of the mapping object.
        """

    def __iter__(self):
        """Return an iterator for the keys of the mapping object.
        """

    def values(self):
        """Return the values of the mapping object.
        """

    def items(self):
        """Return the items of the mapping object.
        """

    def __len__(self):
        """Return the number of items.
        """

class AttributeAccess(object):
    """If someone really needs to access the original context (which should not 
    happen), she hast to use ``object.__getattr__(attraccess, 'context')``.
    """
    
    implements(IAttributeAccess)
    
    def __init__(self, context):
        object.__setattr__(self, 'context', context)
    
    def __getattr__(self, name):
        context = object.__getattribute__(self, 'context')
        try:
            return context[name]
        except KeyError:
            raise AttributeError(name)
    
    def __setattr__(self, name, value):
        context = object.__getattribute__(self, 'context')
        try:
            context[name] = value
        except KeyError:
            raise AttributeError(name)
    
    def __getitem__(self, name):
        context = object.__getattribute__(self, 'context')
        return context[name]
    
    def __setitem__(self, name, value):
        context = object.__getattribute__(self, 'context')
        context[name] = value
    
    def __delitem__(self, name):
        context = object.__getattribute__(self, 'context')
        del context[name]