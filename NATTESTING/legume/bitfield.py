﻿# -*- coding: utf-8 -*-
#
# bitfield manipulation
#
# By Sebastien Keim
# http://code.activestate.com/recipes/113799/
# Released under the PSF License
#

class bf(object):
    def __init__(self,value=0):
        self._d = value

    def __getitem__(self, index):
        return (self._d >> index) & 1

    def __setitem__(self,index,value):
        value    = (value&1)<<index
        mask     = (1)<<index
        self._d  = (self._d & ~mask) | value

    def __getslice__(self, start, end):
        mask = 2**(end - start) -1
        return (self._d >> start) & mask

    def __setslice__(self, start, end, value):
        mask = 2**(end - start) -1
        value = (value & mask) << start
        mask = mask << start
        self._d = (self._d & ~mask) | value
        return (self._d >> start) & mask

    def __int__(self):
        return self._d

bitfield = bf