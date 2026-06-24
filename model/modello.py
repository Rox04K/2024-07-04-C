from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._IDMap = {}

        self._bestCammino = []
        self._bestLunghezza = 0

    def getAnni(self):
        return DAO.getYears()

    def getForme(self, anno):
        return DAO.getShapes(anno)

    def creaGrafo(self, anno, forma):
        self._grafo.clear()
        self._IDMap = {}

        nodi = DAO.getNodi(anno, forma)
        self._grafo.add_nodes_from(nodi)
        for n in nodi:
            self._IDMap[n.id] = n

        archi = DAO.getArchi(anno, forma, self._IDMap)

        for a in archi:
            u = a[0]
            v = a[1]

            if u.longitude > v.longitude:
                peso = u.longitude - v.longitude
                self._grafo.add_edge(v, u, weight=peso)
            elif u.longitude < v.longitude:
                peso = v.longitude - u.longitude
                self._grafo.add_edge(u, v, weight=peso)

    def getInfo(self):
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def getBestArchi(self):
        archi_ordinati = sorted(self._grafo.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
        return archi_ordinati[:5]

    ''' METODO DI RICORSIONE '''

    def getCammino(self):
        # Prima di tutto bisogna reimpostare i valori della ricorsione a 0 perchè così non salviamo valori vecchi
        self._bestCammino = []
        self._bestLunghezza = 0

        # Poi prepariamo la base della ricorsione. Ci sono diversi tipi di ricorsione che vengono trattati nella parte apposita
        parziale = []

        for n in self._grafo.nodes():
            parziale.append(n)
            self.ricorsione(parziale)
            parziale.pop()

        return self._bestCammino, (self._bestLunghezza - 1)

    def ricorsione(self, parziale):
        # Qui scriviamo il metodo ricorsivo
        pass

