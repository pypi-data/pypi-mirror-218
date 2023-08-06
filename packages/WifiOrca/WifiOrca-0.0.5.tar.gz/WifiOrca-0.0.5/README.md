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
# 
# client usage:
# import WifiOrca.main
# make sure to have the server.txt file present in the same directory as WifiOrca for the reverse_shell_client.py script to work
# 
# client start at boot
# On linux in a terminal:
# crontab -e
# then add the following to the file:
# @reboot /usr/bin/python3 path/to/WifiOrca/main.py
# 
# server:
# import WifiOrca.reverse_shell_server
