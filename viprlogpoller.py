import requests, json
from logging.handlers import SysLogHandler
import logging

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

print "Requesting Logs from ViPR Controller"
logs_response = requests.get(url+'?'+start+'&'+end, headers=header, verify=False, stream=True)

print "Writing Logs to File"
print "Forwarding Logs via SysLog"

#lastlogrecord = 1
lastlogrecord = len(logs_response.json())-1
#f = open(logfile, 'w')
for line in range(0, lastlogrecord):
    badlog = (str(logs_response.json()[line]))
    badlog = badlog.replace("\': u\'", "=\'")
    badlog = badlog.replace("\': ", "=")
    badlog = badlog.replace(", u\'", " ")
    badlog = badlog.replace("\', u\'", "\' ")
    badlog = badlog.replace("\'}", "\'")
    badlog = badlog.replace("{u\'node", "node")
    logging.warn(badlog)
#    f.write(badlog+"\n")
#f.close()

