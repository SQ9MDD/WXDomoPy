#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# DOMOTICZ to APRX PYTHON script
# SQ9MDD@2020 released under GPL.v.2
# http://sq9mdd.qrz.pl

# weather frame with position without time structure
# ramka pogodowa z pozycja bez czasu

#   !               - required      identifier
#   5215.01N        - required      latitude
#   /               - required      symbol table
#   02055.58E       - required      longtitude
#   _               - required      icon (must be WX)
#   ...             - required      wind direction (from 0-360) if no data set: "..."
#   /               - required      separator
#   ...             - required      wind speed (average last 1 minute) if no data set: "..."
#   g...            - required      wind gust (max from last 5 mins) if no data set: "g..."
#   t030            - required      temperature in fahrenheit
#   r000            - option        rain xxx
#   p000            - option        rain xxx
#   P000            - option        rain xxx
#   h00             - option        relative humidity (00 means 100%Rh)
#   b10218          - option        atmosferic pressure in hPa multiple 10
#   Fxxxx           - option        water level above or below flood stage see: http://aprs.org/aprs12/weather-new.txt
#   V138            - option        battery volts in tenths   128 would mean 12.8 volts
#   Xxxx            - option        radiation lvl
#
# temp z sieci APRSjest w fahrenheit przeliczanie na C =(F-32)/9*5
# temp w celsjusz do sieci APRS trzeba wyslac jako fahrenheit F = (C*9/5)+32
#
# WX possible icon:
# /_    - weather station wx blue
# /W    - national weather service
# /w    - water weather station
# \_    - weather station with digi green
# \W    - national weather services
#
################################### CONFIGURATION ###############################################
#                                                                                               #
wx_lat      	        = '5215.01N'                     	# coordinates APRS format           #
wx_lon      	        = '02055.58E'                    	# coordinates APRS format           #
wx_icon_table           = '/'                               # / - primary \ - secondary         #
wx_icon_symbol          = '_'                                                                   #
wx_comment  	        = 'WXDomoPy'      	                # beacon comment		            #
wx_err_comment 	        = 'No WX data'				        # comment when no data avaiable	    #
json_ip                 = '10.9.48.3'                       # domoticz IP adress                #
# required                                                                                      #
json_wind_direction_idx = '213'                             # wind direction sensor IDX         #
json_wind_speed_idx     = '213'                             # wind speed sensor IDX             #
json_wind_gust_idx      = '213'                             # wind speed gust IDX               #
json_temp_idx           = '211'                             # Temp sensor IDX                   #
# optionally                                                                                    #
json_rain_1h_idx        = '0'                                                                   #
json_rain_24h_idx       = '0'                                                                   #
json_rain_midnight_idx  = '0'                                                                   #
json_humi_idx           = '211'                             # Humidity sensor IDX               #
json_baro_idx           = '211'                             # Baromether  IDX                   #
# additional                                                                                    #
json_tempi_idx          = '0'                               # inside temperature                #
json_pm_1_idx           = '0'                               # PM 1.0 sensor IDX                 #
json_pm_25_idx          = '140'                             # PM 2.5 sensor IDX                 #
json_pm_10_idx          = '141'                             # PM 10 sensor IDX                  #
json_general_pm_idx     = '0'                               # General PM sensor                 #
json_voltage_batt_idx   = '0'                               # Battery voltage in comment        #
json_voltage_batti_idx  = '98'                              # Battery voltage in frame          #
# extra addons                                                                                  #
json_thunder_dist_idx    = '0'                              # lightning detector distance       #
json_thunder_enrg_idx    = '0'                              # lightning detector energy         #
# comments                                                                                      #
#                                                                                               #
# Solar Flux addon                                                                              #
json_solar_flux_idx      = '309'                             # enabled, disabled SFI             #										      	                                                #
######################## DO NOTE EDIT BELLOW THIS LINE ##########################################

import json
import urllib, json
import requests
url = 'http://' + json_ip + '/json.htm?type=devices&rid='
data_elements_first = False
data_elements_count = 0
storm_warning = False

