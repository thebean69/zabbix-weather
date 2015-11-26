#!/usr/bin/python2
# coding: utf-8
# weather.py
# Grab current weather conditions and load them into Zabbix
# Must run only every 3 min MAX to avoid running into the API limit of 500 free hits per day on weather underground.

import os, sys, urllib2, json, subprocess, ConfigParser
from tempfile import mkstemp

# Find where we are and set where to look for config file based on that.
path = os.path.abspath(os.path.dirname(sys.argv[0]))
config_file = path + '/weather.cfg'
if (os.path.isfile(config_file) == False):
  print "Cannot find config file: {}".format(config_file)
  print "Please create it and try again."
  exit (1)

print "Using config file: {}".format(config_file)
config = ConfigParser.SafeConfigParser({'zabbix_sender': 'zabbix_sender'})

# Read configuration values
try:
  config.read(config_file)
  api_key = config.get('weather', 'api_key')
  location = config.get('weather', 'location')
  zabbix_server = config.get('weather', 'zabbix_server')
  zabbix_hostname = config.get('weather', 'zabbix_hostname')
  zabbix_sender = config.get('weather', 'zabbix_sender')
except ConfigParser.NoOptionError as e:
  print "ERROR: Option '{}' not set in section '{}'".format(e.option, e.section)
  print "Check config file and try again."
  exit (1)

# Check for default config values that haven't been changed
if (api_key == '<API_KEY>'
or zabbix_server == '<ZABBIX_SERVER>'
or zabbix_hostname == '<ZABBIX_HOSTNAME>'):
  print "Default config values found."
  print "Please change them to actual values and try again."
  exit (1)

# Print current config values
print "Read these settings from config file:"
print "api_key: {}".format(api_key)
print "location: {}".format(location)
print "zabbix_server: {}".format(zabbix_server)
print "zabbix_hostname: {}".format(zabbix_hostname)
print "zabbix_sender: {}".format(zabbix_sender)
print "\n"

# Get weather data from weather underground and parse it into variables
f = urllib2.urlopen('http://api.wunderground.com/api/{}/conditions/q/{}.json'.format(api_key, location))
#f = open('/etc/zabbix/scripts/Fort_Collins.json','r')
json_string = f.read()
f.close()
parsed_json = json.loads(json_string)

cw_city = parsed_json['current_observation']['observation_location']['city']
cw_time = parsed_json['current_observation']['observation_time_rfc822']
cw_tempf = parsed_json['current_observation']['temp_f']
cw_tempc = parsed_json['current_observation']['temp_c']
cw_desc = parsed_json['current_observation']['weather']
cw_humid = parsed_json['current_observation']['relative_humidity']
cw_wdir = parsed_json['current_observation']['wind_dir']
cw_wdeg = parsed_json['current_observation']['wind_degrees']
cw_wmph = parsed_json['current_observation']['wind_mph']
cw_wmphg = parsed_json['current_observation']['wind_gust_mph']
cw_pin = parsed_json['current_observation']['pressure_in']
cw_ptrend = parsed_json['current_observation']['pressure_trend']
cw_wcf = parsed_json['current_observation']['windchill_f']
cw_wcf = cw_wcf.replace("NA","0.0")
cw_wcc = parsed_json['current_observation']['windchill_c']
cw_wcc = cw_wcc.replace("NA","0.0")
cw_vism = parsed_json['current_observation']['visibility_mi']
cw_p1in= parsed_json['current_observation']['precip_1hr_in']
cw_pdin = parsed_json['current_observation']['precip_today_in']

# Save temp file of values formatted for zabbix sender with no timestamps
fd, temp_file = mkstemp()
f = open(temp_file, 'w')
f.write("- cw_city %s\n" % (cw_city))
f.write("- cw_time %s\n" % (cw_time))
f.write("- cw_tempf %s\n" % (cw_tempf))
f.write("- cw_tempc %s\n" % (cw_tempc))
f.write("- cw_desc %s\n" % (cw_desc))
f.write("- cw_humid %s\n" % (cw_humid.replace("%","")))
f.write("- cw_wdir %s\n" % (cw_wdir))
f.write("- cw_wdeg %s\n" % (cw_wdeg))
f.write("- cw_wmph %s\n" % (cw_wmph))
f.write("- cw_wmphg %s\n" % (cw_wmphg))
f.write("- cw_pin %s\n" % (cw_pin))
f.write("- cw_ptrend %s\n" % (cw_ptrend))
f.write("- cw_wcf %s\n" % (cw_wcf))
f.write("- cw_wcc %s\n" % (cw_wcc))
f.write("- cw_vism %s\n" % (cw_vism))
f.write("- cw_p1in %s\n" % (cw_p1in))
f.write("- cw_pdin %s\n" % (cw_pdin))
f.close()
os.close(fd)

# Display current conditions in human-readable format
print "Current Conditions:"
print "Observed at: {}".format(cw_time)
print "Location: {}".format(cw_city)
print "Weather: {}".format(cw_desc)
print "Temp: {}°F ({}°C)".format(cw_tempf, cw_tempc)
print "Humidity: {}".format(cw_humid)
print "Pressure: {}in {}".format(cw_pin, cw_ptrend)
print "Visibility: {}mi".format(cw_vism)
print "Precipitation: {}in last hour, {}in today".format(cw_p1in, cw_pdin)
print "Wind: From the {} ({}°) at {}mph, gusting to {}mph".format(cw_wdir, cw_wdeg, cw_wmph, cw_wmphg)
print "Wind Chill: {}°F ({}°C)".format(cw_wcf, cw_wcc)

print "\nSending values to zabbix..."

# Flush stdout buffer to have output print in the correct order.
sys.stdout.flush()

# Call zabbix sender to send values to zabbix
subprocess.call([zabbix_sender, '-z', zabbix_server, '-s', zabbix_hostname, '-i', temp_file])
os.remove(temp_file)
