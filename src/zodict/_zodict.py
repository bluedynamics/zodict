# Copyright 2009, BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

from odict import odict
from zope.interface import implements
from zope.interface.common.mapping import IFullMapping

class Zodict(odict):
    """Mark ordered dict with corresponding interface.
    """
    implements(IFullMapping)
    
    def __init__(self, data=()):
        odict.__init__(self, data=data)
        
# BBB 
zodict = Zodict 
from zope.deprecation import deprecated
deprecated('zodict', "'zodict' has been renamed to 'Zodict'. Please modify your"
                     " code and import to use: 'from zodict import Zodict'")