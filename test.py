#! /usr/bin/python
# -*- coding: utf-8 -*-

# libOMPS (Orbital Marker Positioning System) created by Arkaivos.

import libOMPS 

# INPUT:
# In this example, out anchor points will be the 6 Orbital Markers.
anchors = ["OM1", "OM2", "OM3", "OM4", "OM5", "OM6"]
# The following array contains the distances between the interest point (Javelin position) and each of the anchors.
javelinDistancesToOMs = [472.4, 241.9, 605.9, 652.6, 768.2, 530.9]

# OUTPUT:
print("\n*** Orbital Marker Positioning System.")
print("*** Calculating the lost Javelin's coordinates:")
# We create the point of intereset indicating the moon in which it is placed, the anchors and the distances.
javelinPoI = libOMPS.OMPS("Daymar",anchors, javelinDistancesToOMs)

# The position of the Javelin in cartesian coordinates.
[x, y, z] = javelinPoI.getPosition()
print(x, y, z)

# The position of the Javelin in latitude/longitude/height coordinates.
[latitude, longitude, radius] = javelinPoI.getCoordinates()
print("Latitude: %sºN, Longitude: %sºE, Radius: %skm." % (latitude, longitude, radius))

print "\n*** Extra: Recover the anchor points of interest from the config file:"
pois = libOMPS.PointsOfInterest("Daymar").getAllCoordinates()
print(pois)