#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# DOMOTICZ to APRX PYTHON script
# SQ9MDD@2020 released under GPL.v.2
# http://sq9mdd.qrz.pl
#
# ramka pogodowa bez pozycji z czasem
# _mm dd gg mm                temp hum                baro
# _03 29 06 58 c025 s009 g008 t030 r000 p000 P000 h00 b10218
#
# ramka pogodowa z pozycja bez czasu
#                        _                temp hum                baro
# ! 5215.01N / 02055.58E _ ... / ... g... t030 r000 p000 P000 h00 b10218
#
# temp z sieci APRSjest w fahrenheit przeliczanie na C =(F-32)/9*5
# temp w celsjusz do sieci APRS trzeba wyslac jako fahrenheit F = (C*9/5)+32
#
################################### CONFIGURATION ###############################################
#                                                                                               #
wx_lat      	        = '5215.01N'                     	# coordinates APRS format           #
wx_lon      	        = '02055.58E'                    	# coordinates APRS format           #
json_ip                 = '10.9.48.3'                       # domoticz IP adress                #
# required                                                                                      #
json_wind_direction_idx = '0'                               # wind direction sensor IDX         #
json_wind_speed_idx     = '61'                              # wind speed sensor IDX             #
json_wind_gust_idx      = '61'                              # wind speed gust IDX               #
json_temp_idx           = '5'                               # Temp sensor IDX                   #
# optionally                                                                                    #
json_rain_1h_idx        = '0'                                                                   #
json_rain_24h_idx       = '0'                                                                   #
json_rain_midnight_idx  = '0'                                                                   #
json_humi_idx           = '5'                               # Humidity sensor IDX               #
json_baro_idx           = '5'                               # Baromether  IDX                   #
# additional                                                                                    #
json_tempi_idx          = '0'                               # inside temperature                #
json_pm_25_idx          = '0'                               # PM 2.5 sensor IDX                 #
json_pm_10_idx          = '0'                               # PM 10 sensor IDX                  #
json_general_pm_idx     = '58'                              # General PM sensor                 #
json_voltage_batt_idx   = '7'                               # Battery voltage sensor            #
wx_comment  	        = 'WXDomoPy'      	                # beacon comment		            #
wx_err_comment 	        = 'No WX data'				        # comment when no data avaiable	    #
#										      	                                                #
######################## DO NOTE EDIT BELLOW THIS LINE ##########################################

import json
import urllib, json
url = 'http://' + json_ip + '/json.htm?type=devices&rid='
data_elements_first = False
data_elements_count = 0

################################### FUNCTION ARE HERE ###########################################

# wind direction currently not supported
def wind_direction():
    if(json_wind_direction_idx == 0):
        return('...')
    else:
        return('...')

# wind speed currently not supported
def wind_speed():
    if(json_wind_speed_idx == 0):
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

# wind gust currently not supported
def wind_gust():
    if(json_wind_speed_idx == 0):
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
    if(json_temp_idx == 0):
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
    if(json_humi_idx == 0):
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
    if(json_baro_idx == 0):
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
    if(json_tempi_idx == 0):
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
    if(json_voltage_batt_idx == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_voltage_batt_idx)
            data = json.loads(response.read())
            voltage = float(round(data["result"][0]["Voltage"],1))
            return('Bat: ' + str(voltage) + 'V ')
        except:
            return('')

# read general pm sensor            
def gen_dust():
    if(json_general_pm_idx == 0):
        return('')
    else:
        try:
            response = urllib.urlopen(url+json_general_pm_idx)
            data = json.loads(response.read())
            dust = data["result"][0]["Data"]
            return('Dust: ' + str(dust) + ' ')
        except:
            return('')

# make WX data
def wx_data():
    outside_temp_label = outside_temp()
    # no data send status
    if(data_elements_count == 0 and not data_elements_first):
        return('!' + wx_lat + '/' + wx_lon + '_ ' + wx_err_comment)
    # we have some data
    else:
        return('!' + str(wx_lat) + '/' + str(wx_lon) + '_' + str(wind_direction()) + '/' + str(wind_speed()) + str(wind_gust()) + str(outside_temp()) + str(rain_1h()) + str(rain_24h()) + str(rain_midnight()) + str(humi()) + str(baro()) + ' ' + str(voltage()) + str(inside_temp()) +  str(gen_dust()) + str(wx_comment))

########################################### MAIN ################################################

# lets's go
print wx_data()

# END of This Shit
# Thanks to COVID-19
# #stayathometime
