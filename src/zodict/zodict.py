# Copyright 2003-2009, BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2 or later

from odict import odict
from zope.interface import implements
from zope.interface.common.mapping import IFullMapping

class zodict(odict):
    """Mark ordered dict with corresponding interface.
    """
    implements(IFullMapping)