from hashlib import md5
from rdflib import Graph, Namespace, Literal, BNode
from rdflib.term import URIRef

class Service():

    def __init__(self, svcuuid, svcs) -> None:
        self.svcs = svcs
        self.svcuuid = svcuuid

    def find_services(self, serviceid):
        if serviceid.strip().startswith("No") or serviceid == '':
            return ""
        else:
            test_svc = int(serviceid[4:8].strip(), base=16)
            if test_svc in self.svcs:
                return test_svc
            else:
                return ""
        
    def find_services_uuid(self, serviceid):

        if serviceid.strip().startswith("No") or serviceid == '':
            return ""
        else:
            test_svc = int(str(serviceid[4:8]), base=16)

            if test_svc in self.svcuuid:
                return test_svc
            else:
                return ""