import json
import sys
import datetime
import math
import re

from dateutil import parser
from urllib.request import urlopen
import requests
import pytz

#Intiliazing configuration values
CONFIG = json.loads(open("config.json", 'r').read())
API = CONFIG.get('GIT_API')
PAGE_LIMIT = CONFIG.get('PAGE_LIMIT')

#Intilaizing universal time zone.
UTC = pytz.utc

#Method to get the git issue stats. 
def get_issues_stats(url):
    """
    Method steps:
    * Split the given url with '\' to get user/organisation 
        and repository name.
    * Intialize the various time blocks in utc
        (i.e time before 24hr/1day e.t.c)
    * Request git Api for issues data comparing the created date for:-
        issues within 24hr,
        issues between 7 days and 24 hrs before,
        issues before 7 days. 
    """ 

    #Splitting user given url
    url_split = url.split('/')

    #Check if it's a github repository
    if url_split[2] != "github.com" or len(url_split) < 5:
        return {"ERROR":"please enter a valid url"}

    #Extracting user/org name and repository
    user = url_split[3]
    repo = url_split[4].split('.')[0]

    #Intializing and calculating time blocks
    current_time = datetime.datetime.utcnow().replace(tzinfo = UTC)
    one_day_block = current_time - datetime.timedelta(days = 1)
    #removing the decimal parts of second and substituting + with %2b
    one_day_block = re.sub(r'\.[0-9]*\+', '%2b', one_day_block.isoformat())
    seven_days_block = current_time - datetime.timedelta(days = 7)
    seven_days_block = re.sub(r'\.[0-9]*\+', '%2b', seven_days_block.isoformat())

    #Intializing counter variables
    issues_opened_in_24_hours = 0
    issues_opened_in_7_days = 0
    issues_opened_before_7_days = 0
    total_open_issues = 0

    #Parameters for request
    params_in_24_hours = "?q=state:open+type:issue+repo:"+user+'/'+repo+'+created:>='+\
                        one_day_block
    params_in_7_days = "?q=state:open+type:issue+repo:"+user+'/'+repo+'+created:>='+\
                        seven_days_block
    params_before_7_days = "?q=state:open+type:issue+repo:"+user+'/'+repo+'+created:<'+\
                        seven_days_block

    #Requests to get issues Response with different time blocks
    try:
        issue_response_in_24_hours = urlopen(API+str(params_in_24_hours))

        issue_response_in_7_days = urlopen(API+str(params_in_7_days))

        issue_response_before_7_days = urlopen(API+str(params_before_7_days))
    except Exception as e:
        print(e)
        return {"ERROR":"Please Enter a valid User and Repository/Internal error try after sometime"}

    #Check if page is empty.
    if (issue_response_in_24_hours.status == 404) or\
        (issue_response_in_7_days.status == 404) or\
        (issue_response_before_7_days.status == 404):
        return {"ERROR":"Repository/user/org not found"}

    #Extracting issues count from json response 
    issues_opened_in_24_hours = json.loads(issue_response_in_24_hours.read()).get("total_count",0)
    issues_opened_in_7_days = json.loads(issue_response_in_7_days.read()).get("total_count",0) \
                                - issues_opened_in_24_hours
    issues_opened_before_7_days = json.loads(issue_response_before_7_days.read()).get("total_count",0)
    total_open_issues = issues_opened_in_24_hours + issues_opened_in_7_days \
                            + issues_opened_before_7_days

    return {"Issues opened in 24 hours":issues_opened_in_24_hours,
            "Issues opened after 7 days and within 24 hours:":issues_opened_in_7_days,
            "Issues opened before 7 days":issues_opened_before_7_days,
            "Total open issues":total_open_issues}