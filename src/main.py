import random
import math
import os
import requests
import json
import time

from coordinate import Coordinate
from route import Route

#Divide max length by this to get the radius for the random coordinate function
LENGTH_PER_POINT_RATIO = 3

#(As the crow flies) Adjust this to change the accuracy of the random coordinate function
ATCF = 0.8


def generate_route(origin, max_length, closed_route = True, max_point_amount=3):
    time.sleep(1)
    points = []

    #I. Generate random coordinates and get nearest address
    while len(points) < max_point_amount:
        radius = max_length * ATCF / LENGTH_PER_POINT_RATIO

        random_coordinate = origin.generate_on_street(radius)

        points.append(random_coordinate)
    
    
    #add home to points
    points.append(origin)

    #III. Get routing data and check if route is not too long
    route = Route(points)
    route.sort_by_distance(origin)

    for point in points:
        print(point)

    try:
        route.generate_routing()

        length = route.get_length()
        if length > max_length or length == -1:
            print("TOO LONG")
            print("RETRYING")
            return generate_route(origin, max_length, closed_route, max_point_amount)
        
        
        return route
    except Exception as e:
        print("ERROR")
        print(e)
        return generate_route(origin, max_length, closed_route, max_point_amount)


def __dbg_gen_route():
    p = generate_route(Coordinate(51.846812, 6.242033), 25000)

    print("API INFO:")

    print(p.routing["features"][0]["properties"]["summary"])


#for i in range(230):
#    print(Coordinate(51.846812, 6.242033).generate_random(15000))

__dbg_gen_route()