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
import random
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
logz = open('selected_urls.txt', 'w')   
htmlf = open('index.html', 'w')
#index.html
html_top = """
<html>
<head>
    <title>ホームページ・期末課題</title>
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
jdata = jfile_str.splitlines() #opens as list (R1)
def img_scrapper():
    countj = 0
    userj = input("Enter an integer: ")
    if (isinstance(userj, int) == True):
        try:
            if userj < len(jdata):
                userj = userj
            else:
                userj =  random.randint(1, (len(jdata)-1))
                print "Index exceeded. A random number has been generated for you: %s" % userj
        #Catches error and allows for index to be exceeded via random number generation
        except (TypeError, ValueError, IndexError):
            pass
        while countj < userj:
            print jdata[countj]
            logz.write(jdata[countj]+"\n")
            #if address is jpg (split string based on regex /)
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
            
        
#Takes data from multiple (2) webpages and concentates them within one dict, while merging points from identical racers
url = ("http://www.formula1.com/content/fom-website/en/championship/results/2016-race-results/")
def racers(url):
    racersDict = {}
    payload = ["2016-australia-results/race.html", "2016-bahrain-results/race.html"]
    x = 0
    while (x < len(payload)):
        rx = br.open(url+payload[x])
        htmlx = rx.read()
        soupx = bsoup(html)

        urlslist = soup.findAll("span", { "class" : "last-name" })
        imagelist = soup.findAll("img")
        nameslist = soup.findAll("span", { "class" : "last-name" })
        pointslist = soup.findAll("td", { "class" : "points" }) 
        
        #Names and points
        for eachname, eachpoint in zip(nameslist, pointslist):
           names=eachname.next
           points = eachpoint.next
           if (str(type(names)) != "<class 'BeautifulSoup.Tag'>"):
           #Checks if name is already in dictionary and adds the points if so
              if names.string in racersDict:
                racersDict[names.string] = int(racersDict[names]) + int(points)
              else:
                racersDict[names.string] = points.string
           #print racersDict
           for i in racersDict.iterkeys():
              logf.write(str(i)+"\t"+str(racersDict[i])+"\n")
            
        x += 1
      
jfile.close()
logf.close()
htmlf.write(html_bot)
htmlf.close()

if __name__ == '__main__':
    fo = open('url.txt', 'w')
    logf = open('log.txt', 'w')  
    logz = open('selected_urls.txt', 'w')   
    htmlf = open('index.html', 'w')
    htmlf.write(html_top)
    img_scrapper()
    jfile.close()
    logf.close()
    htmlf.write(html_bot)
    htmlf.close()
    logf = open('log.txt', 'w')
    racers(url)
    logf.close()
    logx = open('log.txt', 'r')
    excess_data = logx.readlines()
    #Deletes duplicate data (extremely hacky - will fix in future)
    del excess_data[0:710]
    del excess_data[22:]
    logx.close()
    logf = open('log.txt', 'w')
    logf.writelines(excess_data)
    logf.close()