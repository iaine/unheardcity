'''
SPARQL queries for sensor data by wiFi
'''

import rdflib
g = rdflib.Graph()

g.parse('./unheardcity/sensor.n3')
g.parse('./unheardcity/wireless.n3')

knows_query = """
SELECT DISTINCT ?svcid ?name ?blename ?svcname
WHERE {
    { ?a uch:mfid ?svcid }
    { ?svcid uchco:company ?name }
    { ?a uch:blememberid ?ble }
    { ?ble svc:name ?blename}
    OPTIONAL { ?a uch:svc  ?s }
    OPTIONAL { ?s svc:name ?svcname} 
}"""

qres = g.query(knows_query)
for row in qres:
    if row.svcname != "":
        print(f"{row.svcid} made by {row.name} uses service {row.svcname} by {row.blename} (?) ")
    else:
        print(f"{row.svcid} made by {row.name} related to {row.blename} (?) ")