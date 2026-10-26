from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    def get_umidita_media(mese):
        cnx = DBConnect.get_connection()

        result = []
        query = """select s.Localita, avg(s.Umidita)
                    from situazione s
                    where month(s.data) = %s 
                    group by s.localita"""

        if cnx is not None:
            cursor = cnx.cursor()

            cursor.execute(query, (mese,))
            result = cursor.fetchall()
            cursor.close()
            cnx.close()
            return result
        else:
            print("Connessione fallita")
            return None

    def get_situazioni_meta_mese(mese):
        cnx = DBConnect.get_connection()
        result = []
        query = """select s.Localita, s.Data, s.Umidita
                    from situazione s
                    where month(s.data) = %s 
                    and day(s.data) <= 15
                    order by s.Data ASC      
                    """

        if cnx is not None:
            cursor = cnx.cursor(dictionary=True)
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()

        return result