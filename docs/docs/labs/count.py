import rdflib
g = rdflib.Graph()

g.parse('./unheardcity/sensor.n3')


count_query = """
SELECT ?svcid (count( ?svcid) as ?tag)
WHERE {
    { ?a uch:svc  ?s }
    OPTIONAL { ?s svc:name ?svcid} 
} GROUP BY ?svcid"""

qres = g.query(count_query)
for row in qres:
    print(f"{row.svcid} by {row.tag} ")

print('---------------------------')
count_members = """
SELECT ?blename (count( ?blename) as ?tag)
WHERE {
    { ?a uch:mfid ?svcid }
    { ?svcid uchco:company ?blename }
    OPTIONAL { ?a uch:svc  ?s }
    OPTIONAL { ?s svc:name ?svcname}
} GROUP BY ?blename"""

qres = g.query(count_members)
for row in qres:
    print(f"{row.blename} by {row.tag} ")