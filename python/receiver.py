#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2022 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

class receiver(gr.basic_block):
    """
    docstring for block receiver
    """
    def __init__(self, url, platoon_id):
        gr.basic_block.__init__(self,
            name="receiver",
            in_sig=[],
            out_sig=[])
    
        self.url = url
        self.platoon_id = platoon_id

    def communicate(self):
        url = self.url + '/' + str(self.platoon_id) 
        x = requests.get(url)
        print(x.json())
        return x.json()['freq']
    

