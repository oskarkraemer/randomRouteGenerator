import random
import math
import os
import requests
import json

from coordinate import Coordinate
from route import Route

#1 generate random coordinates in a given range
#2 get nearest address from coordinates
#3 check if route to address is not using a ferry (routing api)
#4 check again if route is near the given range (same api as 3), maybe +- 1km

BLOCKED_KEYS = ["waterway", "barrier", "aerialway", "water"]

#Divide max length by this to get the radius for the random coordinate function
LENGTH_PER_POINT_RATIO = 1

#(As the crow flies) Adjust this to change the accuracy of the random coordinate function
ATCF = 0.8



def generate_route(origin, max_length, closed_route = True, max_point_amount=3):
    points = []

    #I. Generate random coordinates and get nearest address
    while len(points) < max_point_amount:
        radius = max_length * ATCF / LENGTH_PER_POINT_RATIO
        random_coordinate = Coordinate.randomize(origin, radius)
        points.append(random_coordinate)
    
    for point in points:
        print(f"lat: {point.lat}, lon: {point.lon}")
    
    #add home to points
    points.append(origin)

    #III. Get routing data and check if route is not too long
    route = Route(points)
    route.sort_by_distance(origin)

    route.generate_routing()

    if route.get_length() > max_length: 
        return generate_route(origin, radius, max_point_amount)
    
    return route


p = generate_route(Coordinate(51.846812, 6.242033), 15000)
print("POINTS:")
#print(p.points)

print("API INFO:")

print(p.routing["features"][0]["properties"]["summary"])