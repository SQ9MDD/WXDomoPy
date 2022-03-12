#!/usr/bin/env python

json_ip = '10.9.48.3'
solar_flux_idx = 309

import xmltodict
import requests
import urllib



# /json.htm?type=command&param=udevice&idx=IDX&nvalue=0&svalue=VALUE

def set_sfi(sfi = '0'):
    urllib.urlopen('http://' + json_ip + '/json.htm?type=command&param=udevice&idx=' + str(solar_flux_idx)  + '&nvalue=0&svalue=' + str(sfi))


def get_sfi():
    try:
        data_link = 'https://www.hamqsl.com/solarxml.php'
        response = requests.get(data_link)
        obj = xmltodict.parse(response.text)
        return(obj["solar"]["solardata"]["solarflux"])
    except:
        return("")

current_sfi = get_sfi()
set_sfi(current_sfi)
print(current_sfi)
