"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "OSM_data.xml"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Circle", "Highway", "Way"]

mapping = { "St": "Street",
            "St.": "Street",
            "Rd" : "Road",
            "Rd.": "Road",
            "Ave": "Avenue",
            "Blvd":"Boulevard",
            "Blvd.":"Boulevard",
            "Arthur":"Arthur St",
            "Wellesley":"Wellesley Avenue",
            "Main":"Main Avenue",
            }


def audit_street_type(street_types, street_name):
    """If the street type is not one of our expected types, add it to the 
    street types dictionary"""
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    """Opens OSM file, iterates through the elements, finds tags that denote
    street names and calls our audit function on those tags. Returns a
    dictionary of unexpected street types found along with an array of each 
    full street name for the types"""
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):
    """If the street type is in our list of mappings, replace it. Otherwise
    the same thing is returned"""
    parts = name.split()
    last = parts[-1]
    if last in mapping:
        parts[-1] = mapping[last]
        name = " ".join(parts)
    return name


def test():
    st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    """for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"""


if __name__ == '__main__':
    test()