#V#iPR-Spelunker Syslog Forwarder for EMC ViPR/CoprHD Logs
import requests, json
from logging.handlers import SysLogHandler
import logging
from timestamper import logstartstop

##User variables - set appropriately for you environment
##See https://www.emc.com/techpubs/vipr/run_rest_api_script_proxy_user-1.htm for help generating the authtoken
authtoken = "BAAcZmlkOTdyZUZHMUIwVEg3SzB0SEZVZTlvK0JBPQMAZwQAG3Byb3h5VG9rZW5TaWduYXR1cmVLZXlFbnRyeQIAAQEFAEJ1cm46c3RvcmFnZW9zOlByb3h5VG9rZW46MTI0MzRlNTctMDViMy00NGIzLThkNTEtZjVhNzNmOGZiM2QwOnZkYzECAALQDw=="
viprvip = "10.4.44.6"
syslogtarget = "10.4.44.241"
syslogport = "514"
writetofile = 0
sendtosyslog = 1

##Generate timestamps for collection - Comment out the following line if the above test lines are in use
startstoptime = logstartstop()
##Set timestamps for Test Purposes - Comment out the following line during normal processing
#startstoptime = "start=2015-09-24_17:28:23&end=2015-09-24_17:33:37"

##Static Variables for processing - do not edit
statelog = "state_tracking.txt"
logfile = "logs_response.txt"
url = "https://"+viprvip+":4443/logs"
header = {'accept': 'application/JSON','X-SDS-AUTH-TOKEN': authtoken}
recovery = 0

##Set up Syslog targets
logger = logging.getLogger()
logger.addHandler(SysLogHandler(address=(syslogtarget, syslogport)))
#logger.addHandler(logging.FileHandler("viprsyslog.log"))

##Send REST-HTTP GET Request to VIPR to retrieve logs
#print "Requesting Logs from ViPR Controller"
#print startstoptime
if recovery = 0:
    logs_response = requests.get(url+'?'+startstoptime, headers=header, verify=False, stream=True)
#elif recovery = 1:
#    f = open(statelog, 'r')
#    logs_response = f.readline()???
#    f.close()

#print "Writing Logs to File"
#print "Forwarding Logs via SysLog"

##Get total number of log entries in ViPR JSON response
#lastlogrecord = 1 #Uncomment this line and comment out the next line for test purposes
if recovery = 0
    lastlogrecord = len(logs_response.json())-1 #comment out this line for test purposes
#elif recovery = 1:
#    g = open(statelog, 'r')
#    lastlogrecord = g.readline()???
#    g.close()
#print lastlogrecord

##Create variable for progress tracking
countdown = lastlogrecord

##open file for saving logs to disk if enabled
if writetofile = 1:
    f = open(logfile, 'w')

##Iterate through all log records received from ViPR and forward
for line in range(0, lastlogrecord):
    #Reformat JSON for easier parsing by syslog host
    badlog = (str(logs_response.json()[line]))
    badlog = badlog.replace("\': u", "=", 9)
    badlog = badlog.replace(", u\'", ", ", 8)
    badlog = badlog.replace("\': ", "=", 2)
    badlog = badlog.replace("{u\'", "{", 1)
    countdown = countdown - 1
    ##Save current progress for this polling cycle in case of failure restart
    g = open(statelog, 'w')
    g.write(str(countdown))
    g.close()
    ##Send log entry to syslog destination
    if sendtosyslog = 1:
        logging.warn(badlog)
    ##Write log entry to local file
    if writetofile = 1:
        f.write(badlog+"\n")

##Close log file at end of polling cycle if logging to file
if writetofile = 1:
    f.close()
