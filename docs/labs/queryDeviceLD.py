'''
SPARQL queries for sensor data
'''

import rdflib
g = rdflib.Graph()

g.parse('./unheardcity/sensor.n3')

#knows_query = """
#SELECT DISTINCT ?name ?blename ?svcname
#WHERE {
#    { ?a uch:mfid ?svcid }
#    { ?svcid uchco:company ?name }
#    { ?a uch:blememberid ?ble }
#    OPTIONAL { ?ble svc:name ?blename}
#    OPTIONAL { ?a uch:svc  ?s }
#    OPTIONAL { ?s svc:name ?svcname} 
#}"""
knows_query = """
SELECT DISTINCT ?name  ?svcname  ?svctype
WHERE {
    { ?a uch:mfid ?svcid }
    { ?svcid uchco:company ?name }
    OPTIONAL { ?a uch:svcuuid ?svc }
    OPTIONAL { ?svc svc:name ?svcname }
    OPTIONAL { ?svc svc:type ?svctype }
    OPTIONAL { ?a uch:devicename ?blename }
}"""

qres = g.query(knows_query)
fh = open("service.csv", "w+")
for row in qres:
    fh.write("{},{},{}\n".format(str(row.name).replace(',', '').replace('  ', ' '), str(row.svcname).replace(',', '').replace('  ', ' '), str(row.svctype)))
    print(f"Device made by {row.name} presents service {row.svcname} with type {row.svctype} ")
fh.close()

#for wifi_name in ['CoventryCC', "CovHolyhead WiFi"]:
knows_query = """
SELECT DISTINCT ?svname ?svctime
    WHERE {
        { ?a  wf:time ?svctime }
        { ?a  wf:name ?svname }
        FILTER (strstarts(str(?svname),'Cov'))
} ORDER BY ?svname ?svctime"""

qres = g.query(knows_query)
wifi = {}
for r in qres:
    row = r.asdict()

    if row['svname'] in wifi:
        wifi[row['svname']].append(int(row['svctime']))
    else:
        wifi[row['svname']] = [int(row['svctime'])]

for k, v in wifi.items():
    _min = min(wifi[k])
    _max = max(wifi[k])

    feature_query = """SELECT DISTINCT ?name ?coname ?svcname
    WHERE {
        { ?a uch:devicename ?name }
        { ?a uch:mfid ?svcid }
        OPTIONAL { ?svcid uchco:company ?coname }
        { ?a  uch:timeseen ?svtime }
        FILTER (?svtime >= """ + str(_min) + """ )
    } ORDER BY ?svname ?svctime"""
    qres = g.query(feature_query)
    for r1 in qres:
        print(f"Device {r1.name} made by {r1.coname} by {r1.svcname} (?) ")