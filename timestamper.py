#import datetime module
import datetime
from datetime import timedelta

"""timestamp tracking function for splunk REST API ViPR Logging App"""

def logstartstop():
    #get current time for log request stop time
    stoptime = datetime.datetime.now()
    
    #increment 1 second for start time of polling cycle after this one to prevent duplicate log entries - OLD
    futurestarttime = stoptime
    #decrement 1 minute for stop time of this polling cycle
    stoptime = stoptime-datetime.timedelta(0,60)
    
    #reformat time for REST API use - NEW
    #set seconds to 0 to align timestamps between polling cycles
    stoptime = stoptime.strftime('%Y-%m-%d_%H:%M:00')
    futurestarttime = futurestarttime.strftime('%Y-%m-%d_%H:%M:00')
    
    #open timestamps file for read to get log request start time calculated during last polling cycle
    timestamps_file = open("timestamps.txt", "r")
    
    #get new start time to use for this polling cycle
    starttime = timestamps_file.readline()
    
    #close file
    timestamps_file.close()
    
    #open file for write to store new stop time - for next start time
    timestamps_file = open("timestamps.txt", "r+")
    
    #write next polling start time for use in the next polling cycle
    timestamps_file.write(futurestarttime)
    timestamps_file.close()

    #return timestamp text formatted for ViPR Log API Call
    return 'start='+starttime.rstrip()+'&end='+stoptime
