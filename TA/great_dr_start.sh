#!/usr/bin/env bash
cd /
cd /home/pi/TA/BOS
sudo python Handler.py &
cd /
cd home/pi/TA/DR/
sudo python Main.py &
cd /
cd /home/pi/TA/meter
sudo python run.py &
cd /
cd /home/pi/TA/HealthMonitoring
sudo python run.py
