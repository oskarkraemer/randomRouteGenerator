import math
import json
import requests
import gpxpy

from . import coordinate

class Route:
    """Class for interacting with the OpenRouteService API and handling the response."""

    def __init__(self, points):
        self.points = points
        self.routing_points = []
        self.routing = {}
    
    def sort_by_distance(self, point):
        """Sorts points by distance to a given point."""
        self.points.sort(key=lambda x: x.distance_to(point))

    def __extract_corrected_points(self):
        """Extract the corrected points from the routing data."""
        points = []
        for feature in self.routing["features"]:
            for coord in feature["geometry"]["coordinates"]:
                points.append(coordinate.Coordinate(coord[1], coord[0]))
        return points

    def generate_routing(self, api_key, routing_profile, avoids = ["ferries", "steps"]):
        """Generate a route from a list of points. Query the OpenRouteService API and store the response in self.data."""

        #send post request to url and parse json
        url = f"https://api.openrouteservice.org/v2/directions/{routing_profile}/geojson"

        #convert points to tuple array
        p = []
        for point in self.points:
            p.append((float(point.lon), float(point.lat)))

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
            "Authorization": api_key
        }

        response = requests.post(url, json=data, headers=headers)
        json_data = json.loads(response.text)

        #check for errors
        if not ("features" in json_data):
            try:
                if json_data["error"] == "Authorization field missing":
                    raise Exception("No API key provided. Please provide a valid API key.")
                
                if json_data["error"] == "Access to this API has been disallowed":
                    raise Exception("The API key provided is invalid. Please provide a valid API key.")

                if json_data["error"]["code"] == 2010:
                    raise Exception("No route found. Try again with different parameters.")
            
            except TypeError:
                pass
            
            raise Exception("Error while generating routing: " + json.dumps(json_data))

        self.routing = json_data

        #extract points in self.points
        self.routing_points = self.__extract_corrected_points()
    
    def get_length(self):
        """Returns the length of the route in metres."""
        if self.routing == {}:
            raise Exception("No routing data available. Call generate_routing() first.")
        
        try:
            return self.routing["features"][0]["properties"]["summary"]["distance"] * 1000
        except KeyError:
            return -1
    
    def get_duration(self):
        """Returns the duration of the route in seconds."""
        if self.routing == {}:
            raise Exception("No routing data available. Call generate_routing() first.")
        
        try:
            return self.routing["features"][0]["properties"]["summary"]["duration"]
        except KeyError:
            return -1
    
    def get_elevation(self):
        """Returns the elevation of the route in metres."""
        if self.routing == {}:
            raise Exception("No routing data available. Call generate_routing() first.")
        
        try:
            ascent = self.routing["features"][0]["properties"]["ascent"]
            descent = self.routing["features"][0]["properties"]["descent"]

            r = {
                "ascent": ascent,
                "descent": descent,
                "elevation_gain": ascent - descent
            }

            return r
        except KeyError:
            return {}

    def get_way_info(self):
        """Returns the way info of the route."""
        if self.routing == {}:
            raise Exception("No routing data available. Call generate_routing() first.")
        
        try:
            return self.routing["features"][0]["properties"]["extras"]
        except KeyError:
            return {}
    
    def generate_gpx_file(self, filename):
        """Generates a GPX file from the routing data."""
        if self.routing == {}:
            raise Exception("No routing data available. Call generate_routing() first.")
        
        gpx = gpxpy.gpx.GPX()

        #create track
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        #create segment
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        #add points
        for point in self.routing_points:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point.lat, point.lon))
        
        #write to file
        with open(filename, "w") as f:
            f.write(gpx.to_xml())