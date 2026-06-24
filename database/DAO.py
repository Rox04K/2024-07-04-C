from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(datetime) as anno
                        from sighting s 
                        order by datetime desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row['anno'])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getShapes(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct shape
                        from sighting s 
                        where shape != ""
                        and year(datetime) = %s
                        order by shape asc"""
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(row['shape'])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodi(anno, forma):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                        from sighting s 
                        where shape = %s
                        and year(datetime) = %s """
            cursor.execute(query, (forma, anno,))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getArchi(anno, forma, mappa):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """with nodi as(
                        select *
                        from sighting s 
                        where shape = %s
                        and year(datetime) = %s)
                        select n1.id as a1, n2.id as a2
                        from nodi n1, nodi n2
                        where n1.id > n2.id
                        and n1.state = n2.state"""
            cursor.execute(query, (forma, anno,))

            for row in cursor:
                result.append((mappa[row['a1']], mappa[row['a2']]))
            cursor.close()
            cnx.close()
        return result