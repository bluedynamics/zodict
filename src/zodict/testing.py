# Copyright BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

class NodeTester(object):
    """Tester object for Nodes.
    """
    
    def __call__(self, node, childs=None):
        """
        ``node``
          the node to test
        ``childs``
          odict containing key/val pairs respresenting the child nodespace
        """
        self.nodespaces['childs'] = childs
    
    def run_all(self):
        self.test_IFullMapping()
        self.test_INode()
    
    def test_IFullMapping(self):
        self.test_IItemMapping()
        self.test_IReadMapping()
        self.test_IWriteMapping()
        self.test_IEnumerableMapping()
        self.test_IIterableMapping()
        self.test_IClonableMapping()
        self.test_IExtendedReadMapping()
        self.test_IExtendedWriteMapping()
    
    def test_IItemMapping(self):
        key = None
        self.test__getitem__(key)
    
    def test_IReadMapping(self):
        key = None
        self.test_get(key, default=None)
        self.test__contains__(key)
        
    def test_IWriteMapping(self):
        key = None
        value = None
        self.test__delitem__(key)
        self.test__setitem__(key, value)
    
    def test_IEnumerableMapping(self):
        self.test_keys()
        self.test__iter__()
        self.test_values()
        self.test_items()
        self.test__len__()
    
    def test_IIterableMapping(self):
        self.test_iterkeys()
        self.test_itervalues()
        self.test_iteritems()
    
    def test_IClonableMapping(self):
        self.test_copy()
    
    def test_IExtendedReadMapping(self):
        key = None
        self.test_has_key(key)
    
    def test_IExtendedWriteMapping(self):
        self.test_clear()
        d = None
        self.test_update(d)
        key = None
        self.test_setdefault(key, default=None)
        k = None
        args = []
        self.test_pop(k, *args)
        self.test_popitem()
    
    def test_INode(self):
        self.test_uuid()
        self.test_path()
        self.test_root()
        self.test_index()
        self.test_aliases()
        uuid = None
        self.test_node(uuid)
        interface = None
        self.test_filtereditems(interface)
        newnode = None
        refnode = None
        self.test_insertbefore(newnode, refnode)
        self.test_insertafter(newnode, refnode)
        key = None
        self.test_detach(key)
        self.test_printtree()
            
    ###########################################################################
    # IItemMapping
    ###########################################################################
    
    def test__getitem__(self, key):
        raise NotImplementedError(u"Not implemented yet.")
    
    ###########################################################################
    # IReadMapping
    ###########################################################################
    
    def test_get(self, key, default=None):
        raise NotImplementedError(u"Not implemented yet.")

    def test__contains__(self, key):
        raise NotImplementedError(u"Not implemented yet.")
    
    ###########################################################################
    # IWriteMapping
    ###########################################################################
    
    def test__delitem__(self, key):
        raise NotImplementedError(u"Not implemented yet.")

    def test__setitem__(self, key, value):
        raise NotImplementedError(u"Not implemented yet.")
    
    ###########################################################################
    # IEnumerableMapping
    ###########################################################################
    
    def test_keys(self):
        raise NotImplementedError(u"Not implemented yet.")

    def test__iter__(self):
        raise NotImplementedError(u"Not implemented yet.")

    def test_values(self):
        raise NotImplementedError(u"Not implemented yet.")

    def test_items(self):
        raise NotImplementedError(u"Not implemented yet.")

    def test__len__(self):
        raise NotImplementedError(u"Not implemented yet.")
    
    ###########################################################################
    # IIterableMapping
    ###########################################################################
    
    def test_iterkeys(self):
        raise NotImplementedError(u"Not implemented yet.")

    def test_itervalues(self):
        raise NotImplementedError(u"Not implemented yet.")

    def test_iteritems(self):
        raise NotImplementedError(u"Not implemented yet.")
    
    ###########################################################################
    # IClonableMapping
    ###########################################################################
    
    def test_copy(self):
        raise NotImplementedError(u"Not implemented yet.")
    
    ###########################################################################
    # IExtendedReadMapping
    ###########################################################################
    
    def test_has_key(self, key):
        raise NotImplementedError(u"Not implemented yet.")
    
    ###########################################################################
    # IExtendedWriteMapping
    ###########################################################################
    
    def test_clear(self):
        raise NotImplementedError(u"Not implemented yet.")
    
    def test_update(self, d):
        raise NotImplementedError(u"Not implemented yet.")
    
    def test_setdefault(self, key, default=None):
        raise NotImplementedError(u"Not implemented yet.")
    
    def test_pop(self, k, *args):
        raise NotImplementedError(u"Not implemented yet.")
    
    def test_popitem(self):
        raise NotImplementedError(u"Not implemented yet.")
    
    ###########################################################################
    # INode
    ###########################################################################
    
    def test_uuid(self):
        raise NotImplementedError(u"Not implemented yet.")
    
    def test_path(self):
        raise NotImplementedError(u"Not implemented yet.")
    
    def test_root(self):
        raise NotImplementedError(u"Not implemented yet.")
    
    def test_index(self):
        raise NotImplementedError(u"Not implemented yet.")
    
    def test_aliases(self):
        raise NotImplementedError(u"Not implemented yet.")

    def test_node(self, uuid):
        raise NotImplementedError(u"Not implemented yet.")

    def test_filtereditems(self, interface):
        raise NotImplementedError(u"Not implemented yet.")

    def test_insertbefore(self, newnode, refnode):
        raise NotImplementedError(u"Not implemented yet.")

    def test_insertafter(self, newnode, refnode):
        raise NotImplementedError(u"Not implemented yet.")

    def test_detach(self, key):
        raise NotImplementedError(u"Not implemented yet.")

    def test_printtree(self):
        raise NotImplementedError(u"Not implemented yet.")

node_tester = NodeTester()