################################### FUNCTION ARE HERE ###########################################

# Solar Flux Index
def get_sfi():
    if(int(json_solar_flux_idx) == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_solar_flux_idx)
            data = json.loads(response.read())
            sfi = data["result"][0]["Data"]
            sfi = sfi.replace(" SFI","")
            return('SFI:' + str(sfi) + ' ')
        except:
            return('')

# wind direction
def wind_direction():
    if(int(json_wind_direction_idx) == 0):
        return('...')
    else:
        try:
            response = urllib.urlopen(url+json_wind_direction_idx)
            data = json.loads(response.read())
            wind_dir = int(data["result"][0]["Direction"])
            if(wind_dir < 10):
                wind_str = '00' + str(wind_dir)
            elif(wind_dir > 9 and wind_dir < 100):
                wind_str = '0' + str(wind_dir)
            else:
                wind_str = str(wind_dir)
            return str(wind_str)
        except:
            return('...')

# wind speed 
def wind_speed():
    if(int(json_wind_speed_idx) == 0):
        return('...')
    else:
        try:
            response = urllib.urlopen(url+json_wind_speed_idx)
            data = json.loads(response.read())
            wind_mph = data["result"][0]["Speed"]
            wind_mph = float(wind_mph) * 3600.0 / 1609.0
            wind_mph = int(round(wind_mph))
            if(wind_mph <= 9):
                return '00' + str(wind_mph)
            elif(wind_mph > 9 and wind_mph < 100):
                return '0' + str(wind_mph)
            else:
                return str(wind_mph)
        except:
            return('...')

# wind gust
def wind_gust():
    if(int(json_wind_speed_idx) == 0):
        return('g...')
    else:
        try:
            response = urllib.urlopen(url+json_wind_gust_idx)
            data = json.loads(response.read())
            wind_mph = data["result"][0]["Gust"]
            wind_mph = float(wind_mph) * 3600.0 / 1609.0
            wind_mph = int(round(wind_mph))
            if(wind_mph <= 9):
                return 'g00' + str(wind_mph)
            elif(wind_mph > 9 and wind_mph < 100):
                return 'g0' + str(wind_mph)
            else:
                return 'g' + str(wind_mph)
        except:
            return('g...')

# outside temperature is a minimum information to generate WX APRS DATA
def outside_temp():
    global data_elements_count,data_elements_first
    if(int(json_temp_idx) == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_temp_idx)
            data = json.loads(response.read())
            data_elements_count = data_elements_count + 1
            data_elements_first = True
            temp_fahrenheit = int(round((data["result"][0]["Temp"]*9/5)+32))
            if(temp_fahrenheit < 100):
                zero = '0'
            else:
                zero = ''
            return('t' + zero + str(temp_fahrenheit))
        except:
            return('')

# rain 1h period currently not supported
def rain_1h():
    if(json_rain_1h_idx == 0):
        return('')
    else:
        return('')

# rain 24h period currently not supported
def rain_24h():
    if(json_rain_24h_idx == 0):
        return('')
    else:
        return('')

# rain after midnight period currently not supported
def rain_midnight():
    if(json_rain_midnight_idx == 0):
        return('')
    else:
        return('')

# relative humidity
def humi():
    global data_elements_count
    if(int(json_humi_idx) == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_humi_idx)
            data = json.loads(response.read())
            data_elements_count = data_elements_count + 1
            humi = int(data["result"][0]["Humidity"])
            if(humi == 100):
                humi = '00'
            return('h' + str(humi))
        except:
            return('')

# baromether
def baro():
    global data_elements_count
    if(int(json_baro_idx) == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_baro_idx)
            data = json.loads(response.read())
            data_elements_count = data_elements_count + 1
            baro = int(round(data["result"][0]["Barometer"]*10))
            if(baro < 10000):
                zero = '0'
            else:
                zero = ''
            return('b' + zero + str(baro))
        except:
            return('')

