#!/usr/bin/python2
# coding: utf-8
# weather.py
# Grab current weather conditions and load them into Zabbix
# Must run only every 3 min MAX to avoid running into the API limit of 500 free hits per day on weather underground.

import os, sys, urllib2, json, subprocess
from tempfile import mkstemp

# Set these variables
api_key = 'API_KEY'
zabbix_server = 'ZABBIX_SERVER'
zabbix_hostname = 'ZABBIX_HOSTNAME'


f = urllib2.urlopen('http://api.wunderground.com/api/{}/conditions/q/CO/Fort_Collins.json'.format(api_key))
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

# File is formatted for zabbix trapper values with no timestamps
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
subprocess.call(['zabbix_sender', '-z', zabbix_server, '-s', zabbix_hostname, '-i', temp_file])

os.remove(temp_file)
