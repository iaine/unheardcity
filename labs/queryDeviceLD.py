'''
SPARQL queries for sensor data
'''

import rdflib
g = rdflib.Graph()

g.parse('./unheardcity/sensor.n3')

knows_query = """
SELECT DISTINCT ?svcid ?name ?blname
WHERE {
     {?a uch:mfid ?svcid }
    {?svcid uchco:company ?name }
   { ?a uch:blememberid ?ble }
    {?ble uchco:company ?blname }
    UNION
    {?ble svc:id ?blename}
    
}"""

qres = g.query(knows_query)
for row in qres:
    print(f"{row.svcid} made by {row.name} uses {row.blname} ")