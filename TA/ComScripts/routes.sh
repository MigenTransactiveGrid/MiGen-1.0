# Adds the needed static routes as backup for the mesh.
# WIFI_INTERFACE name is wlan0 if PREDICTABLE NAMES are not enabled.
# WIFI_INTERFACE name is wlxMAC if PREDICTABLE NAMES are enabled.
# Creating static routes should be as needed, if noticed inconsistent routing with some parts.
sudo ip route add IP-CA/32 via IP_CA_NEXT_HOP_TOWARD_DESTINATION_CA dev WIFI_INTERFACE_NAME


