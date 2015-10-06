##Master wrapper script that starts, checks status, and executes the poller functions
def main():
    import time, viprlogpoller
    recovery = 0
    catchup = 0
    interval = 300

##Start up and check status
##   if last polling failed, set recovery flag

##Get polling timestamp
##   if delta is large, set catchup mode

##If normal or recovery mode, execute script, pass recovery flag value
##   execute viprlogpoller.py
    while True:
	print "Polling and Forwarding Logs"
        forwardviprlog(recovery,catchup)
	print "Waiting "+str(interval)+" Seconds"
        time.sleep(interval)

##If catchup mode, start for loop
##   execute viprlogpoller.py
##  if catchup mode, execute again

main()
