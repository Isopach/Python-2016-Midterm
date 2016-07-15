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
url = ("http://www.formula1.com/content/fom-website/en/championship/results/2016-race-results/")

 

def racers(url):
    payload = ["2016-australia-results/race.html", "2016-bahrain-results/race.html"]
    x = 0
    while (x < len(payload)):
        r = br.open(url+payload[x])
        html = r.read()
        soup = bsoup(html)

        urlslist = soup.findAll("span", { "class" : "last-name" })
        imagelist = soup.findAll("img")
        nameslist = soup.findAll("span", { "class" : "last-name" })
        pointslist = soup.findAll("td", { "class" : "points" }) 
        #open the file to keep the list, as required
        logf = open('log.txt', 'w')
        #Names and points
        for eachname, eachpoint in zip(nameslist, pointslist):
           names=eachname.next
           points = eachpoint.next
           if (str(type(names)) != "<class 'BeautifulSoup.Tag'>"):
              
              print names.string, "\t", points.string
              logf.write(names.string+"\t"+points.string+"\n")
        x += 1
              
logf.close()

if __name__ == '__main__':
    racers(url)