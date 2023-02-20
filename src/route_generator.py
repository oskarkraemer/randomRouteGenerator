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

        #(As the crow flies) Factor to reduce the radius per coordinate [maybe deprecated]
        self.__ATCF = 0.25
    
    def generate_route(self, origin, max_length, route_mode = ROUTE_MODE.START_END_ORIGIN, point_amount = 3):
        """ Generates a random route with an origin point and a maximum length in metres."""
        points = []

        #I. Generate random coordinates and get nearest address
        while len(points) < point_amount:
            radius = max_length / (point_amount + 2)

            random_coordinate = origin.generate_on_street(radius)

            points.append(random_coordinate)
        

        #II. Add home to points if mode is START_ORIGIN or START_END_ORIGIN
        if route_mode == self.ROUTE_MODE.START_ORIGIN or route_mode == self.ROUTE_MODE.START_END_ORIGIN:
            points.append(origin)

        #III. Sort points by distance to origin
        route = Route(points)
        route.sort_by_distance(origin)

        
        #IV. Add home to points if mode is END_ORIGIN or START_END_ORIGIN
        if route_mode == self.ROUTE_MODE.END_ORIGIN or route_mode == self.ROUTE_MODE.START_END_ORIGIN:
            route.points.append(origin)

        #V. Generate routing
        route.generate_routing(self.api_key)

        length = route.get_length()
        if length > max_length or length == -1:
            print("TOO LONG")
            print("RETRYING")
            return self.generate_route(origin, max_length, route_mode, point_amount)
                
        return route