import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def fillLocalization(self):
        localization = self._model.fillLocalization()
        for l in localization:
            self._view.dd_localization.options.append(
                ft.dropdown.Option(l)
            )

    def handle_graph(self, e):
        self._view.txt_result.clean()

        loc1 = self._view.dd_localization.value
        self._model.buildGraph(loc1)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Num nodi: {self._model.getNumNodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"Num Archi: {self._model.getNumEdges()}"))

        archi = self._model.getEdges()
        for u, v, data in archi:
            peso = data["weight"]
            self._view.txt_result.controls.append(ft.Text(f"{u} <-> {v}: peso {peso}"))

        self._view.update_page()

    def analyze_graph(self, e):
        self._view.txt_result.controls.append(ft.Text("Le componenti connesse sono: ", color="green"))

        comp = self._model.getConnectedComponents()
        for geneIDs, dim in comp:
            self._view.txt_result.controls.append(
                ft.Text(f"{', '.join(geneIDs)} | dimensione componente = {dim}")
            )
        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result.clean()

        best, components = self._model.bestPath()

        self._view.txt_result.controls.append(
            ft.Text(f"Soluzione di lunghezza {len(best)} con {components} componenti connesse:", color="green")
        )
        for nodo in best:
            self._view.txt_result.controls.append(
                ft.Text(f"{nodo.GeneID} - {nodo.essenziale}")
            )

        self._view.update_page()