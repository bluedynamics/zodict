# Copyright BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

class NodeTestError(Exception):
    """Raised if a Node test fails unforseen.
    """

class NodeTester(object):
    """Tester object for Nodes.
    """
    
    def __call__(self, node, childred=None):
        """
        ``node``
          the node to test
        ``children``
          odict containing key/val pairs respresenting node children.
        """
        self.node = node
        self.children = children
    
    def run_all(self):
        self.test_IFullMapping()
        self.test_INode()
    
    def test_IFullMapping(self):
        self.test_IExtendedWriteMapping()
        self.test_IItemMapping()
        self.test_IReadMapping()
        self.test_IWriteMapping()
        self.test_IEnumerableMapping()
        self.test_IIterableMapping()
        self.test_IClonableMapping()
    
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
        print "WARNING: NodeTester not implemented this function Yet"
    
    ###########################################################################
    # IReadMapping
    ###########################################################################
    
    def test_get(self, key, default=None):
        print "WARNING: NodeTester not implemented this function Yet"

    def test__contains__(self, key):
        print "WARNING: NodeTester not implemented this function Yet"
    
    ###########################################################################
    # IWriteMapping
    ###########################################################################
    
    def test__delitem__(self, key):
        print "WARNING: NodeTester not implemented this function Yet"

    def test__setitem__(self, key, value):
        print "WARNING: NodeTester not implemented this function Yet"
    
    ###########################################################################
    # IEnumerableMapping
    ###########################################################################
    
    def test_keys(self):
        print "WARNING: NodeTester not implemented this function Yet"

    def test__iter__(self):
        print "WARNING: NodeTester not implemented this function Yet"

    def test_values(self):
        print "WARNING: NodeTester not implemented this function Yet"

    def test_items(self):
        print "WARNING: NodeTester not implemented this function Yet"

    def test__len__(self):
        print "WARNING: NodeTester not implemented this function Yet"
    
    ###########################################################################
    # IIterableMapping
    ###########################################################################
    
    def test_iterkeys(self):
        print "WARNING: NodeTester not implemented this function Yet"

    def test_itervalues(self):
        print "WARNING: NodeTester not implemented this function Yet"

    def test_iteritems(self):
        print "WARNING: NodeTester not implemented this function Yet"
    
    ###########################################################################
    # IClonableMapping
    ###########################################################################
    
    def test_copy(self):
        print "WARNING: NodeTester not implemented this function Yet"
    
    ###########################################################################
    # IExtendedReadMapping
    ###########################################################################
    
    def test_has_key(self, key):
        print "WARNING: NodeTester not implemented this function Yet"
    
    ###########################################################################
    # IExtendedWriteMapping
    ###########################################################################
    
    def test_clear(self):
        try:
            # fill self.node
            for key in self.children:
                self.node[key] = self.children[key]
            # after filling len of self.node must match len of self.children
            if len(self.node) != len(self.children):
                msg = 'ERROR: required __len__ implementation for testing ' + \
                      'clear function malfunction.\n'
                print msg
                return
            # fail if len of self.node is not 0 after clear call.
            self.node.clear()
            if len(self.node) != 0:
                msg = 'ERROR: clear function does not work properly.\n'
                print msg
                return
            print 'SUCCESS:'
            self.node.printtree()
            print ''
        except Exception, e:
            raise NodeTestError(e)
    
    def test_update(self, d):
        try:
            # reset node
            self.node.clear()
            self.node.update(self.children)
            # after updating len of self.node must match len of self.children
            if len(self.node) != len(self.children):
                msg = 'ERROR: required __len__ implementation for testing ' + \
                      'clear function malfunction.\n'
                print msg
                return
            # key of self.node and self.children must be the same.
            nodekeys = self.node.keys()
            nodekeys.sort()
            childkeys = self.children.keys()
            childkeys.sort()
            if nodekeys != childkeys:
                msg = 'ERROR: key compaistion failed in test_update.\n'
                print msg
                return
            print 'SUCCESS:'
            self.node.printtree()
            print ''
        except Exception, e:
            raise NodeTestError(e)
    
    def test_setdefault(self, key, default=None):
        print "WARNING: NodeTester not implemented this function Yet"
    
    def test_pop(self, k, *args):
        print "WARNING: NodeTester not implemented this function Yet"
    
    def test_popitem(self):
        print "WARNING: NodeTester not implemented this function Yet"
    
    ###########################################################################
    # INode
    ###########################################################################
    
    def test_uuid(self):
        print "WARNING: NodeTester not implemented this function Yet"
    
    def test_path(self):
        print "WARNING: NodeTester not implemented this function Yet"
    
    def test_root(self):
        print "WARNING: NodeTester not implemented this function Yet"
    
    def test_index(self):
        print "WARNING: NodeTester not implemented this function Yet"
    
    def test_aliases(self):
        print "WARNING: NodeTester not implemented this function Yet"

    def test_node(self, uuid):
        print "WARNING: NodeTester not implemented this function Yet"

    def test_filtereditems(self, interface):
        print "WARNING: NodeTester not implemented this function Yet"

    def test_insertbefore(self, newnode, refnode):
        print "WARNING: NodeTester not implemented this function Yet"

    def test_insertafter(self, newnode, refnode):
        print "WARNING: NodeTester not implemented this function Yet"

    def test_detach(self, key):
        print "WARNING: NodeTester not implemented this function Yet"

    def test_printtree(self):
        print "WARNING: NodeTester not implemented this function Yet"

node_tester = NodeTester()