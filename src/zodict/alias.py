# Copyright BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

class NodespaceAliases(dict):
    pass
    
class PrefixAliaser(object):
    """An aliaser that prefix all keys.

    As it never raise KeyError it is not whitelisting.
    """
    def __init__(self, prefix=''):
        self.prefix = prefix

    def __getitem__(self, aliased_key):
        if not aliased_key.startswith(self.prefix):
            raise KeyError(u"key '%s' does not match prefix '%s'" % \
                    (aliased_key, prefix))

    def reverse(self, key):
        return prefix+key
