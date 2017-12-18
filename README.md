# libOMPS (Orbital Marker Positioning System)

This library provides basic orientation functionality in Star Citizen moons and planets. It allows you to transform a set of distances between a given location and a set of fixed anchors to latitude, longitude and height coordinates.

- libOMPS.py: Python library containing the OMPS Class.
- test.py: Python example program that makes use of the library to calculate the coordinates of the lost Javelin.
- celestialData.cfg: Config file containting the points of interest and orbital markers from the different planets and moons in Star Citizen.

This library creates a cartesian frame of reference fixed in the center of the celestial object (planet/moon) using the positions of the Orbital Markers as axies.
This cartesian frame of reference is used to determine the absolute positions of any given location, that can be converted to latitude/longitude coordinates and painted in a map.

Thanks to u/CreatureOfPrometheus for the underlying math behind this method. For more information, you can check here:
https://www.reddit.com/r/starcitizen/comments/7keaoj/using_om_markers_to_survey_a_world/

I'm also creating a webapp using this library, that will allow us to mark positions in a map of the moon/planet and view the locations of every point of interest on a given celestial object.

- Check the test.py for an example of use of the libray.
- The config file contains one section for each planet/moon. Inside each section there are the several items: the six orbital markers and the different points of interest of that planet/moon.
- Each item contains a 3D vector that indicates the absolute position of the item in the cartesian frame of reference with origin in the center of the planet/moon.
