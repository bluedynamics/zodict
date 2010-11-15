# Copyright BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

try:
    from node.aliasing import (
            DictAliaser,
            PrefixAliaser,
            SuffixAliaser,
            NodespaceAliases,
            AliaserChain,
            PrefixSuffixAliaser,
            NamedAliasers,
            )
except ImportError:
    node = __import__('node.aliasing', {})
    DictAliaser = node.aliasing.DictAliaser
    PrefixAliaser = node.aliasing.PrefixAliaser
    SuffixAliaser = node.aliasing.SuffixAliaser
    NodespaceAliases = node.aliasing.NodespaceAliases
    AliaserChain = node.aliasing.AliaserChain
    PrefixSuffixAliaser = node.aliasing.PrefixSuffixAliaser
    NamedAliasers = node.aliasing.NamedAliasers

# XXX: deprecated message as soon as the new location is stable
#for x in (
#    'DictAliaser',
#    'PrefixAliaser',
#    'SuffixAliaser',
#    'NodespaceAliases',
#    'AliaserChain',
#    'PrefixSuffixAliaser',
#    'NamedAliasers',
#    ):
#    deprecated(
#        x,
#        "Will be removed in 2.0, Use node.aliasing.%s instead." % (x,),
#        )
