import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import os
path='C:\\Users\\aemra\\Documents\\GitHub\\Wrangle-OpenStreetMap-Data'
os.chdir(path)
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

created = {'version': None, 'timestamp': None, 'changeset': None, 'user': None,
           'uid': None}
L = []
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def update_name(name, mapping):
    for v in mapping:
        #print v
        if re.search(v,name):
            name=name.replace(v,mapping[v])       
            return name
        else:
            pass
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd." : "Road",
           'Ave.': 'Avenue',
           'Blvd' : 'Boulevard',
           'Blvd.':'Boulevard',
           'Dr': 'Drive',
           'Frwy':'Freeway',
           'Pkwy': 'Parkway',
           'Rd':'Road',
           'Rd.':'Road',
           'Stree':'Street',
           'blvd':'Boulevard',
           'street':'Street'
            }
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons",'Freeway','Road','Way']


def shape_element(element):
    node = {}
    if element.tag == "node" :
        # YOUR CODE HERE
        created = {}
        for e in element.attrib.keys():
            
            if e in CREATED:
                
                created[e] = element.attrib[e]
                
                
            elif  element.attrib[e] == element.get('lat') or element.attrib[e] == element.get('lon'):
                pos = []
                pos.append(float(element.get('lat')))
                pos.append(float(element.get('lon')))
                node['pos'] = pos

            else:
                node[e] = element.get(e)
                
                
                node['type'] = element.tag

        node['created'] = created
            

        node_refs = []
        address = {}
        for subtag in element:
            if subtag.tag == 'tag':
                if re.search(problemchars, subtag.get('k')):
                    pass
                elif re.search(r'\w+:\w+:\w+', subtag.get('k')):
                    pass
                elif subtag.get('k').startswith('addr:'):
                    address[subtag.get('k')[5:]] = update_name(subtag.attrib['k'],mapping)
                    node['address'] = address
                elif subtag.get('k').startswith("FIXME") or subtag.get('k').startswith("FIXME"):
                    pass
                elif subtag.get("k").startswith('Zipcode') and not subtag.get('v').startswith("77"):
                    pass
                else:
                    node[subtag.get('k')] = subtag.get('v')
            else:
                if subtag.tag == 'nd':
                    node_refs.append(subtag.get('ref'))
                else:
                    pass
        if node_refs:
            node['node_refs'] = node_refs
        return node
    else:
        return None



def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    data = process_map('houston_texas.osm', False)
    
    
    
    
if __name__ == "__main__":
    test()
