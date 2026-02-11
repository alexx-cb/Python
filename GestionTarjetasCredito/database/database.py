import sqlite3


class DataBase:

    def __init__(self, db_name="database.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        self.cursor.execute(""" 
                            CREATE TABLE IF NOT EXISTS tarjetas_credito (
                                numero_tarjeta TEXT PRIMARY KEY,
                                titular TEXT NOT NULL,
                                nif TEXT NOT NULL UNIQUE,
                                pin INTEGER NOT NULL,
                                limite REAL NOT NULL,
                                mes_caducidad INTEGER NOT NULL,
                                año_caducidad INTEGER NOT NULL,
                                cvv INTEGER NOT NULL
                            )
                            """)

        # Tabla movimientos
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS movimientos (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                numero_tarjeta TEXT NOT NULL,
                                cantidad REAL NOT NULL,
                                concepto TEXT NOT NULL,
                                fecha TIMESTAMP,
                                FOREIGN KEY (numero_tarjeta) REFERENCES tarjetas_credito (numero_tarjeta)
                            )
                            """)
        self.conn.commit()


class TarjetaDB:
    def __init__(self, database: DataBase):
        self.db = database


    def insert(self, tarjeta):
        try:
            self.db.cursor.execute("""
                INSERT INTO tarjetas_credito (
                    numero_tarjeta, titular, nif, pin,
                    limite, mes_caducidad, año_caducidad, cvv
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tarjeta.numero_tarjeta,
                tarjeta.titular,
                tarjeta.nif,
                tarjeta.pin,
                tarjeta.limite,
                tarjeta.mes_caducidad,
                tarjeta.año_caducidad,
                tarjeta.cvv
            ))
            self.db.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error insertando tarjeta: {e}")


    def delete(self, tarjeta):
        try:
            self.db.cursor.execute("""
                DELETE FROM tarjetas_credito WHERE numero_tarjeta = ?
            
            """, tarjeta.numero_tarjeta)
            self.db.conn.commit()

        except sqlite3.IntegrityError as e:
            print(f"Error eliminando tarjeta: {e}")


    def patch(self, tarjeta):
        try:
            self.db.cursor.execute("""
                UPDATE tarjetas_credito SET pin = ? WHERE numero_tarjeta = ?
            """, (tarjeta.pin, tarjeta.numero_tarjeta))
            self.db.conn.commit()

        except sqlite3.IntegrityError as e:
            print(f"Error Actualizando la tarjeta tarjeta: {e}")


    def select_all(self):
        try:
            self.db.cursor.execute("""
                SELECT * FROM tarjetas_credito
            """)


        except sqlite3.IntegrityError as e:
            print(f"Error al hacer el select: {e}")

    def select_tarjeta_nif(self, tarjeta):
        try:
            self.db.cursor.execute("""
            SELECT * FROM tarjetas_credito WHERE nif = ?
            """, tarjeta.nif)

        except sqlite3.IntegrityError as e:
            print(f"Error al hacer el select de la tajeta con nif {tarjeta.nif}: {e}")