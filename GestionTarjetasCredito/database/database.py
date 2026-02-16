import sqlite3
from datetime import datetime


class DataBase:

    def __init__(self, db_name="database/database.db"):
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
                                mes_caducidad TEXT NOT NULL,
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
                                fecha TEXT NOT NULL,
                                FOREIGN KEY (numero_tarjeta) REFERENCES tarjetas_credito (numero_tarjeta) ON DELETE CASCADE
                            )
                            """)
        self.conn.commit()

    def close(self):
        """Cierra la conexión a la base de datos"""
        self.conn.close()


class TarjetaDB:
    def __init__(self, database: DataBase):
        self.db = database

    def insert(self, tarjeta):
        """Inserta una nueva tarjeta en la base de datos"""
        try:
            self.db.cursor.execute("""
                INSERT INTO tarjetas_credito (
                    numero_tarjeta, titular, nif, pin,
                    limite, mes_caducidad, año_caducidad, cvv
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(tarjeta.card_number),
                tarjeta.holder,
                tarjeta.nif,
                tarjeta.pin,
                tarjeta.limit,
                tarjeta.expiration_month,
                tarjeta.expiration_year,
                tarjeta.cvv
            ))
            self.db.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error insertando tarjeta: {e}")
            return False

    def delete(self, numero_tarjeta):
        """Elimina una tarjeta de la base de datos"""
        try:
            self.db.cursor.execute("""
                DELETE FROM tarjetas_credito WHERE numero_tarjeta = ?
            """, (str(numero_tarjeta),))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error eliminando tarjeta: {e}")
            return False

    def update_pin(self, numero_tarjeta, nuevo_pin):
        """Actualiza el PIN de una tarjeta"""
        try:
            self.db.cursor.execute("""
                                   UPDATE tarjetas_credito
                                   SET pin = ?
                                   WHERE numero_tarjeta = ?
                                   """, (nuevo_pin, str(numero_tarjeta)))
            self.db.conn.commit()

            if self.db.cursor.rowcount > 0:
                return True
            else:
                print(f"No se encontró la tarjeta con número {numero_tarjeta}")
                return False
        except sqlite3.Error as e:
            print(f"Error actualizando PIN: {e}")
            return False

    def select_all(self):
        """Obtiene todas las tarjetas"""
        try:
            self.db.cursor.execute("""
                SELECT numero_tarjeta, titular, nif, pin, limite, 
                       mes_caducidad, año_caducidad, cvv 
                FROM tarjetas_credito
            """)
            return self.db.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al hacer el select: {e}")
            return []

    def select_by_nif(self, nif):
        """Obtiene una tarjeta por NIF"""
        try:
            self.db.cursor.execute("""
                SELECT numero_tarjeta, titular, nif, pin, limite, 
                       mes_caducidad, año_caducidad, cvv 
                FROM tarjetas_credito WHERE nif = ?
            """, (nif,))
            return self.db.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al buscar tarjeta por NIF: {e}")
            return None

    def exists_nif(self, nif):
        """Verifica si existe una tarjeta con el NIF dado"""
        try:
            self.db.cursor.execute("""
                SELECT COUNT(*) FROM tarjetas_credito WHERE nif = ?
            """, (nif,))
            count = self.db.cursor.fetchone()[0]
            return count > 0
        except sqlite3.Error as e:
            print(f"Error verificando NIF: {e}")
            return False


class MovimientosDB:
    def __init__(self, database: DataBase):
        self.db = database

    def insert(self, movimiento, numero_tarjeta):
        """Inserta un nuevo movimiento en la base de datos"""
        try:
            fecha_str = movimiento.fecha.isoformat() if isinstance(movimiento.fecha, datetime) else movimiento.fecha
            self.db.cursor.execute("""
                INSERT INTO movimientos (numero_tarjeta, cantidad, concepto, fecha) 
                VALUES (?, ?, ?, ?)""",
                (str(numero_tarjeta), movimiento.cantidad, movimiento.concepto, fecha_str))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error insertando movimiento: {e}")
            return False

    def select_all(self):
        """Obtiene todos los movimientos"""
        try:
            self.db.cursor.execute("""
                SELECT id, numero_tarjeta, cantidad, concepto, fecha 
                FROM movimientos
                ORDER BY fecha DESC
            """)
            return self.db.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al seleccionar todos los movimientos: {e}")
            return []

    def select_by_tarjeta(self, numero_tarjeta):
        """Obtiene todos los movimientos de una tarjeta específica"""
        try:
            self.db.cursor.execute("""
                SELECT id, numero_tarjeta, cantidad, concepto, fecha 
                FROM movimientos 
                WHERE numero_tarjeta = ?
                ORDER BY fecha DESC
            """, (str(numero_tarjeta),))
            return self.db.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al seleccionar movimientos de la tarjeta: {e}")
            return []

    def count_by_tarjeta(self, numero_tarjeta):
        """Cuenta los movimientos de una tarjeta"""
        try:
            self.db.cursor.execute("""
                SELECT COUNT(*) FROM movimientos WHERE numero_tarjeta = ?
            """, (str(numero_tarjeta),))
            return self.db.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error contando movimientos: {e}")
            return 0

    def get_total_gastado(self, numero_tarjeta):
        """Calcula el total gastado de una tarjeta"""
        try:
            self.db.cursor.execute("""
                SELECT SUM(cantidad) FROM movimientos WHERE numero_tarjeta = ?
            """, (str(numero_tarjeta),))
            result = self.db.cursor.fetchone()[0]
            return result if result is not None else 0.0
        except sqlite3.Error as e:
            print(f"Error calculando total gastado: {e}")
            return 0.0