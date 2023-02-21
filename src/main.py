import random
import math
import os
import requests
import json
import time

from route_generator import RouteGenerator
from coordinate import Coordinate

def __dbg_gen_route():
    generator = RouteGenerator()
    #generator.api_key = ""
    generator.read_api_key("ors_api.key")
    generator.routing_profile = "cycling-mountain"

    p = generator.generate_route(Coordinate(51.846812, 6.242033), 25000)

    print("API INFO:")

    print(p.routing["features"][0]["properties"]["summary"])
    
    for x in p.points:
        print(x)

    p.generate_gpx_file(filename="out.gpx")

__dbg_gen_route()