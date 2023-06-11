import psycopg2

class PG:

    #Esta clase pide una db y un usuario para conectarse a PG
    def __init__(self,db_name,owner):
        self.dbname = db_name
        self.user = owner
    
    def search_query(self, query, topk)
        """
        query: string; query para la busqueda
        topk: int; numero de documentos de interes
        """

        cur = psycopg2.connect(dbname=self.dbname,user=self.user)

        cur.

    