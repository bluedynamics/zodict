# Copyright BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

from zope.interface import implements
from zope.interface.common.mapping import IFullMapping
from zodict import ReverseMapping
# for some reason this won't work
#from zodict.interfaces import IAliaser
from interfaces import IAliaser

class DictAliaser(dict):
    """Uses its own dictionary for aliasing

    ``__getitem__`` -> unalias
    """
    implements(IAliaser, IFullMapping)

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
    
class AliaserChain(object):
    """A chain of aliasers

    chain = [aliaser1, aliaser2]
    chain.alias(key) == aliaser2.alias(aliaser1.alias(key))
    chain.unalias(alias_key) == aliaser2.unalias(aliaser1.unalias(aliased_key))
    """
    implements(IAliaser)
    # XXX: we are IEnumerableMapping if one of our childs is, which is
    # important as we become a whitelist, eg. for Node.__iter__

    def __init__(self, chain=None):
        self.chain = chain

    def alias(self, key):
        for aliaser in self.chain:
            key = aliaser.alias(key)
        return key

    def unalias(self, key):
        for aliaser in reversed(self.chain):
            key = aliaser.unalias(key)
        return key

class PrefixSuffixAliaser(AliaserChain):
    """Prefixes and suffixes
    """
    def __init__(self, prefix=None, suffix=None):
        self.chain = (
                PrefixAliaser(prefix),
                SuffixAliaser(suffix),
                )

class NamedAliasers(dict):
    """A dictionary storing aliasers by name
    """
