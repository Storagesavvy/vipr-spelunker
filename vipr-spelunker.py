##Master wrapper script that starts, checks status, and executes the poller functions



##Start up and check status
##   if last polling failed, set recovery flag

##Get polling timestamp
##   if delta is large, set catchup mode

##If normal or recovery mode, execute script, pass recovery flag value
##   execute viprlogpoller.py

##If catchup mode, start for loop
##   execute viprlogpoller.py
##  if catchup mode, execute again
