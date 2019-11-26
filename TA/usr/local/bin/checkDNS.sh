#echo "\n" >> /home/pi/com_per/testDNSSC0.txt
ping -c 4 8.8.8.8 
#>> /home/pi/com_per/testDNSSC0.txt 

if [ $? != 0 ]
then   
	now=$(date  "+%d/%m/%y  %H %M") 
	echo "$now DNS connection lost, running the pppd command"  >> /home/pi/com_per/testDNSSC0.txt
	sudo pppd call gprs persist
#	sleep(4)
#	sudo openvpn /home/pi/TA/BOS/bos.vpn	
	#sudo /sbin/shutdown -r now
	
else
 	now=$(date  "+%d/%m/%y  %H %M") >> /home/pi/com_per/testDNSSC0.txt
 	
	echo "$now DNS connection is functional"  >> /home/pi/com_per/testDNSSC0.txt
fi

