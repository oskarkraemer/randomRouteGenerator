import math
import requests
import json
import random

class Coordinate:
    """A class to represent a coordinate."""

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return "<" + str(self.lat) + ";" + str(self.lon) + ">"
    
    @staticmethod
    def randomize(origin, radius):
        """Returns a random coordinate within a radius in metres of the origin."""
        #BROKEN
        #BROKEN
        #BROKEN
        x0 = origin.lon
        y0 = origin.lat

        # Convert radius from metres to degrees
        radiusInDegrees = radius / 111300

        u = float(random.uniform(0.0, 1.0))
        v = float(random.uniform(0.0, 1.0))

        w = radiusInDegrees * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)

        # Adjust the x-coordinate for the shrinking of the east-west distances
        new_x = x / math.cos(y0)

        foundLongitude = new_x + x0
        foundLatitude = y + y0

        return Coordinate(foundLatitude, foundLongitude)
    
    def distance_to(self, other):
        """Calcualtes the distance between this coordinate and another in metres."""
        R = 6373.0

        lat1 = math.radians(self.lat)
        lon1 = math.radians(self.lon)
        lat2 = math.radians(other.lat)
        lon2 = math.radians(other.lon)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c

        return distance
    
    def get_api_info(self):
        """Queries the Photon API for information about this coordinate."""
        url = "https://photon.komoot.io/reverse?lon=" + str(self.lon) + "&lat=" + str(self.lat)

        response = requests.get(url)
        json_data = json.loads(response.text)

        return json_data