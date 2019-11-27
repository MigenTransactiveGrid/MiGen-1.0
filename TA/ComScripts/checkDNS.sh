#################### #################### ####################
# Shell script that checks Internet connectivity and DSN Resolution.
# Pings one of the known google.com DNS servers.
# If connection is lost, the pppd command is used to re-establish the LTE connection to tower.
# Logging could also be used [optional] for monitoring and performance analysis
#################### #################### ####################
ping -c 4 8.8.8.8
now=$(date  "+%d/%m/%y  %H %M")  

if [ $? != 0 ]
then   
	echo "$now DNS connection lost, running the pppd command"  >> logFilePath/LogFileName
	sudo pppd call gprs persist
else
	echo "$now DNS connection is functional"  >> logFilePath/LogFileName
fi

