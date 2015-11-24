zabbix-weather
==============


A script and zabbix template to track weather data pulled from weather underground


Prerequisites
-------------

* An account for API access on weatherunderground.com
* Admin access for at least one host on a Zabbix server (works with Zabbix versions 2.2 and 2.4)
* shell access to the host
* python 2 installed and working on the host machine (tested with Python 2.7)

This has been tested with linux hosts only. The python should be portable enough to run in windows, but the file     paths have to be changed.  The file used is only a temporary file, so it should not matter where it is saved as long  as the user running the script has write access to the directory in which the file resides.


First Time Setup
----------------

* Sign up for API access at weather underground (500 API calls per day are free) at http://www.wunderground.com/weather/api
* Take note of your API key.


Installing
----------

Installation must be done manually, as this is only the initial version.

0. Place the weather.py on a host of your choice where the zabbix agent can execute it
The default location is `/etc/zabbix/scripts`

0. Make it executable `chmod +x /etc/zabbix/scripts/weather.py`

0. Open the script in an editor and change the following items:

```
# Set these variables
api_key = 'API_KEY'
zabbix_server = 'ZABBIX_SERVER'
zabbix_hostname = 'ZABBIX_HOST'

API_KEY        Replace with your actual weather underground API key
ZABBIX_SERVER  Hostname or IP of your zabbix server
ZABBIX_HOST    Zabbix Host name of the host with the weather script installed
```

0. Python2 is required and is expected to be installed at `/usr/bin/python2`. Modify the first line of the script if  your python2 is named just python or resides in a different path.

0. If desired, the location can be changed. It is set up to query weather from Fort Collins, CO
To change, replace the `/CO/Fort_Collins.json` in the URL with the URL for your city.
The name must be one that the weather underground supports.

0. Run the script from the command line to ensure that it works properly.  An example of a successful run is below
```
Current Conditions:
Observed at: Mon, 23 Nov 2015 15:40:12 -0700
Location: Hanna Farm, Fort Collins
Weather: Clear
Temp: 56.5°F (13.6°C)
Humidity: 28%
Pressure: 29.96in +
Visibility: 10.0 mi
Precipitation: 0.00in last hour, 0.00in today
Wind: From the WSW (247°) at 2.2mph, gusting to 6.3mph
Wind Chill: 0.0°F (0.0°C)

Sending values to zabbix...
info from server: "processed: 17; failed: 0; total: 17; seconds spent: 0.000182"
sent: 17; skipped: 0; total: 17
```

0. Import the weather template into Zabbix `Configuration -> Templates -> Import`. This template only includes Applications, Items, Triggers and Graphs

0. Add a host to be in the template.  This should be the same host as the script is installed.

0. Look at the host's latest data.  It should be populated with weather data in a few minutes.

Any errors from the script will be in the latest data of the "Collect Weather Data" item.

