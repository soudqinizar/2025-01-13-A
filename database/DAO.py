from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_classifications():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM classification"""
            cursor.execute(query)

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getLocalization():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(c.Localization )
                        from classification c
                        order by c.Localization desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Localization"], )

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodes(localization):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = query = """select c.GeneID, c.Localization, g.Essential as essenziale
                        from classification c
                        join genes g on g.GeneID = c.GeneID
                        where c.Localization = %s"""
            cursor.execute(query, ( localization, ))

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(localization):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select i.GeneID1, i.GeneID2,
                              sum(distinct g.Chromosome) as peso
                       from interactions i
                       join classification c1 on c1.GeneID = i.GeneID1
                       join classification c2 on c2.GeneID = i.GeneID2
                       join genes g on g.GeneID = i.GeneID1 or g.GeneID = i.GeneID2
                       where c1.Localization = %s
                         and c2.Localization = %s
                         and i.GeneID1 != i.GeneID2
                       group by i.GeneID1, i.GeneID2"""
            cursor.execute(query, (localization, localization))
            for row in cursor:
                result.append((row["GeneID1"], row["GeneID2"], row["peso"]))
            cursor.close()
            cnx.close()
        return result
