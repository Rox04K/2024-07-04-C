import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._IDMap = {}

        self._bestCammino = []
        self._bestPunteggio = 0

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

    def getCamminoOttimo(self):
        self._bestCammino = []
        self._bestPunteggio = 0

        mesi = {i:0 for i in range(1,13)}

        for n in self._grafo.nodes():
            mesi[n.datetime.month] += 1
            parziale = [n]
            self._ricorsione(parziale, mesi)
            mesi[n.datetime.month] -= 1


        return self._bestCammino, self._bestPunteggio

    def _ricorsione(self, parziale, mesi):
        validi = self._getSuccessors(parziale, mesi)
        if validi == []:
            pesoAttuale = self._peso(parziale)
            if pesoAttuale > self._bestPunteggio:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestPunteggio = pesoAttuale

        for n in validi:
            mesi[n.datetime.month] += 1
            parziale.append(n)
            self._ricorsione(parziale, mesi)
            mesi[n.datetime.month] -= 1
            parziale.pop()

    def _getSuccessors(self, parziale, mesi):
        succ = self._grafo.successors(parziale[-1])
        validi = []

        for n in succ:
            if n not in parziale:
                if mesi[n.datetime.month] < 3:
                    if len(parziale) >= 2:
                        if self._grafo[parziale[-1]][n]['weight'] < self._grafo[parziale[-2]][parziale[-1]]['weight']:
                            validi.append(n)
                    else:
                        validi.append(n)

        return validi

    def _peso(self, parziale):
        peso = 100*len(parziale)
        for p in range(len(parziale)-1):
            u= parziale[p]
            v= parziale[p+1]
            if u.datetime.month == v.datetime.month:
                peso += 200
        return peso