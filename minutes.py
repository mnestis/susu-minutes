#!/usr/bin/python

"""
SUSU Committee Minute Checker -- Darren Richardson

This collection of scripts was created to help assess whether SUSU (https://susu.org) is
adhering to Union policy 1213P6.

For details of the policy, see:
	https://blogs.susu.org/policy/2013/05/09/the-importance-of-minutes-to-this-students-union/

See LICENSE for copyright information and licensing details.
"""

import urllib, urllib2, re

committee_link = re.compile("<a href=\"(/representation/minutes/committees/(\d+))\">([A-Za-z0-9\- ]+)</a>")

class Committee():
    def __init__(self, name, id, url):
        self.url = url
        self.id = id
        self.name = name

    def __str__(self):
        return "%s: %s (%s)" % (self.id, self.name, self.url)

    def __repr__(self):
        return "<Committee Object -- %s>" % (str(self),)

def fetch_committees():
    meetings_page = urllib.urlopen("https://www.susu.org/meetings")

    committees_string = ""
    for line in meetings_page.readlines():
        committees_string += line

    return detect_committees(committees_string)

def detect_committees(committees_string):
    committees = []

    for match in committee_link.findall(committees_string):
        committees.append(Committee(match[2],match[1],match[0]))

    return committees

def check_minutes_status():
    committees = fetch_committees()
    
    print "There are %s SUSU committees that we know about." % (len(committees),)

    for comm in committees:
        print comm


if __name__=="__main__":
    check_minutes_status()
