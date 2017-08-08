import sys, time, os
from pantilt import *
from time import sleep
import datetime
from astral import Astral
import pytz
from pytz import timezone as timezones

a = Astral()
city_name = 'Boston'
city = a[city_name]
print('Information for %s/%s\n' % (city_name, city.region))
timezone = city.timezone
print('Timezone: %s' % timezone)
sun = city.sun(datetime.datetime.now(), local=True)
print('Dawn:    %s' % str(sun['dawn']))
print('Sunrise: %s' % str(sun['sunrise']))
print('Noon:    %s' % str(sun['noon']))
print('Sunset:  %s' % str(sun['sunset']))
print('Dusk:    %s' % str(sun['dusk']))

sunlightHours = abs(sun['sunrise'].hour-sun['sunset'].hour)
print('sunlight hours')
print sunlightHours

print('sunlight total minutes')
totalsunMinutes = (abs(sun['sunrise'].hour-sun['sunset'].hour)*60)+(sun['sunset'].minute-sun['sunrise'].minute)
print totalsunMinutes

global cam_pan
global cam_tilt
cam_pan = 100
cam_tilt = 220
# Turn the camera to the default position
pan(110)
tilt(90)
print('before')
sleep(5)


hourCounter = sun['sunrise'].hour

hoursBetweenRiseNoon = sun['noon'].hour - sun['sunrise'].hour
hoursBetweenNoonSet = sun['sunset'].hour - sun['noon'].hour

print(hoursBetweenRiseNoon)
print(hoursBetweenNoonSet)

minutesBetweenRiseNoon = hoursBetweenRiseNoon * 60 + (sun['noon'].minute - sun['sunrise'].minute)
minutesBetweenNoonSet = hoursBetweenNoonSet * 60 + (sun['noon'].minute - sun['sunset'].minute)

print(minutesBetweenRiseNoon)
print(minutesBetweenNoonSet)


#move to sunrise position
def sunrise():
    global cam_pan, cam_tilt
    cam_pan = 10
    cam_tilt = 120
    pan(cam_pan)
    tilt(cam_tilt)
    print('test sunrise')

#move to sunnoon position
def sunnoon():
    global cam_pan, cam_tilt
    cam_pan = 100
    cam_tilt = 220
    pan(cam_pan)
    tilt(cam_tilt)
    print('test noon')

#move to sunset position
def sunset():
    global cam_pan, cam_tilt
    cam_pan = 220
    cam_tilt = 340
    pan(cam_pan)
    tilt(cam_tilt)
    print('test sunset')

while True:
    global cam_pan, cam_tilt

    eastern = timezones('US/Eastern')
    loc_dt = datetime.datetime.now(eastern)
    print(loc_dt)
    
    #if time is after sunset run sunrise function
    if loc_dt.hour <= sun['sunrise'].hour:
        #if loc_dt.minute >= sun['sunset'].minute:
        sunrise()
        print('sunrise')

    #If time is equal to the runrise run sunrise fuction
    if loc_dt.hour == sun['sunrise'].hour:
	if loc_dt.minute == sun['sunrise'].minute:
	    sunrise()
            print('test sunrise')
    #if time is after sunrise then loop till noon
    if loc_dt.hour == sun['sunrise'].hour and loc_dt.now().minute > sun['sunrise'].minute:
        print('between rise and noon')
	for x in range(0, 100):
	    tilt(120+x)
	    cam_pan = x
	    #if x < 10:
	    #    tilt(120+10)
	    pan(cam_pan)
	    sleep(((minutesBetweenRiseNoon*60)-120)/100)

    #if time is noon run sunnoon function
    if loc_dt.hour == sun['noon'].hour:
        if loc_dt.minute == sun['noon'].minute:
            sunnoon()
            print('test sunoon')

    #if time is after noon loop till sunset
    if loc_dt.hour == sun['noon'].hour and loc_dt.minute > sun['noon'].minute:
        print('between noon and set')
        for x in range(100, 220):
            cam_pan = x
	    tilt(120+x)
            pan(cam_pan)
            sleep(((minutesBetweenNoonSet*60)-120)/120)

    #if time is noon run sunset function
    if loc_dt.hour == sun['sunset'].hour:
        if loc_dt.minute == sun['nsunset'].minute:
            sunset()
            print('test sunset')
    print('fuck')
    #if time is after sunset run sunrise function
    if loc_dt.hour > sun['sunset'].hour:
        #if loc_dt.minute >= sun['sunset'].minute:
        sunrise()
        print('sunset')

    print('sunset hour')
    print(sun['sunset'].hour)
    print('now hour')
    print(loc_dt.hour)
