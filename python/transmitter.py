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

import serial
import pynmea2
import requests
from threading import Thread


gps_value = {
	'timestamp' : '',
	'latitude': 0.0,
	'longitude': 0.0,
	'speed': 0.0,
	'bearing': 0.0
}

def read_gps(device_name):
	global gps_value
	with serial.Serial(device_name) as ser:
		while True:
			line = ser.readline().decode('ascii', errors='replace')
			nmeaobj = pynmea2.parse(line)
			x = ['%s: %s' % (nmeaobj.fields[i][0], nmeaobj.data[i]) for i in range(len(nmeaobj.fields))]
			#print(dir(nmeaobj))
			#print(x)
			#print(nmeaobj.fields)
			#print('new gps value')
			#print(type(nmeaobj.timestamp))
			#print(nmeaobj.timestamp, nmeaobj.latitude, nmeaobj.longitude)
			try:
				gps_value['timestamp'] = nmeaobj.timestamp.strftime("%H:%M:%S.%f")
				gps_value['latitude'] = nmeaobj.latitude
				gps_value['longitude'] = nmeaobj.longitude
				gps_value['speed'] = nmeaobj.speed #nmeaobj.spd_over_grnd
				gps_value['bearing'] = nmeaobj.true_course if nmeaobj.true_course != None else 0.0
			except:
				pass


class transmitter(gr.basic_block):
	def __init__(self, url, device_name, platoon_id):
		gr.basic_block.__init__(self,
			name="transmitter",
			in_sig=[],
			out_sig=[])

		self.device_name = device_name
		self.url = url
		self.platoon_id = platoon_id

		new_thread = Thread(target=read_gps, args=(self.device_name,))
		new_thread.start()


	def communicate(self):
		url = self.url + '/' + str(self.platoon_id) 
		data = {
			  "key": "not_used_now",
			  "lat": gps_value['latitude'],
			  "lon": gps_value['longitude'],
			  "speed": gps_value['speed'],
			  "azim": gps_value['bearing'],
			  "delay": 0.5
		}


		x = requests.post(url, json = data)

		print(x.json())

		return x.json()['freq']
	

