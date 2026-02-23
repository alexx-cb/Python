from models.movimiento import Movimiento
from models.tarjeta_credito import TarjetaCredito
from database.database import DataBase, TarjetaDB, MovimientosDB


class TarjetaService:
    def __init__(self):
        self.db = DataBase()
        self.tarjeta_db = TarjetaDB(self.db)
        self.movimiento_db = MovimientosDB(self.db)


    """
    ----------------------------------------
    TARJETAS
    ----------------------------------------
    """

    def listar_tarjetas(self) -> list[TarjetaCredito]:
        rows = self.tarjeta_db.select_all()

        tarjetas = []
        for row in rows:
            movimientos = self._cargar_movimientos(row[0])
            tarjeta = TarjetaCredito.from_db_row(row, movimientos)
            tarjetas.append(tarjeta)

        return tarjetas

    def obtener_tarjeta(self, nif: str) -> TarjetaCredito | None:
        row = self.tarjeta_db.select_by_nif(nif)

        if row is None:
            return None

        movimientos = self._cargar_movimientos(row[0])
        return TarjetaCredito.from_db_row(row, movimientos)

    def crear_tarjeta(self, data:dict) -> TarjetaCredito:
        campos = ["holder","nif" ,"pin", "limit" ,"card_number"]

        for campo in campos:
            if not data.get(campo):
                raise ValueError(f"El campo {campo} es obligatorio")

        if self.tarjeta_db.exists_nif(data["nif"]):
            raise ValueError(f"Ya existe una tarjeta de credito asociada al nif:  {data['nif']}")

        try:
            pin = int(data["pin"])
            limit = int(data["limit"])
            card_number = int(data["card_number"])
        except ValueError:
            raise ValueError("pin, limit y card_number deben ser numericos")


        tarjeta = TarjetaCredito(
            holder=data["holder"],
            nif=data["nif"],
            pin=pin,
            limit=limit,
            card_number=card_number
        )

        self.tarjeta_db.insert(tarjeta)

        return tarjeta


    def eliminar_tarjeta(self, nif:str) -> bool:

        if not self.tarjeta_db.exists_nif(nif):
            raise ValueError(f"No existe ninguna tarjeta asociada al nif: {nif}")

        row = self.tarjeta_db.select_by_nif(nif)
        numero_tarjeta = row[0]

        return self.tarjeta_db.delete(numero_tarjeta)



    def modificar_pin(self, nif:str, nuevo_pin:int) -> bool:
        if not self.tarjeta_db.exists_nif(nif):
            raise ValueError(f"No existe tarjeta asociada al nif: {nif}")

        row = self.tarjeta_db.select_by_nif(nif)
        numero_tarjeta = row[0]

        return self.tarjeta_db.update_pin(numero_tarjeta, nuevo_pin)


    """
    -----------------------------
    MOVIMIENTOS
    -----------------------------
    """

    def realizar_pago(self, nif:str, cantidad:str, concepto:str)->Movimiento:

        tarjeta = self.obtener_tarjeta(nif)

        if tarjeta is None:
            raise ValueError(f"No existe tarjeta asociada al nif {nif}")

        try:
            cantidad = float(cantidad)
        except (ValueError, TypeError):
            raise ValueError(f"El cantidad debe ser numericos")

        tarjeta.pagar(cantidad, concepto)

        movimiento = tarjeta.movements[-1]
        self.movimiento_db.insert(movimiento, tarjeta.card_number)

        return movimiento


    def obtener_movimientos(self, nif:str, n: int = None) -> list[Movimiento]:

        tarjeta = self.obtener_tarjeta(nif)

        if tarjeta is None:
            raise ValueError(f"No existe tarjeta asociada al nif {nif}")

        total = tarjeta.numero_movimientos()

        if total == 0:
            return []

        n = n if n is not None and 0 <= n <= total else total
        return tarjeta.movimientos(n)


    """
    --------------------------
    GASTOS
    --------------------------
    """

    def calcular_gasto_total(self, nif:str) -> float:
        tarjeta = self.obtener_tarjeta(nif)

        if tarjeta is None:
            raise ValueError(f"No existe tarjeta asociada al nif {nif}")

        return tarjeta.gastado()


    def calcular_gasto_total_todas(self)->float:

        tarjetas = self.listar_tarjetas()
        return sum(tarjeta.gastado() for tarjeta in tarjetas)

    def _cargar_movimientos(self, numero_tarjeta) -> list[Movimiento]:
        rows = self.movimiento_db.select_by_tarjeta(numero_tarjeta)

        return [
            Movimiento(
                cantidad=row[2],
                concepto=row[3],
                fecha=row[4]
            )
            for row in rows
        ]


