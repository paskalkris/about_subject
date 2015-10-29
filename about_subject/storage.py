#!/home/paskal/public/venv python
import rdflib
import rdflib.store as store
from rdflib import Namespace
from rdflib.namespace import FOAF, RDF
from urllib.parse import quote_plus
import base64

class RDFStorage():
    def load_graph(self, store, path, name):
        ident = rdflib.URIRef(name)
        g = rdflib.Graph(store=store, identifier=ident)
        g.open(path, create=True)

        if len(g)==0:
            g.parse("http://xmlns.com/foaf/0.1/")
            g.commit()
            print("A graph has been obtained and loaded.")

        print("graph has %s statements." % len(g))
        return g

    def __init__(self, store="KyotoCabinet", path="rdfstore", name="mystore"):
        self.graph = self.load_graph(store, path, name)

    def close_graph(self):
        self.graph.close()
        return True

    def toRDF(self, string):
        return rdflib.URIRef(string)

    def remove_all(self):
        self.graph.remove((None,None,None))
        self.graph.commit()

    def get_all_subjects(self):
        return sorted(set(self.graph.subjects(None, None)))

    def get_predicates(self, subject=None):
        return sorted(set(self.graph.predicates(subject=self.toRDF(subject))))

    def get_objects(self, subject=None, predicate=None):
        return sorted(set(self.graph.objects(subject=self.toRDF(subject), predicate=self.toRDF(predicate))))

    def get_all_subjects2(self):
        return self.graph.query("""
            SELECT DISTINCT ?p ?o
            WHERE {
                <http://xmlns.com/foaf/0.1/Person> ?p ?o .
            }""")

    def test(self):
        s = self.get_all_subjects()
        ss = self.get_all_subjects2()
        st = 'http://xmlns.com/foaf/0.1/Person'
        tt = base64.b64decode(bytes('aHR0cDovL3htbG5zLmNvbS9mb2FmLzAuMS8=', 'utf-8'))
        p = self.get_predicates(tt.decode('utf-8'))
        for x in p:
            print(x)
        return 
        for x in sorted(set(s)):
            print(x)
        #print(self.graph.serialize(format='nt'))

if __name__=="__main__":
    g = RDFStorage()
    #g.remove()
    g.test()
    g.close_graph()
