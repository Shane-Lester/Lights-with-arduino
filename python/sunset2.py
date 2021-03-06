#!/usr/local/bin/python3

# a Python script for PyEphem
# http://rhodesmill.org/pyephem/
# to find out the sunrise and sunset time
# in UTC
# (add more code for the local time by yourself)
# by Kenji Rikitake 6-OCT-2009

from datetime import datetime, timedelta
from time import localtime, strftime
import ephem

SEC30 = timedelta(seconds=30)

home = ephem.Observer()
# replace lat, long, and elevation to yours
home.lat = '54.5270'
home.long = '-1.5503'
home.elevation = 40

sun = ephem.Sun()

fmt = "%d-%b-%Y %H %M"

if __name__ == '__main__':

    sun.compute(home)

    nextrise = home.next_rising(sun)
    nextset = home.next_setting(sun)

    nextriseutc= nextrise.datetime() + SEC30
    nextsetutc= nextset.datetime() + SEC30

    
    hour= int((nextriseutc.strftime("%H")))
    minute =int((nextriseutc.strftime("%M")))

    #print(hour)
    #print(minute)

    #print ("next sunrise: ", nextriseutc.strftime(fmt))
    #print ("next sunset:  ", nextsetutc.strftime(fmt))

# end of code
