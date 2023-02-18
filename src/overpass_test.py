import overpy

api = overpy.Overpass()

forbidden_highways = ["motorway", "trunk", "steps", "motorway_link", "trunk_link"]
bounding_box = (50.7, 7.1, 50.8, 7.25)

query = 'way["highway"]'
for highway in forbidden_highways:
    query += '["highway"!="{}"]'.format(highway)

query += '{};out body; >; out skel qt;'.format(bounding_box)

print(query)

result = api.query(query)

#result = api.query("""way["highway"]["highway"!="motorway"]["highway"!="trunk"]["highway"!="steps"]["highway"!="motorway_link"]["highway"!="trunk_link"](50.7,7.1,50.8,7.25);out;""")

for way in result.ways:
    print("Highway: %s" % way.tags.get("highway", "n/a"))
    print(f"Center: {way.center_lat}, {way.center_lon}")
    nodes = way.get_nodes(resolve_missing=True)
    for node in nodes:
        print("Node %s: lat=%f, lon=%f" % (node.id, node.lat, node.lon))