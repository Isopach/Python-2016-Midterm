#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import mechanize
import cookielib
import urllib
import urllib2
import os
from BeautifulSoup import BeautifulSoup as bsoup
import json
from scipy import misc, ndimage
import numpy as np
from PIL import Image
br = mechanize.Browser()

jfile = open('list.json')
jfile_str = jfile.read()
jdata = jfile_str.splitlines()
countj = 0
userj = input("Enter an integer: ")
if (isinstance(userj, int) == True):
    if userj < len(jdata):
        while countj < userj:
            print jdata[countj]
            #if address is jpg
            if jdata[countj].rsplit('/', 1)[-1].endswith('jpg'):
                savedfile = 'rotated_' + jdata[countj].rsplit('/', 1)[-1]
                os.system('wget64 %s -O %s' % (jdata[countj], savedfile))
                #rotating it
                filej = misc.imread('%s'%savedfile)
                lx, ly, lz = filej.shape
                rotate_filej = ndimage.rotate(filej, 90)
                rotate_filej_noreshape = ndimage.rotate(filej, 90, reshape=False)
                imrot = misc.toimage(rotate_filej_noreshape)
                imrot.save('%s'%savedfile)

                countj += 1
                
            #elif jdata[countj].rsplit('/', 1)[-1].endswith('html'):
            else:
                os.system('wget64 %s' % jdata[countj]) #downloads file; requires installation of wget or wget64 in this case
                countj += 1 
               
            #else:
             #   break
        
    else:
        print "Please enter an integer smaller than %s" % len(jdata)
