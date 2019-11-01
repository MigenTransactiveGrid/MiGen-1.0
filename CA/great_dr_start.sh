#!/usr/bin/env bash
cd /
cd home/pi/CA/DR
sudo python Handler.py &

cd /
cd home/pi/CA/meter
sudo python CA_HEMSC_meter.py &

cd /
cd home/pi/CA/Server
sudo python Server.py 8060

#cd /
#cd home/pi/CA/meter
#sudo python meter.py
