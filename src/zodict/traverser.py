from zope.interface import implements
from types import StringTypes

from interfaces import INodeTraverser
from interfaces import _RAISE_KEYERROR

class NodeTraverser(object):
    
    implements(INodeTraverser)
    
    def __init__(self, context):
        self.context = context
    
    def traverse(self, path, default=_RAISE_KEYERROR):
        if isinstance(path, StringTypes):
            path = path.split('/')
            if len(path) > 1 and not path[-1]:
                # Remove trailing slash
                path.pop()
        else:
            path = list(path)
        path.reverse()
        curr = self.context
        if not path[-1]:
            # Start at the root
            path.pop()
            curr = self.context.root
            while path:
                name = path.pop()
                try:
                    curr = curr[name]
                except:
                    if default == _RAISE_KEYERROR:
                        raise KeyError, "'"+curr.name + "' has no '" + name + "'"
                    return default
            return curr