<p align="center">
  <a href="">
    <img src="banner.png" alt="Repository Banner">
  </a>
</p>

A Python package to generate a random route with a specified length.

Utilizes the openrouteservice API to generate the routing and the Overpass API for picking a random location. 

## Installation

Random-Route-Generator releases are available as wheel packages for macOS, Windows and Linux on [PyPI](https://pypi.org/project/random-route-generator/). Install it using `pip`:

```bash
pip install random-route-generator
```

## Example

This script generates a random route which is **maximum 25km** long and starts at the coordinate **(51.846812, 6.242033)**. It uses **mountain-biking** route generation and utilizes **4 random points**. The route also **avoids ferries** and **steps** and is **self-contained**.

```python
from randomRouteGenerator.route_generator import RouteGenerator
from randomRouteGenerator.coordinate import Coordinate

generator = RouteGenerator()

#Manually set the openrouteservice API key
generator.api_key = ""

#OR read the API key from a file
#generator.read_api_key("ors_api.key")


#What type of route generation should be used? (See README)
generator.routing_profile = "cycling-mountain"

#How many random points should be generated?"
generator.point_amount = 4

#How should the origin and end point be handled (See RouteGenerator.ROUTE_MODE)?
generator.route_mode = generator.ROUTE_MODE.START_END_ORIGIN

#Which features should be avoided in the route?
generator.avoids = ["ferries", "steps"]

#Generate the route with the given origin point and maximum length
p = generator.generate_route(Coordinate(51.846812, 6.242033), 25000)


length = p.get_length()
duration = p.get_duration()
elevation = p.get_elevation()

#Retrieve information about the road-types in the route i.e. gravel, paved, ...
print(p.get_way_info())

#Print all routing points (all points generated by the routing)
for x in p.routing_points:
	print(x)



#Print all way-points (ONLY the random points whose amount is specified in generator.point_amount)
for x in p.points:
	print(x)


#Generate a GPX file containing the route
p.generate_gpx_file(filename="out.gpx")
```


## Profiles
* driving-car (Regular car routing)
* driving-hgv (Routing for heavy-trucks)
* cycling-regular (Routing for regular cycling)
* cycling-road (Routing for road bikes)
* cycling-mountain (Routing for mountain bikes, prefers offroad tracks)
* cycling-electric (Routing for E-bikes)

## Credits

* [openrouteservice](https://openrouteservice.org/) - Used to generate the routing between the points
* [Overpass-API](http://overpass-api.de/) - Used for picking a random location
* [gpxpy](https://github.com/tkrajina/gpxpy) - Used for exporting to a GPX file
* [overpy](https://pypi.org/project/overpy/) - Used for communicating with the Overpass-API
* [haversine](https://pypi.org/project/haversine/) - Used for coordinate calculations

## License

[GPL v3.0](https://github.com/oskarkraemer/youtubeWordFinder/blob/main/LICENSE)
