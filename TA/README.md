# TA © 2016–2018 HydroOttawa.
	
>PROPIETARY AND CONFIDENTIAL This document contains proprietary and confidential intellectual property owned by HydroOttawa, as provided for under the Copyright Act of Canada 2012, andl not be disclosed except with written permission from HydroOttawa or University of Ottawa. 
	
	
### before starting anything make sure the time and date is set  
  
```
$ sudo dpkg-reconfigure tzdata
```
## Step  1:
Make sure all the following hardware are connected:

1) Power supply  
2) Measurlogic Metering,
3) CT, 
4) Voltage transformer,
5) LTE module 

## Step  2:

Make sure you have a root permission otherwise do:
```
$ sudo su -
```
## Step  3:

Make the TA directory:
```
$ mkdir TA
```
Give the full permission to yourself:
```
$ chmod -R 077 /home/pi/CA/
```
and make sure you have the following folders and files placed in place:
```
..\TA\DR\...
..\TA\lib\...
..\TA\meter\...
..\TA\HealthMonitoring\...
..\TA\database\...
..\TA\Predictor\...
..\TA\Reward\...
..\TA\Server\...
..\TA\requirements.txt
..\TA\great_dr_start.sh

```
## Step 5 
Disable the DHCP client daemon and switch to standard Debian networking:
```
$ sudo systemctl disable dhcpcd
$ sudo systemctl enable networking
```
## Step 6:
add the following part in /etc/network/interfaces:  
Note: This part will be change according to Wi-Fi meshed netwrok settings:
```
$ sudo nano /etc/network/interfaces
```
then   
```
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
        address 10.7.7.1
        netmask 255.0.0.0
        gateway 10.255.255.255

auto wlan0
iface wlan0 inet static
        address 10.156.7.120-254
        netmask 255.0.0.0
		wireless-mod ad-hoc
		wireless-channel 1
        wireless-essid AREDN-20-v3

iface default inet dhcp
```
## Step  7:
Install python requirements:
```
$ sudo apt-get install build-essential libffi-dev python-dev
$ sudo apt-get install python-setuptools
```
or 
```
$ sudo apt-get install python-pip
$ sudo pip install --upgrade setuptools
```

## Step  8:
Install scipy, numpy ans Cython for python;
```
$ sudo apt-get install python-scipy
```
```
$ sudo apt-get install python-numpy
```
```
$ sudo apt-get install python-Cython
```
then
```
$ sudo pip install -r requirements.txt
```
## Step  9: 
Install python GPIO library:
```
$ sudo apt-get install python-dev
$ wget wget https://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.5.11.tar.gz
```
unzip it with
```
$ tar -xvf RPi.GPIO-0.5.11.tar.gz
```
go to the folder 
```
$ cd RPi.GPIO-0.5.11
```
and install
```
$ sudo python setup.py install
```
## Step  10:

check w1-gpio.dtbo is loaded if not do:
```
$ sudo nano /boot/config.txt
```
Look to see whether there is a line that has dtoverlay=w1-gpio in it.  If not, add the following to the end of the file:
```
dtoverlay=w1-gpio
```
## Step  11:
Update and upgrade the tinker:
```
$ sudo apt-get update
$ sudo apt-get upgrade
```
## Step  12: 
Enable spi by:
```
$ sudo nano /boot/config.txt
```
and making spi2=on in;
```
dtparam=spi=on
```
see if spi is enabled by:
```
sudo cat /dev/spidev*
```
and you see /dev/spidev0.0 in the list.

## Step  13:
Reboot the system:
```
$ sudo reboot
```
## Step  14: 
Open a terminal (use root) do;
```
sudo apt-get update
sudo apt-get upgrade
```
and install requirement for wi-fi meshed network TBD

## Step  15:
Reboot the system:
```
$ sudo reboot
```
## Step  16:
If all above steps get passed the you should be able to execute all firmwares via shell script, which is automatically is running all needed firmware  
Open a terminal session and edit the file
```
$ sudo nano /etc/profile
```
Add the following line to the end of the file
```
/home/pi/CA/great_dr_start.sh
```
Save and Exit by pressing Ctrl+X to exit nano editor followed by Y to save the file. you may wish to test your shell file but first make sure you set all above lines carefully otherwise DO NOT:
```
$ sed -i 's/\r$//' great_dr_start.sh
```

## to set the LTE communication on the TA sids, the follwoing steps should be followed:
## Step 1:
Get a copy o the ppp-creator.sh needed to configure and connect the installed sixfab shield. A copy has already been provided in /TA/ComScripts. Then use the following commands to give the needed permissions and install the needed parts.
```
$ chmod +x install.sh
sudo ./install.sh
```
## Step 2:
During the ppp-creator installation, it asks several questions to complete the installation process. The answers to the questions based on the used hardware are reported inside the square brackets [ ]. In addition, The following figure 2 and Figure 3 are included for guidance. The questions/selections as follwoing :
●       Please choose your Sixfab Shield/HAT [select 2]. The required scripts for the selected shield will be fetched.
●       What is your carrier APN? [Enter the APN for the service provider]. For Bell Jasper SIM cards, the APN is “APN-NAME”.
●       Does your carrier need username and password? [select n] For Bell Jasper SIM cards, there is no need for username and password.
●       What is your device communication PORT? [For 3G, 4G/LTE Base Shield enter “ttyUSB3”]
●       Do you want to activate auto-connect/reconnect service at RPi boot up? [select Y] allows the connection to the Internet automatically when the RPI boot up.

