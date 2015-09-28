import requests, json
from logging.handlers import SysLogHandler
import logging
from timestamper import logstartstop
#import re

logger = logging.getLogger()
logger.addHandler(SysLogHandler(address=('10.4.44.241', 514)))
#logger.addHandler(logging.FileHandler("viprsyslog.log"))
authtoken = "BAAcZmlkOTdyZUZHMUIwVEg3SzB0SEZVZTlvK0JBPQMAZwQAG3Byb3h5VG9rZW5TaWduYXR1cmVLZXlFbnRyeQIAAQEFAEJ1cm46c3RvcmFnZW9zOlByb3h5VG9rZW46MTI0MzRlNTctMDViMy00NGIzLThkNTEtZjVhNzNmOGZiM2QwOnZkYzECAALQDw=="
start = "start"+"="+"2015-09-24_17:28:23"
end = "end"+"="+"2015-09-24_17:33:37"
#certverify = 'False'
header = {'accept': 'application/JSON','X-SDS-AUTH-TOKEN': authtoken}
viprvip = "10.4.44.6"
url = "https://"+viprvip+":4443/logs"
logfile = "logs_response.txt"
startstoptime = logstartstop()

print "Requesting Logs from ViPR Controller"
print startstoptime
#logs_response = requests.get(url+'?'+start+'&'+end, headers=header, verify=False, stream=True)
logs_response = requests.get(url+'?'+startstoptime, headers=header, verify=False, stream=True)

print "Writing Logs to File"
print "Forwarding Logs via SysLog"

#lastlogrecord = 1
lastlogrecord = len(logs_response.json())-1
print lastlogrecord
countdown = lastlogrecord
#f = open(logfile, 'w')
for line in range(0, lastlogrecord):
    badlog = (str(logs_response.json()[line]))
#    print badlog+"\n"
#    badlog = re.sub ("\{\u\'|}|,[\s]\u\'", " ", badlog) 
#    print badlog+"\n"
#    badlog = re.sub ("\':\s\u", "=", badlog)
#    print badlog+"\n"
    badlog = badlog.replace("\': u", "=", 9)
#    print badlog+"\n"
    badlog = badlog.replace(", u\'", ", ", 8)
#    print badlog+"\n"
    badlog = badlog.replace("\': ", "=", 2)
#    print badlog+"\n"
    badlog = badlog.replace("{u\'", "{", 1)
#    print badlog+"\n"
    print "sent "+str(countdown)
    countdown = countdown - 1
    logging.warn(badlog)
#    f.write(badlog+"\n")
#f.close()