# raspberry inside temperature
def inside_temp():
    global data_elements_count,data_elements_first
    if(int(json_tempi_idx) == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_tempi_idx)
            data = json.loads(response.read())
            data_elements_count = data_elements_count + 1
            data_elements_first = True
            temp_celsius = float(round(data["result"][0]["Temp"],1))
            return('Int.T: ' + str(temp_celsius) + 'C ')
        except:
            return('')

# battery voltage
def voltage():
    global data_elements_count
    if(int(json_voltage_batt_idx) == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_voltage_batt_idx)
            data = json.loads(response.read())
            voltage = float(round(data["result"][0]["Voltage"],1))
            return('Bat: ' + str(voltage) + 'V ')
        except:
            return('')

def voltage_in_frame():
    global data_elements_count
    if(int(json_voltage_batti_idx) == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_voltage_batti_idx)
            data = json.loads(response.read())
            voltage = int(round(data["result"][0]["Voltage"],1)*10)
            return('V' + str(voltage))
        except:
            return('')

# read general pm sensor
def gen_dust():
    if(int(json_general_pm_idx) == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_general_pm_idx)
            data = json.loads(response.read())
            dust = data["result"][0]["Data"]
            dust = dust.replace(" ","")
            return('Dust:' + str(dust) + ' ')
        except:
            return('')

# read pm1 sensor
def gen_pm_1_dust():
    if(int(json_pm_1_idx) == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_pm_1_idx)
            data = json.loads(response.read())
            dust = data["result"][0]["Data"]
            dust = dust.replace(" ","")
            return('PM1:' + str(dust) + ' ')
        except:
            return('')

# read pm25 sensor
def gen_pm_25_dust():
    if(int(json_pm_25_idx) == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_pm_25_idx)
            data = json.loads(response.read())
            dust = data["result"][0]["Data"]
            dust = dust.replace(" ","")
            return('PM2.5:' + str(dust) + ' ')
        except:
            return('')

# read pm10 sensor
def gen_pm_10_dust():
    if(int(json_pm_10_idx) == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_pm_10_idx)
            data = json.loads(response.read())
            dust = data["result"][0]["Data"]
            dust = dust.replace(" ","")
            return('PM10:' + str(dust) + ' ')
        except:
            return('')

# read lightning detector data
def storm_data():
    if(int(json_thunder_dist_idx) == 0 or int(json_thunder_enrg_idx) == 0):
        storm_warning = False
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_thunder_dist_idx)
            data = json.loads(response.read())
            strike_distance = int(data["result"][0]["Data"].replace(" km",""))
            if(strike_distance == 0):
                return('')
            elif(strike_distance > 0 and strike_distance < 10):
                storm_warning = True
                return('STORM OVERHEAD!!! ')
            elif(strike_distance > 10 and strike_distance < 20):
                storm_warning = True
                return('STORM COMING ')
            elif(strike_distance > 20):
                storm_warning = True
                return('STORM DETECTED ')
        except:
            storm_warning = False
            return('')

# make WX data
def wx_data():
    outside_temp_label = outside_temp()
    # no data send status
    if(data_elements_count == 0 and not data_elements_first):
        return('!' + wx_lat + wx_icon_table + wx_lon +  wx_icon_symbol + ' ' + wx_err_comment)
    # we have some data
    else:
        return('!' + str(wx_lat) + wx_icon_table + str(wx_lon) + wx_icon_symbol + str(wind_direction()) + '/' + str(wind_speed()) + str(wind_gust()) + str(outside_temp()) + str(rain_1h()) + str(rain_24h()) + str(rain_midnight()) + str(humi()) + str(baro()) + str(voltage_in_frame()) + 'oDtz' + ' ' +str(get_sfi()) + str(voltage()) + str(inside_temp()) +  str(gen_dust()) + str(gen_pm_1_dust()) + str(gen_pm_25_dust()) + str(gen_pm_10_dust())  + storm_data() + str(wx_comment))

########################################### MAIN ################################################

# lets's go
print wx_data()

# END of This Shit
# Thanks to COVID-19
# #stayathometime
