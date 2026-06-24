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
        opzioni = self._model.getForme()

        opzioniDD = list(map(lambda x: ft.dropdown.Option(x), opzioni))
        self._view.ddshape.options = opzioniDD
        self._view.update_page()

    def handle_graph(self, e):
        pass

    def handle_path(self, e):
        pass
