!/usr/bin/env bash
(sudo pkill -9 -f Server.py; sleep 5) &&

cd /
cd /home/pi/TA/Server
sudo python Server.py 8060 &

cd /
cd /home/pi/TA/Server
sudo python Server.py 8070
