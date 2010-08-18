# Copyright BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

from zope.interface import implements
from zodict import ReverseMapping
# for some reason this won't work
#from zodict.interfaces import IAliaser
from interfaces import IAliaser

class DictAliaser(dict):
    """Uses its own dictionary for aliasing

    ``__getitem__`` -> unalias
    """
    implements(IAliaser)

    def alias(self, key):
        return ReverseMapping(self)[key]
    
    def unalias(self, aliased_key):
        return self[aliased_key]

class PrefixAliaser(object):
    """An aliaser that prefix all keys.

    As it never raise KeyError it is not whitelisting.
    """
    implements(IAliaser)

    def __init__(self, prefix=None):
        self.prefix = prefix

    def alias(self, key):
        return (self.prefix or '') + key

    def unalias(self, prefixed_key):
        """returns the real key for a prefixed_key
        """
        prefix = self.prefix or ''
        if not prefixed_key.startswith(prefix):
            raise KeyError(u"key '%s' does not match prefix '%s'" % \
                    (prefixed_key, prefix))
        return prefixed_key[len(prefix):]

class SuffixAliaser(object):
    """An aliaser that suffixes all keys.

    As it never raise KeyError it is not whitelisting.
    """
    implements(IAliaser)

    def __init__(self, suffix=None):
        self.suffix = suffix

    def alias(self, key):
        return key + (self.suffix or '')

    def unalias(self, suffixed_key):
        """returns the real key for a suffixed_key
        """
        suffix = self.suffix or ''
        if not suffixed_key.endswith(suffix):
            raise KeyError(
                    u"key '%s' does not match suffix '%s'" % \
                            (suffixed_key, suffix)
                    )
        return suffixed_key[:-len(suffix)]

class NodespaceAliases(dict):
    pass
    
