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
                    if n.duration > parziale[-1].duration:
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

    def cammino_ottimo(self):
        self._cammino_ottimo = []
        self._score_ottimo = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)

        for nodo in self._grafo.nodes():
            self._occorrenze_mese[nodo.datetime.month] += 1
            successivi_durata_crescente = self._calcola_successivi(nodo)
            self._calcola_cammino_ricorsivo([nodo], successivi_durata_crescente)
            self._occorrenze_mese[nodo.datetime.month] -= 1
        return self._cammino_ottimo, self._score_ottimo

    def _calcola_cammino_ricorsivo(self, parziale, successivi):
        if len(successivi) == 0:
            score = Model._calcola_score(parziale)
            if score > self._score_ottimo:
                self._score_ottimo = score
                self._cammino_ottimo = copy.deepcopy(parziale)
        else:
            for nodo in successivi:
                # aggiungo il nodo in parziale ed aggiorno le occorrenze del mese corrispondente
                parziale.append(nodo)
                self._occorrenze_mese[nodo.datetime.month] += 1
                # nuovi successivi
                nuovi_successivi = self._calcola_successivi(nodo)
                # ricorsione
                self._calcola_cammino_ricorsivo(parziale, nuovi_successivi)
                # backtracking: visto che sto usando un dizionario nella classe per le occorrenze, quando faccio il
                # backtracking vado anche a togliere una visita dalle occorrenze del mese corrispondente al nodo che
                # vado a sottrarre
                self._occorrenze_mese[parziale[-1].datetime.month] -= 1
                parziale.pop()

    def _calcola_successivi(self, nodo):
        """
        Calcola il sottoinsieme dei successivi ad un nodo che hanno durata superiore a quella del nodo e che non eccedano
        il numero massimo di occorrenze per un dato mese.
        """
        successivi = self._grafo.successors(nodo)
        successivi_ammissibili = []
        for s in successivi:
            if s.duration > nodo.duration and self._occorrenze_mese[s.datetime.month] < 3:
                successivi_ammissibili.append(s)
        return successivi_ammissibili

    @staticmethod
    def _calcola_score(cammino) -> int:
        """
        Funzione che calcola il punteggio di un cammino.
        :param cammino: il cammino che si vuole valutare.
        :return: il punteggio
        """
        # parte del punteggio legata al numero di tappe
        score = 100 * len(cammino)
        # parte del punteggio legata al mese
        for i in range(1, len(cammino)):
            if cammino[i].datetime.month == cammino[i - 1].datetime.month:
                score += 200
        return score