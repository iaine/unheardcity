'''
SPARQL queries for sensor data
'''
import csv 
import rdflib

g = rdflib.Graph()

g.parse('./unheardcity/A52sensor.n3')

knows_query = """
SELECT  ?name ?type ?id
WHERE {
    { ?a uch:mfid ?svcid }
    { ?a uch:id ?id }
    OPTIONAL { ?svcid uchco:company ?name }
    OPTIONAL { ?a uch:svcuuid ?svc }
    OPTIONAL { ?svc svc:name ?type } 
} 

"""
#knows_query = """
#SELECT DISTINCT ?name  ?svcname  ?svctype
#WHERE {
#   { ?a uch:mfid ?svcid }
#   { ?svcid uchco:company ?name }
#    OPTIONAL { ?a uch:svcuuid ?svc }
#    OPTIONAL { ?svc svc:name ?svcname }
#    OPTIONAL { ?svc svc:type ?svctype }
#    OPTIONAL { ?a uch:devicename ?blename }
#}"""

qres = g.query(knows_query)
fh = open("service.csv", "w+")
for row in qres:
    w = csv.writer(fh, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    w.writerow([row.id, row.name, row.type])
    #fh.write("{},{},{}\n".format(str(row.id).replace(',', '').replace('  ', ' '), str(row.name).replace(',', '').replace('  ', ' '), str(row.type)))
    #print(f"Device {row.id} made by {row.name} presents service {row.type} ")
fh.close()

wifi_query = """
SELECT  ?name ?decibel
WHERE {
    { ?a wf:name ?name }
    { ?a wf:decibel ?decibel }
} 
"""
res = g.query(wifi_query)
fh = open("wifi.csv", "w+")
for row in res:
    w = csv.writer(fh, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    w.writerow([row.name, row.decibel])
    #fh.write("{},{},{}\n".format(str(row.id).replace(',', '').replace('  ', ' '), str(row.name).replace(',', '').replace('  ', ' '), str(row.type)))
    print(f"Device made by {row.name} sound level {row.decibel} ")
fh.close()