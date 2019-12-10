#  

The first part shows the needed steps to setup the communication at the TA side.
## Setting up the LTE connection between the TA and BOS
To setup the LTE connection between the TA and the BOS, the needed scripts and commands shall be executed to enable the Sixfab shield as per the following commands/steps:
1. Clone the repository
```
git clone https://github.com/sixfab/Sixfab_PPP_Installer.git
```

2. Change the permission of the downloaded script and install the script using the following commands:
```
cd Sixfab_PPP_Installer/ppp_installer
chmod +x install.sh
sudo ./install.sh
```
Note: In case of any problems with the ppp-creator.sh, a copy is provided along with the scripts in  Migen1.0/TA/ComScripts.

Afterwards, several questions will be asked to complete the installation process. The answers to the questions are based on the used hardware and are reported inside the square brackets [ ]. Figure 1 and Figure 2 are included for guidance. The questions are:
* Please choose your Sixfab Shield/HAT [select 2]. The required scripts for the selected shield will be fetched.
* What is your carrier APN? [Enter the APN for the service provider]. For Bell Jasper SIM cards, the APN is “APN_NAME”.
* Does your carrier need username and password? [select n] For Bell Jasper SIM cards, there is no need for a username and password.
* What is your device communication PORT? [For 3G, 4G/LTE Base Shield enter “ttyUSB3”]
* Do you want to activate auto-connect/reconnect service at RPi boot up? [select Y] This option allows the connection to the Internet via the shield automatically when the RPI boots up.

Figure 1: sixfab shield software installation steps for RPi – part I
![Picture1](https://user-images.githubusercontent.com/23392778/69773521-19c40c80-1161-11ea-8db6-892506c75eed.png)

Figure 2: sixfab shield software installation steps for RPi – part II
![Picture2](https://user-images.githubusercontent.com/23392778/69773658-67d91000-1161-11ea-8fc7-f1d0b6930c34.png)

The table below summarizes some of the commands that might be needed and the function of each command to establish/disconnect the 4G/LTE communication.
<img width="854" alt="Screen Shot 2019-11-27 at 10 02 10 PM" src="https://user-images.githubusercontent.com/23392778/69773724-9c4ccc00-1161-11ea-9587-95c580893633.png">

## Setting up the Wi-Fi mesh connection
The communication between the TA and CAs uses Wi-Fi Mesh. In this project we based the solution on the HSMM-PI project. Moreover, we added additional scripts and configurations to make the mesh implementation better suits the Migen requirements and the IEEE 2030.5 standard. 

### Step 1: HSMM-PI along with the OLSR
The HSMM-PI is an open source project and could be installed by following the steps below:
1. Download HSMM-PI by running the following commands:
```
sudo apt-get install -y git
git clone https://github.com/ismaelalshiab/hsmm-pi.git
cd hsmm-pi
```
2. Run the install.sh
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
1. From the repository, copy all scripts under Migen1.0/TA/ComScripts to /usr/local/bin:

```
cp NAME_OF_SHELL_SCRIPT /usr/local/bin/
```

2. After installing the mesh on the TA, the routes.sh, checkMesh.sh, and checkDNS.sh shell scripts in /usr/local/bin should be given 775 privilege mode using
```
sudo chmod 775 NAME_OF_SHELL_SCRIPT.
```

### Step 3: Crontab Rules

1. Open the Crontab file by executing this command 

```
crontab -e
```

2. Add the following crontab rules
The following scripts enables the VPN connectivity, add the needed static routes, and continuously check and log the DNS and Mesh reachability. The logging is optional and could be used for monitoring and performance analysis.
```
@reboot sleep 15 && /usr/local/bin/vpnUP.sh
@reboot sleep 15 &&  /usr/local/bin/routes.sh
*/2 * * * * /usr/bin/sudo -H /usr/local/bin/checkDNS.sh
*/5 * * * * /usr/bin/sudo -H /usr/local/bin/checkMesh.sh 
```
	
	
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
