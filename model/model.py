import copy
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapClassification = {}
        self._best = []
        self._bestComponents = None

    def buildGraph(self, loc1):
        self._graph.clear()
        classificazioni = DAO.getNodes(loc1)
        self._graph.add_nodes_from(classificazioni)
        self._idMapClassification = {c.GeneID: c for c in classificazioni}

        archi = DAO.getEdges(loc1)
        for gid1, gid2, peso in archi:
            if gid1 in self._idMapClassification and gid2 in self._idMapClassification:
                self._graph.add_edge(
                    self._idMapClassification[gid1],
                    self._idMapClassification[gid2],
                    weight=peso
                )

    def fillLocalization(self):
        return DAO.getLocalization()

    def getNumNodes(self):
        return len(self._graph.nodes())

    def getNumEdges(self):
        return len(self._graph.edges())

    def getEdges(self):
        archi = list(self._graph.edges(data=True))
        return sorted(archi, key=lambda e: e[2]["weight"])

    def getConnectedComponents(self):
        components = list(nx.connected_components(self._graph))
        components = [c for c in components if len(c) > 1]
        components = sorted(components, key=len, reverse=True)

        result = []
        for c in components:
            geneIDs = sorted(n.GeneID for n in c)
            result.append((geneIDs, len(c)))
        return result

    def bestPath(self):
        # nodi divisi per essenzialità, esclusi i "?"
        essential = [n for n in self._graph.nodes() if n.essenziale == "Essential"]
        non_essential = [n for n in self._graph.nodes() if n.essenziale == "Non-Essential"]

        self._best = []
        self._bestComponents = None

        # esploro ciascun gruppo separatamente: dentro un gruppo il vincolo II è garantito
        for gruppo in (essential, non_essential):
            gruppo = sorted(gruppo, key=lambda n: n.GeneID)
            self.ricorsione([], 0, gruppo)

        return self._best, self._bestComponents

    def ricorsione(self, parziale, start, gruppo):
        self.valuta(parziale)

        for i in range(start, len(gruppo)):
            # pruning: se anche prendendo tutti i nodi rimanenti non supero il best, taglio
            nodi_rimanenti = len(gruppo) - i
            if len(parziale) + nodi_rimanenti < len(self._best):
                break
            parziale.append(gruppo[i])
            self.ricorsione(parziale, i + 1, gruppo)
            parziale.pop()

    def valuta(self, parziale):
        if len(parziale) == 0:
            return

        # numero di componenti connesse del sottografo indotto dai nodi scelti
        sub = self._graph.subgraph(parziale)
        numComp = nx.number_connected_components(sub)

        migliore = False
        if len(parziale) > len(self._best):
            migliore = True
        elif len(parziale) == len(self._best) and self._bestComponents is not None and numComp < self._bestComponents:
            migliore = True

        if migliore:
            self._best = sorted(copy.copy(parziale), key=lambda n: n.GeneID)
            self._bestComponents = numComp