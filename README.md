# WXDomoPy

The script downloads data from domoticz and prepares a complete weather frame, compliant with the APRS standard

## Configuration

Configuration comes down to filling in the IP address of the domoticz from which data will be collected, and the IDX of individual sensors.

## weather frame with position without time structure
 ramka pogodowa z pozycja bez czasu

   !               - required      identifier
   5215.01N        - required      latitude
   /               - required      symbol table
   02055.58E       - required      longtitude
   _               - required      icon (must be WX)
   ...             - required      wind direction (from 0-360) if no data set: "..."
   /               - required      separator
   ...             - required      wind speed (average last 1 minute) if no data set: "..."
   g...            - required      wind gust (max from last 5 mins) if no data set: "g..."
   t030            - required      temperature in fahrenheit
   r000            - option        rain xxx
   p000            - option        rain xxx
   P000            - option        rain xxx
   h00             - option        relative humidity (00 means 100%Rh)
   b10218          - option        atmosferic pressure in hPa multiple 10
   Fxxxx           - option        water level above or below flood stage see: http://aprs.org/aprs12/weather-new.txt
   V138            - option        battery volts in tenths   128 would mean 12.8 volts
   Xxxx            - option        radiation lvl

 temp z sieci APRSjest w fahrenheit przeliczanie na C =(F-32)/9*5
 temp w celsjusz do sieci APRS trzeba wyslac jako fahrenheit F = (C*9/5)+32

 WX possible icon:
 /_    - weather station wx blue
 /W    - national weather service
 /w    - water weather station
 \_    - weather station with digi green
 \W    - national weather services
