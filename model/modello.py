from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        pass

    def getAnni(self):
        return DAO.getYears()

    def getForme(self):
        return DAO.getShapes()