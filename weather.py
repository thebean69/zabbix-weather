#!/usr/bin/python2
# coding: utf-8
# weather.py
# Grab current weather conditions and load them into Zabbix
# Must run only every 3 min MAX to avoid running into the API limit of 500 free hits per day on weather underground.

# required libraries
import os, sys, urllib2, json, subprocess

# grab the JSON blob
u = urllib2.urlopen('http://api.wunderground.com/api/<API_KEY>/conditions/q/CO/Fort_Collins.json')
#u = open('/tmp/weather.json', 'r')

#print "DEBUG: Reading JSON.."
json_string = u.read()

#print "DEBUG: Parsing JSON.."
parsed_json = json.loads(json_string)

#print "DEBUG: Extracting values..."
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
cw_wcc = parsed_json['current_observation']['windchill_c']
cw_vism = parsed_json['current_observation']['visibility_mi']
cw_p1in= parsed_json['current_observation']['precip_1hr_in']
cw_pdin = parsed_json['current_observation']['precip_today_in']

# File is formatted for zabbix trapper values
#print "DEBUG: Writing file.."
f = open('/tmp/zbx_weather', 'w')

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
u.close()

print "\n\nCurrent Conditions:"
print "Observed at: %s" % (cw_time)
print "Location: %s" % (cw_city)
print "Weather: %s" % (cw_desc)
print "Temp: %s°F (%s°C)" % (cw_tempf, cw_tempc)
print "Humidity: %s" % (cw_humid)
print "Pressure: %s inHg %s" % (cw_pin, cw_ptrend)
print "Visibility: %s mi" % (cw_vism)
print "Precipitation: %s in last hour, %s in today" % (cw_p1in, cw_pdin)

print "\n\nSending values to zabbix..."
subprocess.call(['zabbix_sender', '-z', '<ZABBIX_SERVER>', '-s', '<ZABBIX_HOST>', '-i', '/tmp/zbx_weather'])

#print "DEBUG: deleting temp file.."
os.remove('/tmp/zbx_weather')

#print "DEBUG: Ending weather script.\n"

