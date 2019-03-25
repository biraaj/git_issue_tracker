# GITHUB ISSUE TRACKER

This application enables you to get the total open issues and number of open issues that were opened in the timeframe of:
* 24 hours
* 7 days
* Before 7 days

## USAGE

### Starting the application

In order to run the application set the environment variable below.
```
Windows
set FLASK_APP=run.py

Unix
export FLASK_APP=run.py
```
Run the command below to start the application
```
flask run
```

## DESCRIPTION

* This python application uses flask framework which supports Restful request dispatching and is WSGI compliant.
    * documentation:http://flask.pocoo.org/docs/1.0/
* steps followed to get the response:
    * Request git search api to get issues list.
    * Get the count for different time frames(within 24 hours, 7 days e.t.c) by comparing created_date.
    * Render the results obtained using html page.

## FUTURE IMPROVEMENTS 

* Adding multiple filters to get count according to user's requirement.
* Adding issue list along with the count to get to know about a certain issue.
* As the app is deployed in the heroku cloud we can scale it by increasing number of dynos,
  which means that there will be multiple instances of app running in separate containers.
  This setting will handle multiple traffic by handing over user requests to random dynos.
* Logic can be altered to launch multiple threads to get results from multiple pages similtaneously
  for a single query as git api only gives 100 results per page.
