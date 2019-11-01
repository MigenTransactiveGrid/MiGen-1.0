# Import Libraries
import os
import glob
import time
 
# Initialize the GPIO Pins
os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module

device_folder = list()
# Finds the correct device file that holds the temperature data
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')
#device_folder.append(glob.glob(base_dir + '10*'))

device_files = list()
for item in device_folder:
  device_files.append(item + '/w1_slave')

# A function that reads the sensors data
def read_temp_raw(device_file):
  f = open(device_file, 'r') # Opens the temperature device file
  lines = f.readlines() # Returns the text
  f.close()
  return lines
 
# Convert the value of the sensor into a temperature
def read_temp(device_file):
  lines = read_temp_raw(device_file) # Read the temperature 'device file'
 
  # While the first line does not contain 'YES', wait for 0.2s
  # and then read the device file again.
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw()
 
  # Look for the position of the '=' in the second line of the
  # device file.
  equals_pos = lines[1].find('t=')
 
  # If the '=' is found, convert the rest of the line after the
  # '=' into degrees Celsius, then degrees Fahrenheit
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    return temp_c, temp_f
 
def run():
  i = 1
  data = list()
  for device_file in device_files:
    data.append(read_temp(device_file))
  if data == []:
    data = [(24.375, 75.875), (24.25, 75.65), (24.25, 75.65)]
  return data

if __name__ == "__main__":
  data = run()
