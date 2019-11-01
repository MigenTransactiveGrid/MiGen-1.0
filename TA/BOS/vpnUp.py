import requests
import os
import time

def internet(url='http://www.google.com/', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

def mesh(_hostname):
    hostname = _hostname
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False
    return pingstatus

i = 0
for i in range (10):
    if (internet() == True) and (mesh("10.8.0.16")== False):     
        res = os.system('sudo openvpn /home/pi/TA/BOS/bos.ovpn &')
        time.sleep(4)
        if mesh("10.8.0.16")== True:
            break
        i += 1
        time.sleep(10)
        print i
    else:
        print "All is Ok"
        break
