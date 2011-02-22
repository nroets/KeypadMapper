#!/usr/bin/python
# To execute this file:
# python KeypadMapper.py trace1.gpx keypadmapper
import sys, string, datetime, time, math, calendar
from os import path
from xml.dom import minidom

distanceFromTrace = 25
# This is the distance from the user to the point where the node is placed,
# when L or R is pressed. For F the distance will be more, because user must
# try to press F before turning. The units are meters, but there may still be
# something wrong with the calibration. 30 works well in South Africa where
# properties are typically 50 meters by 50 meters

VAR1 = 111111 / float(distanceFromTrace) # Times 111111 to convert from degrees latitude to meters.

header = "<?xml version='1.0' encoding='UTF-8'?>\n<osm version='0.6' generator='KeypadMapper_v2.py'>\n"
nodeId = -1
time0 = 0

try:
  fn1 = sys.argv[1]
  doc = minidom.parse( fn1 )
  doc.normalize()
except:
  print "Error while loading gpx file"
  exit(1)
  
try:
  fn2 = sys.argv[2]
  keypadmapperFile = file.open(fn2, r)
except:
  print "Fail opening Keymapper file"
  exit(1)
l = keypadmapperFile.readline()

try:
  osmOut = file.open(path.dirname(fn1)+'/'+path.splitext(fn1)[0]+'.osm', w)
except:
  print "Fail opening osm file for writing"
  exit(1)
write = osmOut.write
write(header)

gpx = doc.documentElement
for trk in gpx.getElementsByTagName('trk') :
  for trkseg in trk.getElementsByTagName('trkseg') :
    for trkpt in trkseg.getElementsByTagName('trkpt') :
      try:
        lat1 = float(trkpt.getAttribute('lat'))
      except:
        print "Ignoring a trackpoint: lat is missing"
        continue
      try:
        lon1 = float(trkpt.getAttribute('lon'))
      except:
        print "Ignoring a trackpoint: lon is missing"
        continue
      try:
        rfc3339 = trkpt.getElementsByTagName('time')[0].firstChild.data
      except:
        print "Ignoring a trackpoint: time is missing"
        continue
      try:
        ts = datetime.datetime.strptime(rfc3339, '%Y-%m-%dT%H:%M:%SZ')
      except:
        print "Ignoring a trackpoint: timesting cannot be parsed"
        continue
      time1 = calendar.timegm(ts.timetuple())
      if len(l) > 11 and int(l[0:10]) <= time1 :
        if time0 <= 0 :
          print 'Warning: First entry precedes GPX data'
        else :
          latDif = lat1 - lat0
          lonDifAdj = (lon1 - lon0) / math.cos (lat1 / 180. * math.pi)
          speed = max (math.sqrt(latDif * latDif + lonDifAdj * lonDifAdj) \
                       * VAR1, 0.0000001)
          if l[13:14] == "F" :
            speed /= 2.
            # The user should hit F before starting to turn. So he is
            # typically twice as far from the house as the L and R cases
            lonDif = lon1 - lon0
          else :
            latDif = -lonDifAdj
            lonDif = (lat1 - lat0) * math.cos (lat1 / 180. * math.pi)
            if l[13:14] == "L" :
              latDif *= -1
              lonDif *= -1
            
          out = "\t<node id='", str(nodeId), "' visible='true' lat='", \
              str(lat1 + latDif / speed), "' lon='", str(lon1 + lonDif / speed), \
              "'>\n", "\t\t<tag k='addr:housenumber' v='", l[14:len(l)-1], \
              "' />\n\t</node>"
          for stringElement in out:
            write(stringElement)
          nodeId -= 1
        l = keypadmapperFile.readline()
      time0 = time1
      lat0 = lat1
      lon0 = lon1
if len(l) > 11 :
  print'Warning: No GPX data for last keypad entry'
write("</osm>")
keypadmapperFile.close()
osmOut.close()
