#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup as bsoup
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

#Yes i know some of you have probably tried this one:
#r = br.open("http://en.wikipedia.org/wiki/List_of_names_in_Japan")
#It's possible but more challenging/tricky

#This one is easier instead (you are free to decide any website as per the instruction)
r = br.open("http://www.formula1.com/content/fom-website/en/championship/results/2016-race-results/2016-australia-results/race.html")

html = r.read()
soup = bsoup(html)

#Have a look at the manual (which is the point of this exercise)
#http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html#The basic find method: findAll(name, attrs, recursive, text, limit, **kwargs)

#This will find all <td> tags which has no atttribute
nameslist = soup.findAll("span", { "class" : "last-name" })
pointslist = soup.findAll("td", { "class" : "points" }) 

logf = open('log.txt', 'w')

for eachname, eachpoint in zip(nameslist, pointslist):
   names=eachname.next
   points = eachpoint.next
   if (str(type(names)) != "<class 'BeautifulSoup.Tag'>"):
      
      print names.string, "\t", points.string
      logf.write(names.string+"\t"+points.string+"\n")
   
logf.close()

