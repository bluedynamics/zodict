from node.aliasing import (
    DictAliaser,
    PrefixAliaser,
    SuffixAliaser,
    NodespaceAliases,
    AliaserChain,
    PrefixSuffixAliaser,
    NamedAliasers,
)

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