"""timestamp tracking function for splunk REST API ViPR Logging App"""

#import datetime module
import datetime
from datetime import timedelta

#get current time for log request stop time
stoptime = datetime.datetime.now()
#increment 1 second for start time of polling cycle after this one to prevent duplicate log entries
futurestarttime = stoptime+datetime.timedelta(0,1)

#reformat time for REST API use
stoptime = stoptime.strftime('%Y-%m-%d_%H-%M-%S')
futurestarttime = futurestarttime.strftime('%Y-%m-%d_%H-%M-%S')

####### Output for testing
##print "\n\nScript begin time = ", stoptime, " : stoptime var \n" #testonly
#######

#open timestamps file for read to get log request start time calculated during last polling cycle
timestamps_file = open("timestamps.txt", "r")

#get new start time to use for this polling cycle
starttime = timestamps_file.readline()
    
#close file
timestamps_file.close()

####### Output for testing
##print "\nValues to use for current polling cycle"
##print "  start time = ", starttime, "starttime var"
##print "  stop time = ", stoptime, "stoptime var"
##print "\nValues to use for next polling cycle"
##print "  future start time = ", futurestarttime, "futurestarttime var"
##print "  future stop time = TBD"
#######
    
#open file for write to store new stop time - for next start time
timestamps_file = open("timestamps.txt", "r+")

#write next polling start time for use in the next polling cycle
timestamps_file.write(futurestarttime)
timestamps_file.close()

####### Output for testing
##print "stored =  ", futurestarttime #(testonly)
##print "start="+starttime+"&end="+stoptime
#######
