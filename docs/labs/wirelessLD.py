'''
Map to Wireless data to RDF
'''
from hashlib import md5
from rdflib import Graph, Namespace, Literal, BNode
from rdflib.term import URIRef

fh = open("/Users/iain/Desktop/hh4_aist/A52/A52wifi.txt", 'r')
data = fh.readlines()
fh.close()
fh = open("/Users/iain/Desktop/hh4_aist/A51/A51wifi.txt", 'r')
data += fh.readlines()
fh.close()
fh = open("/Users/iain/Desktop/hh4_aist/zte/ztewifi.txt", 'r')
data += fh.readlines()
fh.close()

UCH = Namespace("http://unheardcity.org.uk/")
WI = Namespace("http://unheardcity.org.uk/wifi/")

g = Graph()
g.bind("uch", UCH) 
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

g.serialize("wireless.n3", format="n3")
