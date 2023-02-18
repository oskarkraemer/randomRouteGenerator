import math
import json
import requests

from coordinate import Coordinate

class Route:
    """Class for interacting with the OpenRouteService API and handling the response."""

    def __init__(self, points):
        self.points = points
        self.routing = {}

        self.ferries = False
        self.steps = False
        self.fords = True
    
    def sort_by_distance(self, point):
        """Sorts points by distance to a given point."""
        self.points.sort(key=lambda x: x.distance_to(point))

    def __extract_corrected_points(self):
        """Extract the corrected points from the routing data."""
        points = []
        for feature in self.routing["features"]:
            for coord in feature["geometry"]["coordinates"]:
                points.append(Coordinate(coord[1], coord[0]))
        return points

    def generate_routing(self):
        """Generate a route from a list of points. Query the OpenRouteService API and store the response in self.data."""

        #send post request to url and parse json
        url = "https://api.openrouteservice.org/v2/pdirections/cycling-regular/geojson"

        #convert points to tuple array
        p = []
        for point in self.points:
            p.append((point.lon, point.lat))

        #cunstruct avoid features array
        avoids = []
        if not self.ferries:
            avoids.append("ferries")
        if not self.steps:
            avoids.append("steps")
        if not self.fords:
            avoids.append("fords") 
        

        data = {
            "coordinates": p,
            "elevation": True,
            "instructions_format":"html",
            "extra_info":["surface","steepness","waytype"],
            "language":"en",
            "units":"km",
            "preference":"recommended",
            "options":{"avoid_features": avoids}
        }

        headers = {
            "Authorization": "5b3ce3597851110001cf6248b813db0f732349eb8ad539782dfa1207",
            "Origin": "https://openrouteservice.org",
            "Referer": "https://openrouteservice.org/",
        }

        response = requests.post(url, json=data, headers=headers)
        json_data = json.loads(response.text)

        #print(json_data)

        if json_data["error"]["code"] == 2010:
            print(json_data)
            raise Exception("No route found. Try again with different parameters.")

        self.routing = json_data

        #extract points in self.points
        self.points = self.__extract_corrected_points()
    
    def get_length(self):
        """Returns the length of the route in metres."""
        if self.routing == {}:
            raise Exception("No routing data available. Call generate_routing() first.")
        
        try:
            return self.routing["features"][0]["properties"]["summary"]["distance"] * 1000
        except KeyError:
            return -1