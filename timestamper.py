#define token functions for substitution in endpoint URL
#/someurl/foo/$sometoken$/goo -> /someurl/foo/zoo/goo

# functions can return a scalar or a list
# if a scalar is returned , then a single URL request will be made
# if a list is returned , then (n) URL requests will be made , where (n) is the 
# length of the list
# multiple requests will get executed in parallel threads

import datetime

def sometoken():
    return 'zoo'

def sometokenlist():
    return ['goo','foo','zoo']

def datetoday():
    today = datetime.date.today()
    return today.strftime('%Y-%m-%d')

"""timestamp tracking function for splunk REST API ViPR Logging App"""

def logstartstop():
    #import datetime module
    import datetime
    from datetime import timedelta
    
    #get current time for log request stop time
    stoptime = datetime.datetime.now()
    #increment 1 second for start time of polling cycle after this one to prevent duplicate log entries
    futurestarttime = stoptime+datetime.timedelta(0,1)
    
    #reformat time for REST API use
    stoptime = stoptime.strftime('%Y-%m-%d_%H:%M:%S')
    futurestarttime = futurestarttime.strftime('%Y-%m-%d_%H:%M:%S')
    
    #open timestamps file for read to get log request start time calculated during last polling cycle
    timestamps_file = open("/opt/splunk/etc/apps/rest_ta/bin/timestamps.txt", "r")
    
    #get new start time to use for this polling cycle
    starttime = timestamps_file.readline()
    
    #close file
    timestamps_file.close()
    
    #open file for write to store new stop time - for next start time
    timestamps_file = open("/opt/splunk/etc/apps/rest_ta/bin/timestamps.txt", "r+")
    
    #write next polling start time for use in the next polling cycle
    timestamps_file.write(futurestarttime)
    timestamps_file.close()

    #return timestamp text formatted for ViPR Log API Call
    return 'start='+starttime.rstrip()+'&end='+stoptime
