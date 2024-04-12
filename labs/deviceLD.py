'''
Map to Sensor data to RDF
'''
from hashlib import md5
from rdflib import Graph, Namespace, Literal, BNode
from rdflib.term import URIRef
import yaml

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
        mems[svc['uuid']] = u
        s = URIRef("http://unheardcity.org.uk/"+ md5(str(svc['uuid']).encode('utf-8')).hexdigest())
        g.add((s, SD.uuid, Literal(svc['uuid'])))
        g.add((s, SD.name, Literal(svc['name'])))

svcs = {}
with open('/Users/iain/git/public/assigned_numbers/uuids/service_uuids.yaml', 'r') as file:
    service = yaml.safe_load(file)
    for svc in service['uuids']:
        svcs[svc['uuid']] = u
        s = URIRef("http://unheardcity.org.uk/"+ md5(str(svc['uuid']).encode('utf-8')).hexdigest())
        g.add((s, SD.uuid, Literal(svc['uuid'])))
        g.add((s, SD.name, Literal(svc['name'])))


no_device = BNode()

fh = open("/Users/iain/Documents/projects/unheard/holyheadroad/A52/bluetoothle_1680540950259.txt", 'r')
data = fh.readlines()
fh.close()

for r in data:
    row = r.split("\t")
    #might want to make this more random
    u = URIRef("http://unheardcity.org.uk/"+ md5(row[1].encode('utf-8')).hexdigest())
    g.add((u, UCH.id, Literal(row[1]) ))
    g.add((u, UCH.rssi, Literal( row[2])  ))
    g.add((u, UCH.devicename, Literal(row[6]) ))
    g.add((u, UCH.tx, Literal( row[8])   ))
    
    comp = ""
    if row[10] != ' ' and row[10] != '' and int(row[10]) in comps: 
        comp = comps[int(row[10])]
    else:
        comp = BNode()

    g.add((u, UCH.mfid, URIRef(comp) ))

    # now to create services
    r = row[12].strip()[4:8]

    if ';' in row[12]:
        s_row = row[12].split(';')
        for mr in s_row:
            if int(mr[4:8].strip(), base=16) in svcs:
                g.add((u, UCH.blememberid,URIRef(svcs[mr[4:8].strip()]) ))
            else:
                new_svc = URIRef("http://unheardcity.org.uk/svc/"+ md5(mr[4:8].encode('utf-8')).hexdigest())
                g.add((new_svc, SD.uuid, Literal(mr[4:8])))
                g.add((u, UCH.blememberid,URIRef(new_svc)))
    elif r != 'ervi' and r != '' and int(r, base=16) in mems: 
        g.add((u, UCH.blememberid,URIRef(mems[int(r, base=16)])))
    elif r != 'ervi' and r != '' and int(r, base=16) in svcs: 
        g.add((u, UCH.blememberid,URIRef(svcs[int(r, base=16)])))
    else:
        g.add((u, UCH.blememberid, URIRef(no_device) ))

    g.add((u, UCH.blesvcid, Literal(row[13]) ))

g.serialize("sensor.n3", format="n3")