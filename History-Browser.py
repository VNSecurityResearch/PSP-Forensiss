#!/usr/bin/env python
#coding:utf-8
"""
  Author:  HieuHT --<>
  Purpose: Extract histories from browser
  Created: 30/03/2016
"""
import struct
from datetime import datetime

with open('historyv.dat') as f:
    data = f.read()

if data:
    histories = data.split('\x03\x00\x01\x00')
    header, histories= histories[0], histories[1:]
    
    for h in histories:
        h = h.split('\x00\x00\x00')
        length_history = struct.unpack('c', h[0])
        length_url = ord(struct.unpack('c', h[2].strip('\x00')[0])[0])
        
        try:            
            page_title_exist = struct.unpack('?', h[1][8:])[0]                
        except:
            page_title_exist = False
            
        if page_title_exist:
            title = ''.join(struct.unpack(length_url *'c', h[3][:length_url]))
            url = h[4][:-9]
        else:
            title = ''.join(struct.unpack(length_url *'c', h[3][:length_url]))
            url = title
            
        try:
            date = struct.unpack('<H', h[4][-9:-7])  # Days elapsed since 01/01/1970 (Little Endian)
            date = date[0] * 24 * 60 * 60                    
            date = datetime.fromtimestamp(date)            
        except:
            date = None
            
        print title
        print url
        print date
        print '---'
            