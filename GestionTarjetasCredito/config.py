class Config:

    # Clave secreta para sesiones (cambiar en producción)
    SECRET_KEY = 'vsJj1p18i1d3fFV8We1mQPh-w0DF9zqeKIVXDR50dUo'

    # Ruta a la base de datos
    DATABASE_PATH = 'database/database.db'

    # Modo debug activado
    DEBUG = True

    # Constantes de validación
    LIMITE_MIN_TARJETA = 500
    LIMITE_MAX_TARJETA = 5000
    PIN_MIN_DIGITOS = 4