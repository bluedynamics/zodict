class NodeTester():
    """Test all known node behaviour
    """
    
    def __call__(self, node, childs=None):
        """
        ``node``
          the node to test
        ``childs``
          odict containing key/val pairs respresenting the child nodespace
        """
        self.nodespaces['childs'] = childs
        # IItemMapping
        self.test__getitem__(key)
        # IReadMapping
        self.test_get(key, default=None)
        self.test__contains__(key)
        # IWriteMapping
        self.test__delitem__(key)
        self.test__setitem__(key, value)
        # IEnumerableMapping
        self.test_keys()
        self.test__iter__()
        self.test_values()
        self.test_items()
        self.test__len__()
        # IIterableMapping
        self.test_iterkeys()
        self.test_itervalues()
        self.test_iteritems()
        # IClonableMapping
        self.test_copy()
        # IExtendedReadMapping
        self.test_has_key(key)
        # IExtendedWriteMapping
        self.test_clear()
        self.test_update(d)
        self.test_setdefault(key, default=None)
        self.test_pop(k, *args)
        self.test_popitem()
        # INode
        self.test_uuid()
        self.test_path()
        self.test_root()
        self.test_index()
        self.test_aliases()
        self.test_node(uuid)
        self.test_filtereditems(interface)
        self.test_insertbefore(newnode, refnode)
        self.test_insertafter(newnode, refnode)
        self.test_detach(key)
        self.test_printtree()
            
    ###########################################################################
    # IItemMapping
    ###########################################################################
    
    def test__getitem__(self, key):
        pass
    
    ###########################################################################
    # IReadMapping
    ###########################################################################
    
    def test_get(self, key, default=None):
        pass

    def test__contains__(self, key):
        pass
    
    ###########################################################################
    # IWriteMapping
    ###########################################################################
    
    def test__delitem__(self, key):
        pass

    def test__setitem__(self, key, value):
        pass
    
    ###########################################################################
    # IEnumerableMapping
    ###########################################################################
    
    def test_keys(self):
        pass

    def test__iter__(self):
        pass

    def test_values(self):
        pass

    def test_items(self):
        pass

    def test__len__(self):
        pass
    
    ###########################################################################
    # IIterableMapping
    ###########################################################################
    
    def test_iterkeys(self):
        pass

    def test_itervalues(self):
        pass

    def test_iteritems(self):
        pass
    
    ###########################################################################
    # IClonableMapping
    ###########################################################################
    
    def test_copy(self):
        pass
    
    ###########################################################################
    # IExtendedReadMapping
    ###########################################################################
    
    def test_has_key(self, key):
        pass
    
    ###########################################################################
    # IExtendedWriteMapping
    ###########################################################################
    
    def test_clear(self):
        pass
    
    def test_update(self, d):
        pass
    
    def test_setdefault(self, key, default=None):
        pass
    
    def test_pop(self, k, *args):
        pass
    
    def test_popitem(self):
        pass
    
    ###########################################################################
    # INode
    ###########################################################################
    
    def test_uuid(self):
        pass
    
    def test_path(self):
        pass
    
    def test_root(self):
        pass
    
    def test_index(self):
        pass
    
    def test_aliases(self):
        pass

    def test_node(self, uuid):
        pass

    def test_filtereditems(self, interface):
        pass

    def test_insertbefore(self, newnode, refnode):
        pass

    def test_insertafter(self, newnode, refnode):
        pass

    def test_detach(self, key):
        pass

    def test_printtree(self):
        pass

node_tester = NodeTester()