# Wifi Orca contains free and open source tools similar to hak5!
# 
# requirements:
# * iw (linux package)
# * linux
# * monitor mode
# * nmap (linux package)
# * sqlmap
# * TheSilent
# 
# client usage:
# import WifiOrca.main
# make sure to have the server.txt file present in the same directory as WifiOrca for the reverse_shell_client.py script to work
# make sure to have the mode.txt file present in the same directory as WifiOrca for the reverse_shell_client.py script to work
# make sure to have the ports.txt file present in the same directory as WifiOrca for the reverse_shell_client.py script to work
# 
# reverse shell client start at boot:
# On linux in a terminal:
# crontab -e
# then add the following to the file:
# @reboot /usr/bin/python3 path/to/WifiOrca/main.py
# 
# reverse shell server:
# import WifiOrca.reverse_shell_server
# 
# reverse shell modes:
# 0 | off | ip_sniff
# 1 | internal to internal | ip_sniff
# 2 | internal to external but not internal to internal | ip_sniff
# 3 | all | ip_sniff
# 
# reverse shell ports:
# ports must be separated by new lines
# only one port per line
# use "all" if you don't care what ports are recorded
# 
# reverse shell recommended ports for red team assessments:
# 20,21,23,25,53,67,68,80- clear text
# 1194,1725,9050,19132,19133- potential policy violation
