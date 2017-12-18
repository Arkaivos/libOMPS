#! /usr/bin/python

# libOMPS (Orbital Marker Positioning System) created by Arkaivos.
# Thanks to u/CreatureOfPrometheus for the math behind the _calculateAbsolutePosition method.

import ConfigParser
import numpy
import math

# This method allows us to convert a cartesian position vector into latitude, longitude, radius.
def _absoluteToCoordinates(absolutePosition):
    radius = numpy.linalg.norm(absolutePosition) # Magnitude 2-norm.
    latitudeRadians = math.asin(absolutePosition[2]/radius)
    longitudeRadians = math.atan2(absolutePosition[1], absolutePosition[0])

    latitude = latitudeRadians * 57.2958 # In degrees.
    longitude = longitudeRadians * 57.2958 # In degrees.
        
    return [latitude, longitude, radius]

# This class allows us to calculate the coordinates of a given point. In cartesian (x,y,z) and latitude/longitude/height format.
class OMPS:
    # celestialObject contains the name of the current planet/moon. It is used to load the absolute position of the anchors from the config file.
    # anchors is an array containing the name of the anchors that we are going to use to calculate the position of this point of interest.
    # distances is an array containing the distances between the point of interest and the anchors.
    def __init__(self, celestialObject, anchors, distances):
        self.absolutePosition = None
        self.celestialObject=celestialObject 
        self.anchors = anchors
        self.distances = distances
        
        # The less anchors, the more precision needed for an accurate result.
        precision = 60 - len(anchors)*10
        if precision <= 10:
            precision = 10
            
        self._calculateAbsolutePosition(precision)
        
    # Returns the name of the current celestial object.
    def getCelestialObject(self):
        return self.celestialObject
        
    # Returns the markers that are being used as anchors.
    def getAnchors(self):
        return self.anchors
        
    # Returns the distances from the point of interest to the anchors.
    def getDistances(self):
        return self.distances
        
    # This method calculates the absolute position of the point of interest given its distances to a given set of anchors.
    def _calculateAbsolutePosition(self, precision = 10):
        # New
        config = ConfigParser.RawConfigParser()
        config.optionxform = str
        config.read("celestialData.cfg")
        anchorPositions = []
        
        for anchor in self.anchors:
            anchorAbsolutePosition = config.get(self.celestialObject, anchor)
            anchorPositions.append(numpy.array([float(x) for x in anchorAbsolutePosition.split(",")]))
         
        # Initial estimated position in "ECEF" Coordinate System.
        estimatedPosition = numpy.array([0.0, 0.0, 0.0])
        
        # Iterations.
        for currentIteration in range(0,precision):
            for currentAnchor in range(0,len(self.anchors)): # For each Anchor:
                relativePosition = estimatedPosition - anchorPositions[currentAnchor]
                estimatedDistance = numpy.linalg.norm(relativePosition) # Magnitude 2-norm.
                unitVector = relativePosition / estimatedDistance
                distanceError = self.distances[currentAnchor] - estimatedDistance
                estimatedPosition = estimatedPosition + 0.5 * distanceError * unitVector
                
        self.absolutePosition = estimatedPosition.tolist()

    def getPosition(self):
        return self.absolutePosition
    
    def getCoordinates(self):
        [latitude, longitude, radius] = _absoluteToCoordinates(self.absolutePosition)
        return ["%.3f" % (latitude), "%.3f" % (longitude), "%.3f" % (radius)]
        
# This class allows us to obtain a dictionary containing all the points of interest for a given celestial objects. This points of interest are extracted from the config file.
class PointsOfInterest:
    def __init__(self, celestialObject):
        config = ConfigParser.RawConfigParser()
        config.optionxform = str
        config.read("celestialData.cfg")
        self.ips = config.items(celestialObject)
       
    def getAllCoordinates(self):
        dictionary = {}
        for i in range(0, len(self.ips)):
            dictionary[self.ips[i][0]] = _absoluteToCoordinates([float(x) for x in self.ips[i][1].split(",")])
        return dictionary