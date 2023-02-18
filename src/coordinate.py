import math
import requests
import json
import random
import haversine
import math

class Coordinate:
    """A class to represent a coordinate."""

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return "" + str(self.lat) + " " + str(self.lon) + ""
    
    @staticmethod
    def randomize(origin, radius):
        """Returns a random coordinate within a radius in metres of the origin."""
        max_coord = haversine.inverse_haversine((origin.lat, origin.lon), radius / 1000, haversine.Direction.NORTH)
        radius = max_coord[0] - origin.lat

        r = radius * math.sqrt(random.random())
        theta = 2 * math.pi * random.random()

        foundLatitude = r * math.cos(theta) + origin.lat
        foundLongitude = r * math.sin(theta) * 2 + origin.lon

        #print(math.cos(origin.lat))

        return Coordinate(foundLatitude, foundLongitude)
    
    def distance_to(self, other):
        """Returns the distance in metres between this coordinate and another."""
        return haversine.haversine((self.lat, self.lon), (other.lat, other.lon)) * 1000
    
    def get_api_info(self):
        """Queries the Photon API for information about this coordinate."""
        url = "https://photon.komoot.io/reverse?lon=" + str(self.lon) + "&lat=" + str(self.lat)

        response = requests.get(url)
        json_data = json.loads(response.text)

        return json_data