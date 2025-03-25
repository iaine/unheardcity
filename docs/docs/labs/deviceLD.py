'''
Map to Sensor data to RDF
'''
from hashlib import md5
from rdflib import Graph, Namespace, Literal, BNode
from rdflib.term import URIRef
import yaml

from deviceLDservices import Service

UCH = Namespace("http://unheardcity.org.uk/")
UCHC = Namespace("http://unheardcity.org.uk/company/")
SD = Namespace("http://unheardcity.org.uk/svc/")

g = Graph()
g.bind("uch", UCH) 
g.bind("svc", SD)
g.bind("uchco", UCHC) 

comps = {}

with open('/Users/iain/git/public/assigned_numbers/company_identifiers/company_identifiers.yaml', 'r') as file:
    prime_service = yaml.safe_load(file)
    for svc in prime_service['company_identifiers']:
        u = URIRef("http://unheardcity.org.uk/company/"+ md5(str(svc['value']).encode('utf-8')).hexdigest())
        g.add((u, UCHC.value, Literal(svc['value'])))
        g.add((u, UCHC.company, Literal(svc['name'])))
        comps[svc['value']] = u

mems = {}
with open('/Users/iain/git/public/assigned_numbers/uuids/member_uuids.yaml', 'r') as file:
    service = yaml.safe_load(file)
    for svc in service['uuids']:
        
        s = URIRef("http://unheardcity.org.uk/member/"+ md5(str(svc['uuid']).encode('utf-8')).hexdigest())
        mems[svc['uuid']] = s
        g.add((s, SD.uuid, Literal(svc['uuid'])))
        g.add((s, SD.name, Literal(svc['name'])))
        g.add((s, SD.type, Literal("member")))

svcs = {}
with open('/Users/iain/git/public/assigned_numbers/uuids/service_uuids.yaml', 'r') as file:
    service = yaml.safe_load(file)
    for svc in service['uuids']:
        
        s = URIRef("http://unheardcity.org.uk/svc/"+ md5(str(svc['uuid']).encode('utf-8')).hexdigest())
        svcs[svc['uuid']] = s
        g.add((s, SD.uuid, Literal(svc['uuid'])))
        g.add((s, SD.name, Literal(svc['name'])))
        g.add((s, SD.type, Literal("service")))


no_device = BNode()
no_maker = BNode()

#fh = open("/Users/iain/Documents/projects/unheard/holyheadroad/A52/bluetoothle_1680540950259.txt", 'r')
fh = open("/Users/iain/Desktop/A52_archive/A52ble.txt", 'r')
data = fh.readlines()
fh.close()


for r in data:
    row = r.split(",")
    #might want to make this more random
    u = URIRef("http://unheardcity.org.uk/"+ md5(row[1].encode('utf-8')).hexdigest())
    g.add((u, UCH.id, Literal(row[1]) ))
    g.add((u, UCH.rssi, Literal( row[2])  ))
    g.add((u, UCH.devicename, Literal(row[6]) ))
    g.add((u, UCH.tx, Literal( row[8])   ))
    
    comp = ""
    if row[10] != ' ' and row[10] != '' and not row[10].startswith(' No') and int(row[10]) in comps: 
        comp = comps[int(row[10])]
    else:
        comp = no_maker

    g.add((u, UCH.mfid, URIRef(comp) ))

    service = Service(svcuuid=mems, svcs=svcs)
    blank = row[12].strip()
    print(row)
    print(blank)
    if row[12] == '': print(row[13])
    #if row[12] == "":
    #    blank = row[13]

    if ';' in blank:
        s_row = blank.split(';')      
        for mr in s_row:
            _m = service.find_services_uuid(mr.strip())
            _s = service.find_services(mr.strip())
            print(f"fg: {_m}:{_s}")
            if  _m != "":
                print(f"fhhg: {_m}:{_s}")
                g.add((u, UCH.svcuuid,URIRef(mems[_m]) ))
            elif _s != '': 
                print(f"fjjhg: {_m}:{_s}")
                g.add((u, UCH.svcuuid,URIRef(str(svcs[_s]) )))
            else:
                new_svc = URIRef("http://unheardcity.org.uk/svc/"+ md5(mr[4:8].encode('utf-8')).hexdigest())
                g.add((new_svc, SD.uuid, Literal(mr[4:8])))
                g.add((u, UCH.svcuuid,URIRef(new_svc)))
                g.add((new_svc, SD.type, Literal("custom")))
    else:
        _mems = service.find_services_uuid(blank)
        _svc = service.find_services(blank)
        if _mems != '': 
            g.add((u, UCH.svcuuid,URIRef(str(mems[_mems]) )))
        elif _svc != '': 
            g.add((u, UCH.svcuuid,URIRef(str(svcs[_svc]) )))
        else:
            g.add((u, UCH.svcuuid, URIRef(no_device) ))
    
    g.add((u, UCH.svcdata, Literal(row[14].strip()) ))
    g.add( (u, UCH.timeseen, Literal(row[0])) )

#WiFi
WI = Namespace("http://unheardcity.org.uk/wifi/")
g.bind("wf", WI)

fh1 = open("/Users/iain/Documents/projects/unheard/holyheadroad/A52/wifi_1680540950259.txt", 'r')
data= fh1.readlines()
fh1.close()

for datum in data:
    d = datum.split(',')
    if len(d) > 2:
        u = URIRef("http://unheardcity.org.uk/"+ md5(d[1].encode('utf-8')).hexdigest())
        g.add((u, WI.id, Literal(u) ))
        g.add((u, WI.time, Literal(d[0]) ))
        g.add((u, WI.name, Literal(d[1]) ))
        g.add((u, WI.decibel, Literal(d[4]) ))
        g.add((u, WI.ranging, Literal(d[3]) ))

g.serialize("A52sensor.n3", format="n3")