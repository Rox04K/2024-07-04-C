import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        opzioni = self._model.getAnni()

        opzioniDD = list(map(lambda x: ft.dropdown.Option(
            key=x,
            data=x,
            on_click=self.fillDDShape
        ), opzioni))
        self._view.ddyear.options = opzioniDD

    def fillDDShape(self, e):
        anno = self._view.ddyear.value

        opzioni = self._model.getForme(anno)

        opzioniDD = list(map(lambda x: ft.dropdown.Option(x), opzioni))
        self._view.ddshape.options = opzioniDD
        self._view.update_page()

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        if anno == "":
            self._view.create_alert('Attenzione selezionare un anno!')
            return

        forma = self._view.ddshape.value
        if forma == "":
            self._view.create_alert('Attenzione selezionare una forma!')
            return

        self._view.txt_result1.controls.clear()
        self._model.creaGrafo(anno, forma)

        nodi,archi = self._model.getInfo()
        self._view.txt_result1.controls.append(ft.Text(f'Numero di vertici: {nodi}'))
        self._view.txt_result1.controls.append(ft.Text(f'Numero di archi: {archi}'))

        bestArchi = self._model.getBestArchi()
        self._view.txt_result1.controls.append(ft.Text(f'I 5 archi di peso maggiore sono:'))
        for u,v,data in bestArchi:
            self._view.txt_result1.controls.append(ft.Text(f'{u} -> {v} | weight = {data['weight']}'))

        self._view.update_page()

    def handle_path(self, e):
        pass
