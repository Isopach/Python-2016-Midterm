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

# cookie jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Firefox/12.0')]

r = br.open("http://www.formula1.com/content/fom-website/en/championship/results/2016-race-results/2016-australia-results/race.html")

html = r.read()
soup = bsoup(html)

urlslist = soup.findAll("span", { "class" : "last-name" })
imagelist = soup.findAll("img")
nameslist = soup.findAll("span", { "class" : "last-name" })
pointslist = soup.findAll("td", { "class" : "points" }) 
#open the file to keep the list, as required
fo = open('url.txt', 'w')
logf = open('log.txt', 'w')   
htmlf = open('index.html', 'w')
#index.html
html_top = """
<html>
<head>
    <title>My Home Page: Midterm</title>
</head>

<body>
"""
html_bot = """
</body>
</html>
"""
htmlf.write(html_top)


#Url list
for img in imagelist:
        print "".join(["http://www.formula1.com",img['src']])
        fo.write("".join(["http://www.formula1.com",img['src']])+"\n")

fo.close()

jfile = open('list.json')
jfile_str = jfile.read()
jdata = jfile_str.splitlines()
countj = 0
userj = input("Enter an integer: ")
if (isinstance(userj, int) == True):
    if userj < len(jdata):
        while countj < userj:
            print jdata[countj]
            logf.write(jdata[countj]+"\n")
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
                htmlf.write("<img src='" + savedfile +"'>" + "\n")
                countj += 1

            else:
                os.system('wget64 %s -O %s' % (jdata[countj], jdata[countj].rsplit('/', 1)[-1])) #downloads file; requires installation of wget or wget64 in this case
                htmlf.write("<a href='" + jdata[countj] + "'></a>" + "\n")
                countj += 1 
        
    else:
        print "Please enter an integer smaller than %s" % len(jdata)

#Names and points
for eachname, eachpoint in zip(nameslist, pointslist):
   names=eachname.next
   points = eachpoint.next
   if (str(type(names)) != "<class 'BeautifulSoup.Tag'>"):
      
      print names.string, "\t", points.string
      logf.write(names.string+"\t"+points.string+"\n")
      
jfile.close()
logf.close()
htmlf.write(html_bot)
htmlf.close()