##ViPR-Spelunker Syslog Forwarder for EMC ViPR/CoprHD Logs

import requests, json, logging, socket, time
from logging.handlers import SysLogHandler
from timestamper import logstartstop

def forwardviprlogs( recovery, catchup ):

##User variables - set appropriately for your environment
##See https://www.emc.com/techpubs/vipr/run_rest_api_script_proxy_user-1.htm for help generating the authtoken
    authtoken = "BAAcZmlkOTdyZUZHMUIwVEg3SzB0SEZVZTlvK0JBPQMAZwQAG3Byb3h5VG9rZW5TaWduYXR1cmVLZXlFbnRyeQIAAQEFAEJ1cm46c3RvcmFnZW9zOlByb3h5VG9rZW46MTI0MzRlNTctMDViMy00NGIzLThkNTEtZjVhNzNmOGZiM2QwOnZkYzECAALQDw=="
    viprvip = "10.4.44.6"
    syslogtarget = "10.4.44.241"
    syslogport = 514
    writetofile = 0
    sendtosyslog = 1
    testmode = 0

##Generate timestamps for collection
    if testmode == 0:
	startstoptime = logstartstop()
##Set timestamps for Test Purposes
    if testmode == 1:
	startstoptime = "start=2015-09-24_17:28:23&end=2015-09-24_17:33:37"

##Static Variables for processing - do not edit
    statelog = "state_tracking.txt"
    logfile = "logs_response.txt"
    restqueue = "rest_response.txt"
    url = "https://"+viprvip+":4443/logs"
    header = {'accept': 'application/JSON','X-SDS-AUTH-TOKEN': authtoken}

##Set up Syslog targets
    logger = logging.getLogger()
    logger.addHandler(SysLogHandler(address=(syslogtarget, syslogport)))
    #logger.addHandler(logging.FileHandler("viprsyslog.log"))

##Send REST-HTTP GET Request to VIPR to retrieve logs
    print "Requesting Logs from ViPR Controller"
    print "Startstoptime "+str(startstoptime)
    requeuelinetemp = False
    if recovery == 0:
        r = open(restqueue, 'w')
        logs_response = requests.get(url+'?'+startstoptime, headers=header, verify=False, stream=True)
        lastlogrecord = len(logs_response.json())-1
        for lineone in range(0, lastlogrecord):
            restqueuelinetemp = (str(logs_response.json()[lineone]))
            r.write(restqueuelinetemp+'\n')
        r.close()

#elif recovery = 1:
#    f = open(statelog, 'r')
#    logs_response = f.readline()???
#    f.close()

##Get total number of log entries in ViPR JSON response
    if testmode == 1:
        lastlogrecord = 1
    if recovery == 0:
        lastlogrecord = len(logs_response.json())-1
        print "lastlogrecord "+str(lastlogrecord)

#Clear JSON from memory and operate from disk
    logs_response = False

#elif recovery = 1:
#    g = open(statelog, 'r')
#    lastlogrecord = g.readline()???
#    g.close()
#print lastlogrecord

##Create variable for progress tracking
    countdown = lastlogrecord

##open file for saving logs to disk if enabled
    if writetofile == 1:
        f = open(logfile, 'w')

##Iterate through all log records received from ViPR and forward
    print "Formatting and Forwarding Logs"
    with open(restqueue, "r") as file:
        for line in file:
            line = line.rstrip("\n")
            line = line.replace("\': u", "=", 9)
            line = line.replace(", u\'", ", ", 8)
            line = line.replace("\': ", "=", 2)
            line = line.replace("{u\'", "{", 1)
            countdown = countdown - 1
            ##Save current progress for this polling cycle in case of failure restart
            g = open(statelog, 'w')
            g.write(str(countdown))
            g.close()
            ##Send log entry to syslog destination
            if sendtosyslog == 1:
                logging.warn(line)
            ##Write log entry to local file
            if writetofile == 1:
                f.write(line+"\n")

##Close log file at end of polling cycle if logging to file
    r.close()
    if writetofile == 1:
        f.close()

def main():
    recovery = 0
    catchup = 0
    interval = 300
    while True:
        print "Polling and Forwarding Logs"
        forwardviprlogs( recovery, catchup )
        print "Waiting "+str(interval)+" Seconds"
        time.sleep(interval)

main()
