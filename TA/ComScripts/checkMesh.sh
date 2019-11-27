#################### #################### ####################
# Shell script that checks mesh connectivity by making ping to one of the Ca Homes.
# This is optional script and used for monitoring and troubleshooting.
# If connection is lost, the ifconfig command is used to switch the Wi-Fi mesh interface on.
# The script could be changed to reload the RPi instead of reloading the Wi-Fi interface by removing the comment line 15
# If line 15 is de-commented, 14 should be converted to comment by adding 
# Logging could also be used [optional] for monitoring and performance analysis.
#################### #################### ####################
ping -c 4 IP-CA
now=$(date  "+%d/%m/%y  %H %M") 
if [ $? != 0 ]
then
  echo "$now H_CA_NUMBER is not reachable, turning mesh Wi-Fi interface back on"  >> logFilePath/LogFileName
  sudo ifconfig WIFI_INTERFACE_NAME up
  #sudo /sbin/shutdown -r now
else
	echo "$now H_CA_NUMBER is reachable"  >> logFilePath/LogFileName
fi