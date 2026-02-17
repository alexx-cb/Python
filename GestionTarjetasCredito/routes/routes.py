from flask import Blueprint, render_template, request, redirect, url_for, flash

from services.tarjeta_service import TarjetaService

tarjetas_bp = Blueprint('tarjetas', __name__)
movimientos_bp = Blueprint('movimientos', __name__)

service = TarjetaService()


@tarjetas_bp.route('/tarjetas')
def listar_tarjetas():
    try:
        tarjetas = service.listar_tarjetas()
        return render_template('tarjetas/listar.html', tarjetas=tarjetas)

    except Exception as e:
        flash(f"Error al cargar las tarjetas")