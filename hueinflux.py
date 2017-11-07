#!/usr/bin/python

#todo FINISH MAIN, still need to figure out how to craft the query
#then need to refactor to accept params
#then need to refactor to perform the post

import requests
import argparse
from os.path import expanduser

def main(host='localhost', port=8086, hueuser):
    """Connect to influxdb and post data"""
    influx_user = 'root'
    influx_password = 'root'
    db_name = 'huedb'
    measurement_name = 'hue_light_status'
    query = 'SELECT light_state_on FROM %s WHERE light_name = ' % (measurement_name)

def get_default_username(dot_hue_path):
    """Check if .hue file exists in users home dir.  Read username from the file if it does"""
    try:
        with open(dot_hue_path, 'r') as f:
            for line in f:
                value = line.split(' ')
                if value[0] == 'username' and len(value[1]) >= 1:
                    return value[1].replace('\n', '')
    except IOError:
        sys.exit("Error: %s could not be read" % dot_hue_path)

    return ''

def get_bridge_ip(hue_nupnp):
    """Get IP of local Hue bridge from Hue's UPNP site"""
    try:
        response = requests.get(hue_nupnp)
        return response.json()[0]['internalipaddress']
    except:
        sys.exit('Could not resolve Hue Bridge IP address. Please ensure your bridge is connected')

def parse_args():
    """Parse some arguments"""
    home = expanduser("~")
    dot_hue_path = home + "/.hue"

    parser = argparse.ArgumentParser(description='Import hue stats to InfluxDB')
    parser.add_argument('--host', type=str, required=False, default='localhost', help='hostname of InfluxDB HTTP API')
    parser.add_argument('--port', type=int, required=False, default=8086, help='port of InfluxDB http API')
    parser.add_argument('--hueuser', default=get_default_username(dot_hue_path), help='Username to use when connecting to Hue bridge')
    return parser.parse_args()

if __name__ == '__main__':
    HUE_NUPNP = 'https://www.meethue.com/api/nupnp'

    args = parse_args()
    if len(args.username) == 0:
        sys.exit("Error: Username must be provided as argument or in %s" % dot_hue_path)

    bridge_ip = get_bridge_ip(HUE_NUPNP)
