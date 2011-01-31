#!/usr/bin/python
# To execute this file:
# python KeypadMapper.py trace1.gpx ... <keypadmapper >keypadmapper.osm
import sys, string, datetime, time, math, calendar
from xml.dom import minidom

distanceFromTrace = 25
# This is the distance from the user to the point where the node is placed,
# when L or R is pressed. For F the distance will be more, because user must
# try to press F before turning. The units are meters, but there may still be
# something wrong with the calibration. 30 works well in South Africa where
# properties are typically 50 meters by 50 meters

l = sys.stdin.readline()
print "<?xml version='1.0' encoding='UTF-8'?>"
print "<osm version='0.6' generator='KeypadMapper.py'>"
nodeId = -1
time0 = 0
for i in range(1, len (sys.argv)) :
  print sys.argv[i]
  try:
    doc = minidom.parse (sys.argv[i])
    doc.normalize()
  except:
    print "<!-- ERROR WITH ", sys.argv[i], "-->"
  gpx = doc.documentElement
  for trk in gpx.getElementsByTagName('trk') :
    for trkseg in trk.getElementsByTagName('trkseg') :
      for trkpt in trkseg.getElementsByTagName('trkpt') :
        lat1 = float(trkpt.getAttribute('lat'))
        lon1 = float(trkpt.getAttribute('lon'))
        rfc3339 = trkpt.getElementsByTagName('time')[0].firstChild.data
        ts = datetime.datetime.strptime(rfc3339, '%Y-%m-%dT%H:%M:%SZ')
        time1 = calendar.timegm(ts.timetuple())
        if len(l) > 11 and int(l[0:10]) <= time1 :
          if time0 <= 0 :
            sys.stderr.write ('Warning: First entry precedes GPX data\n')
          else :
            latDif = lat1 - lat0
            lonDifAdj = (lon1 - lon0) / math.cos (lat1 / 180 * math.pi)
            speed = max (math.sqrt(latDif * latDif + lonDifAdj * lonDifAdj) \
                         * 111111 / distanceFromTrace, 0.0000001)
            # Times 111111 to convert from degrees latitude to meters.
            if l[13:14] == "F" :
              speed /= 2
              # The user should hit F before starting to turn. So he is
              # typically twice as far from the house as the L and R cases
              lonDif = lon1 - lon0
            else :
              latDif = -lonDifAdj
              lonDif = (lat1 - lat0) * math.cos (lat1 / 180 * math.pi)
              if l[13:14] == "L" :
                latDif, lonDif = -latDif, -lonDif
              
            print "<node id='"+str(nodeId)+"' visible='true' " \
                  "lat='"+str(lat1 + latDif / speed)+ \
                  "' lon='"+str(lon1 + lonDif / speed)+"' >"
            print "  <tag k='addr:housenumber' v='"+l[14:len(l)-1]+"' />"
            print "</node>"
            nodeId -= 1
          l = sys.stdin.readline()
        time0 = time1
        lat0 = lat1
        lon0 = lon1
if len(l) > 11 :
  sys.stderr.write ('Warning: No GPX data for last keypad entry\n')
print "</osm>"
