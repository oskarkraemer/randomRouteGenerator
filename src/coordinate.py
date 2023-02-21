import math
import requests
import json
import random
import haversine
import math
import overpy

class Coordinate:
    """A class to represent a coordinate."""

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

        #Data for API caching
        self.__overpass_cache = {}
        self.__cache_radius = 0
        self.__cache_cycle = False

    def __str__(self):
        return str(self.lat) + ", " + str(self.lon)

    def in_distance(self, distance, direction):
        """Returns a coordinate at a given distance and direction from self."""
        r = haversine.inverse_haversine((self.lat, self.lon), distance / 1000, direction)
        return Coordinate(r[0], r[1])
    
    def generate_random(self, radius):
        """Returns a random coordinate within a radius in metres of self."""
        max_coord = self.in_distance(radius, haversine.Direction.NORTH)
        radius = max_coord.lat - self.lat

        r = radius * math.sqrt(random.random())
        theta = 2 * math.pi * random.random()

        foundLatitude = r * math.cos(theta) + self.lat
        foundLongitude = r * math.sin(theta) * 2 + self.lon

        #print(math.cos(self.lat))

        return Coordinate(foundLatitude, foundLongitude)
    
    def generate_on_street(self, radius, cycle = True):
        """Returns a random coordinate on a street within a radius in metres of the origin."""
        """Cycle is a boolean that determines if the coordinate should be reachable on a bicycle."""

        #Check if valid API cache can be used
        if self.__cache_radius == radius and self.__cache_cycle == cycle:
            return random.choice(self.__overpass_cache)
        
        api = overpy.Overpass()

        if cycle:
            forbidden_highways = ["motorway", "trunk", "steps", "motorway_link", "trunk_link"]
        else:
            forbidden_highways = []
        
        #Calculate bounding box
        no_coordinate = self.in_distance(radius, haversine.Direction.NORTHEAST)
        sw_coordinate = self.in_distance(radius, haversine.Direction.SOUTHWEST)

        bounding_box = (sw_coordinate.lat, sw_coordinate.lon, no_coordinate.lat, no_coordinate.lon)

        query = 'way["highway"]'
        for highway in forbidden_highways:
            query += '["highway"!="{}"]'.format(highway)

        query += '{};out body; >; out skel qt;'.format(bounding_box)

        print(query)

        #Try to query the Overpass API
        result = None
        success = False
        urls = ["http://lz4.overpass-api.de/api/interpreter", 
            "http://z.overpass-api.de/api/interpreter", 
            "http://maps.mail.ru/osm/tools/overpass/api/interpreter", 
            "http://overpass.openstreetmap.ru/api/interpreter", 
            "http://overpass.osm.ch/api/interpreter", 
            "http://overpass.kumi.systems/api/interpreter"
        ]
        
        for url in urls:
            try:
                api.url = url
                result = api.query(query)
                success = True
                break
            except Exception as e:
                print(e)
                print("Failed to query Overpass API at " + url)

    
        #Store every way-coordinate in a list
        candidates = []

        for way in result.ways:
            #print("Highway: %s" % way.tags.get("highway", "n/a"))
            #print(f"Center: {way.center_lat}, {way.center_lon}")
            nodes = way.get_nodes(resolve_missing=True)
            for node in nodes:
                #print("Node %s: lat=%f, lon=%f" % (node.id, node.lat, node.lon))
                candidates.append(Coordinate(node.lat, node.lon))
        

        #Store result in cache
        self.__overpass_cache = candidates
        self.__cache_radius = radius
        self.__cache_cycle = cycle
        
        #Select a random coordinate from the list
        return random.choice(candidates)

    
    def distance_to(self, other):
        """Returns the distance in metres between this coordinate and another."""
        return haversine.haversine((self.lat, self.lon), (other.lat, other.lon)) * 1000
    
    def get_api_info(self):
        """Queries the Photon API for information about this coordinate."""
        url = "https://photon.komoot.io/reverse?lon=" + str(self.lon) + "&lat=" + str(self.lat)

        response = requests.get(url)
        json_data = json.loads(response.text)

        return json_data