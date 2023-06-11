import psycopg2
import utils
TEST = True


class PG:

    #Esta clase pide una db y un usuario para conectarse a PG
    def __init__(self,db_name,owner):
        self.dbname = db_name
        self.user = owner 

    def getConnection(self):
        #esto existe para poder configurar facilmente la coneccion
        return psycopg2.connect(dbname=self.dbname,user=self.user)

    def db_exists(self):
        conn = self.getConnection()
        cur = conn.cursor()

        #mala practica, pero es algo que entiendo mejor!
        query = """SELECT EXISTS (
            SELECT FROM 
                pg_tables
            WHERE 
                schemaname = 'public' AND 
                tablename  = 'textos'
            );"""
        cur.execute(query)
        to_ret = cur.fetchone()
        conn.close()
        return to_ret[0]

    def create_schema(self):
        if self.db_exists():
            print("[INFO] Table exists. Cant Override existing table")
            return
        
        conn = self.getConnection()
        cur = conn.cursor()

        query = """
        CREATE TABLE textos (
            id INTEGER,
            text_body text,
            text_vector tsvector
        );
        """

        cur.execute(query)
        conn.commit()
        conn.close()
        return


    def index_documents(self,documents):
        """
        documents: list of dict-like elements containing a 'text' field to be indexed
        """

        query = """
        INSERT INTO textos VALUES ( %s, %s, NULL);
        """

        # Idea is to create schema and load all the documents into postgres
        if not (self.db_exists()):
            self.create_schema()
        try:
            conn = self.getConnection()
            cur = conn.cursor()
            for i, entry in enumerate(documents):
                cur.execute(query,(i,entry['text']))

            #then have postgres do the tsvector calculation
            cur.execute("UPDATE textos SET text_vector=to_tsvector('spanish',text_body);")
            cur.execute("CREATE INDEX idxTextosText_vectorGin ON textos USING GIN (text_vector);")
            conn.commit()
        except:
            print("[ERROR] Could not insert documents")
            conn.rollback()
        conn.close()
        return




    
    def search_query(self, query, topk):
        """
        query: string; query para la busqueda
        topk: int; numero de documentos de interes

        return value: list of tuples: (id, score)
        """
        query_sql = """
            SELECT id, ts_rank(text_vector, query) AS rank
            FROM textos, to_tsquery('spanish', %s) AS query
            WHERE text_vector @@ query
            ORDER BY rank DESC
            LIMIT %s;
        """
        conn = self.getConnection()
        cur = conn.cursor()

        cur.execute(query_sql,(query,topk))
        print(cur.fetchall())


if TEST:
    docs = utils.read_txt_files("../documents/")
    querier = PG("bd2_proyecto","postgres") #works in my machine. Yours will be different
    querier.search_query("frodo",2)
