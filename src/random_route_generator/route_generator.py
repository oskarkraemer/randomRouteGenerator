from coordinate import Coordinate
from route import Route

class RouteGenerator:
    """ Class to generate a random route """

    class ROUTE_MODE:
        """ Enum for the route mode (handling the origin point in the route) """

        EXCLUDE_ORIGIN = 0 # Don't include the origin point from the route
        START_ORIGIN = 1 # Start the route at the origin point (end at random point)
        END_ORIGIN = 2 # End the route at the origin point (start at random point)
        START_END_ORIGIN = 3 # Start and end the route at the origin point


    def __init__(self):
        self.api_key = ""
        self.routing_profile = "cycling-regular"

        self.route_mode = self.ROUTE_MODE.START_END_ORIGIN
        self.point_amount = 4
        self.avoids = ["ferries", "steps"]

        """ A constant to change the radius of each generated coordinate. """
        """ The higher the value, the closer the points to the origin."""
        self.radius_factor = 0.25
    
    def read_api_key(self, path):
        """ Reads the API key from a file. """
        with open(path, "r") as f:
            self.api_key = f.read()
    
    def generate_route(self, origin, max_length):
        """ Generates a random route with an origin point and a maximum length in metres."""
        points = []

        #I. Generate random coordinates and get nearest address
        while len(points) < self.point_amount:
            radius = max_length / (self.point_amount + 3)

            random_coordinate = origin.generate_on_street(radius, cycle = "cycling" in self.routing_profile)

            points.append(random_coordinate)
        

        #II. Add home to points if mode is START_ORIGIN or START_END_ORIGIN
        if self.route_mode == self.ROUTE_MODE.START_ORIGIN or self.route_mode == self.ROUTE_MODE.START_END_ORIGIN:
            points.append(origin)

        #III. Sort points by distance to origin
        route = Route(points)
        route.sort_by_distance(origin)

        
        #IV. Add home to points if mode is END_ORIGIN or START_END_ORIGIN
        if self.route_mode == self.ROUTE_MODE.END_ORIGIN or self.route_mode == self.ROUTE_MODE.START_END_ORIGIN:
            route.points.append(origin)

        #V. Generate routing
        route.generate_routing(self.api_key, self.routing_profile, self.avoids)

        length = route.get_length()
        if length > max_length or length == -1:
            print("TOO LONG")
            print("RETRYING")
            return self.generate_route(origin, max_length)
                
        return route