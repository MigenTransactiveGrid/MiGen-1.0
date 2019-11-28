# CA © 2016–2018 HydroOttawa.
	
>PROPIETARY AND CONFIDENTIAL This document contains proprietary and confidential intellectual property owned by HydroOttawa, as provided for under the Copyright Act of Canada 2012, andl not be disclosed except with written permission from HydroOttawa or University of Ottawa. 
	
	
### before starting anything make sure the time and date is set  
  
```
$ sudo dpkg-reconfigure tzdata
```
## Step  1:
Make sure all the following hardware are connected:

1) Power supply  
2) Metering shield, (you may ignore it for raining trial)  
3) CT, (you may ignore it for raining trial)  
4) Voltage transformer, (you may ignore it for raining trial)  
5) LAN to HEMSC  

## Step  2:

Make sure you have root permission otherwise do:
```
$ sudo su -
```
## Step  3:

Make the CA directory:
```
$ mkdir CA
```
Give the full permission to yourself:
for Tinker:
```
$ chmod -R 077 /home/pi/CA/
```
and make sure you have the following folders and files placed in place:
```
..\CA\DR\...
..\CA\lib\...
..\CA\meter\...
..\CA\requirements.txt
..\CA\great_dr_start.sh

```
## Step 5 
//Disable the DHCP client daemon and switch to standard Debian networking:
```
$ sudo systemctl disable dhcpcd
$ sudo systemctl enable networking
```
## Step 6:
```
$ sudo nano /etc/network/interfaces
```
add the following part in /etc/network/interfaces:
```
$ sudo nano /etc/network/interfaces
```
then 
``
#source-directory /etc/network/interfaces.d

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
``
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
then
```
$ sudo pip install -r requirements.txt
```
## Step  8:
Install scipy for python;
```
$ sudo apt-get install python-scipy
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

## Setting up the connection between the CA and the Wi-Fi mesh network
The Wi-Fi Mesh communication is based on the HSMM-PI project.

### Step 1: HSMM-PI along with the OLSR: The HSMM-PI is an open source project and could be installed by following the steps below:

1. It could be downloaded by running the following commands:
```
sudo apt-get install -y git
git clone https://github.com/ismaelalshiab/hsmm-pi.git
cd hsmm-pi
```
2. Run the following command
```
sh install.sh
```

3. After installing the HSMM-Pi, the network configuration for the Ethernet and Wi-Fi interfaces should be modified according to the figure below using the following command
```
sudo nano /etc/network/interface
```

Figure 3: Updating the network configuration of the Ethernet and Wi-Fi interfaces
![Picture3](https://user-images.githubusercontent.com/23392778/69774089-df5b6f00-1162-11ea-99eb-21173d72f71a.png)

### Step 2: Scripts
1. From the repository, copy all scripts under Migen1.0/CA/ComScripts to /usr/local/bin:

```
cp NAME_OF_SHELL_SCRIPT /usr/local/bin/
```

2. After installing the mesh on the CA, the routes.sh, and checkMesh.sh shell scripts in /usr/local/bin should be given 775 privilege mode using
```
sudo chmod 775 NAME_OF_SHELL_SCRIPT.
```

### Step 3: Crontab Rules

1. Open the Crontab file by executing this command 

```
crontab -e
```

2. Add the following crontab rules

a) Required:
```
@reboot sleep 15 &&  /usr/local/bin/routes.sh
```

b) Optional:
```
*/15 * * * * /usr/bin/sudo -H /usr/local/bin/checkMesh.sh  2>&1
```

