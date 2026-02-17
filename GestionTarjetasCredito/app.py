from flask import Flask, render_template, flash
from config import Config
import os


def create_app(config_class=Config):
    """
    Factory function para crear la aplicación Flask
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Asegurar que existe el directorio de la base de datos
    db_dir = os.path.dirname(app.config['DATABASE_PATH'])
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Registrar blueprints
    from routes.routes import tarjetas_bp, movimientos_bp


    app.register_blueprint(tarjetas_bp)
    app.register_blueprint(movimientos_bp)

    # Ruta principal - Dashboard
    @app.route('/')
    def index():
        """
        Página principal / Dashboard
        """
        from services.tarjeta_service import TarjetaService

        try:
            service = TarjetaService()

            tarjetas = service.listar_tarjetas()
            total_tarjetas = len(tarjetas)
            gasto_total = service.calcular_gasto_total_todas()

            # Obtener las últimas 5 tarjetas creadas
            tarjetas_recientes = tarjetas[:5] if len(tarjetas) > 5 else tarjetas

            return render_template(
                'index.html',
                total_tarjetas=total_tarjetas,
                gasto_total=gasto_total,
                tarjetas_recientes=tarjetas_recientes
            )
        except Exception as e:
            flash(f'Error al cargar el dashboard: {str(e)}', 'danger')
            return render_template('index.html', total_tarjetas=0, gasto_total=0, tarjetas_recientes=[])

    # Manejador de errores 404
    @app.errorhandler(404)
    def page_not_found(e):
        """
        Página de error 404 - No encontrado
        """
        return render_template('errors/404.html'), 404

    # Manejador de errores 500
    @app.errorhandler(500)
    def internal_server_error(e):
        """
        Página de error 500 - Error interno del servidor
        """
        return render_template('errors/500.html'), 500

    # Filtro personalizado para formatear moneda
    @app.template_filter('format_currency')
    def format_currency_filter(amount):
        """
        Formatea cantidades como moneda
        Ejemplo: 1234.5 -> 1,234.50€
        """
        return f"{amount:,.2f}€"

    # Filtro personalizado para formatear fechas
    @app.template_filter('format_date')
    def format_date_filter(date_value):
        """
        Formatea fechas de forma legible
        """
        if isinstance(date_value, str):
            from datetime import datetime
            try:
                date_obj = datetime.fromisoformat(date_value)
                return date_obj.strftime('%d/%m/%Y %H:%M')
            except:
                return date_value
        elif hasattr(date_value, 'strftime'):
            return date_value.strftime('%d/%m/%Y %H:%M')
        return str(date_value)


    @app.context_processor
    def utility_processor():
        """
        Funciones disponibles en todos los templates
        """

        def format_nif(nif):
            """Oculta parcialmente el NIF para privacidad"""
            if len(nif) >= 5:
                return nif[:3] + '****' + nif[-1]
            return nif

        return dict(format_nif=format_nif)

    return app


app = create_app()

if __name__ == '__main__':
    """
    Punto de entrada de la aplicación
    Solo se ejecuta si se corre directamente este archivo
    """
    print("=" * 50)
    print("🚀 Iniciando aplicación de Tarjetas de Crédito")
    print("=" * 50)
    print(f"📊 Dashboard: http://127.0.0.1:5000/")
    print(f"💳 Tarjetas: http://127.0.0.1:5000/tarjetas")
    print("=" * 50)

    # Ejecutar la aplicación
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )