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
from datetime import datetime

# Magic things that just make it work...
committee_link = re.compile("<a href=\"(/representation/minutes/committees/(\d+))\">([A-Za-z0-9\- ]+)</a>")
meeting_link = re.compile("<a href=\"(/representation/minutes/(\d+))\">([A-Za-z0-9 ]+)</a>")
meetings_page_url = "https://www.susu.org/meetings"
susu_root_url = "https://www.susu.org"
meeting_date_str_fmt = re.compile("([A-z][a-z][a-z]) (\d+)[a-z]+ ([A-Za-z]+) (\d+)")

# Calculate some magical dates
now = datetime.now()
academic_year_start = datetime(now.year if now.month >= 9 else now.year-1, 9, 1)
academic_year_end = datetime(now.year if now.month < 9 else now.year+1, 8, 31)

class Committee():
    """
    Committee have meetings, and meetings have minutes. Simple.
    """
    def __init__(self, name, id, url):
        self.url = url
        self.id = id
        self.name = name

    def __str__(self):
        return "%s: %s (%s)" % (self.id, self.name, self.url)

    def __repr__(self):
        return "<Committee Object -- %s>" % (str(self),)

class Meeting():
	"""
	Meetings are things held by committees that should have minutes...
	"""
	def __init__(self, date_str, id, url):
		pass

def fetch_committees():
    """
    This function goes to the SUSU website and pulls the list of committees from the 
    minutes page. It then returns those committees as Committee objects.
    """
    meetings_page = urllib.urlopen(meetings_page_url)

    committees_string = ""
    for line in meetings_page.readlines():
        committees_string += line

    return detect_committees(committees_string)

def detect_committees(committees_string):
    """
    Taking the already downloaded meetings page, this extracts the committees and 
    creates the Committee objects.
    """
    committees = []

    for match in committee_link.findall(committees_string):
        committees.append(Committee(match[2],match[1],match[0]))

    return committees

def fetch_meetings(committee_url):

    meeting_page = urllib.urlopen(susu_root_url + committee_url)
    
    meeting_string = ""
    for line in meeting_page.readlines():
        meeting_string += line

    return detect_meetings(meeting_string)
    
def detect_meetings(meeting_string):
    meetings = []
    
    for match in meeting_link.findall(meeting_string):
        date = convert_susu_meeting_date(match[2])
        if this_year_to_date_p(date):
        	print date
        
def convert_susu_meeting_date(date_str):

	day, date, month, year = meeting_date_str_fmt.match(date_str).groups()
	
	return 	datetime.strptime("%02d %s %s" % (int(date), month, year), "%d %B %Y")

def this_year_to_date_p(date):
	return (date >= academic_year_start) and (date <= now)

def this_year_p(date):
	return (date >= academic_year_start) and (date <= academic_year_end)

def check_minutes_status():
    """
    Identifies which committees are adhering to Union policy regarding minutes.
    """

    committees = fetch_committees()
    
    print "There are %s SUSU committees that we know about." % (len(committees),)

    fetch_meetings(committees[0].url)

if __name__=="__main__":
    check_minutes_status()
