# vipr-spelunker
<h4>Syslog forwarder for EMC ViPR and CoprHD</h4>

<h3>Status:</h3>
<b>ViPR-Spelunker</b> has been updated to handle reformatting of the JSON output to make parsing by Splunk and other tools easier. This code also now includes embedded syslog forwarding.  Log messages retreived from ViPR will be sent via Syslog to the destination specified in <b>viprlogpoller.py</b>.

<h3>Plan:</h3>
<p>This project will encompass the following functions:</p>
<p><b>1.)</b> Request a set of ViPR Controller (aka CoprHD) logs between two timestamp value with a RESTful GET request to the ViPR Controller API interface (<b>IMPLEMENTED</b> in viprlogpoller.py)</p>
<p><b>2.)</b> Track the timestamp of the last polling cycle for use during the next polling cycle (<b>IMPLEMENTED</b> in timestamper.py)</p>
<p><b>3.)</b> Receive the JSON log response from ViPR Controller following the request and store it in memory for parsing (<b>IMPLEMENTED</b> in viprlogpoller.py)</p>
<p><b>4.)</b> Reformat the JSON reponse to produce one log line per ViPR log event and remove extreaneous artifact characters in the data (<b>IMPLEMENTED</b> in viprlogpoller.py)</p>
<p><b>5.)</b> Forward each resulting log line via Syslog to a remote syslog server (<b>IMPLEMENTED</b> in viprlogpoller.py)</p>
<p><b>6.)</b> Detect a large backlog - via the difference between the "start" timestamp and current time and request the logs in smaller batches to catch up (<b>TODO</b>)<br />&nbsp<i>The intent with this enhancement is to speed up processing.  The more log entries in memory, the slower the reformatting and forwarding operations operate.   It seems faster to do lots of small batches compared one large batch.</i></p>

<h3>ToDo:</h3>
<p><b>1.)</b> Document the steps for configuration</p>
<p><b>2.)</b> Document the steps needed to properly configure Splunk for the incoming logs</p>
<p><b>3.)</b> Enhance the timestamper.py code to automatically calculate batch groups of 20-30 minutes of logs to speed up backlog processing</p>
<p><b>4.)</b> Enhance the timestamper.py code to be more resilient of a failure during a single batch (ie: prevent missed or duplicate logs if the process fails and is restarted</p>

<h3>Notes:</h3>
<p>The reformatting process is CPU intensive and consists of a series of Python .replace functions that act on each log entry.  As of now .replace seems to be the fastest way I know to perform the reformatting function.  re.sub was orders of magnitude slower.</p>

<h3>Basic Setup:</h3>
<p>Edit the variables in the top section of the <b>viprlogpoller.py</b> to match your environment (<b><i>IP Address of the ViPR Controller VIP, Syslog destination, and AUTH Key</i></b> are the primary settings that need to be configured.</p>

<p>More information on generating/retrieving your AUTH key can be found <a href="https://www.emc.com/techpubs/vipr/run_rest_api_script_proxy_user-1.htm"> at EMC.com</a></p>

