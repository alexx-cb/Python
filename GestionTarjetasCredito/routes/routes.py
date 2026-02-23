from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.tarjeta_service import TarjetaService

tarjetas_bp = Blueprint('tarjetas', __name__)
movimientos_bp = Blueprint('movimientos', __name__)

service = TarjetaService()


@tarjetas_bp.route('/tarjetas')
def listar_tarjetas():
    try:
        tarjetas = service.listar_tarjetas()
        return render_template('tarjetas/lista.html', tarjetas=tarjetas)
    except Exception as e:
        flash(f'Error al cargar las tarjetas: {str(e)}', 'danger')
        return redirect(url_for('index'))


@tarjetas_bp.route('/tarjetas/crear', methods=['GET', 'POST'])
def crear_tarjeta():
    """
    GET  → Muestra el formulario de creación
    POST → Procesa los datos del formulario y crea la tarjeta
    """
    if request.method == 'GET':
        return render_template('tarjetas/crear.html')

    if request.method == 'POST':
        try:
            datos = {
                'holder':      request.form.get('holder'),
                'nif':         request.form.get('nif'),
                'pin':         request.form.get('pin'),
                'limit':       request.form.get('limit'),
                'card_number': request.form.get('card_number'),
            }

            service.crear_tarjeta(datos)
            flash('Tarjeta creada correctamente', 'success')
            return redirect(url_for('tarjetas.listar_tarjetas'))

        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('tarjetas/crear.html', datos=request.form)


@tarjetas_bp.route('/tarjetas/<nif>')
def detalle_tarjeta(nif):
    """
    Muestra el detalle y opciones de gestión de una tarjeta concreta
    """
    try:
        tarjeta = service.obtener_tarjeta(nif)

        if tarjeta is None:
            flash('No se encontró ninguna tarjeta con ese NIF', 'warning')
            return redirect(url_for('tarjetas.listar_tarjetas'))

        gasto = service.calcular_gasto_total(nif)
        movimientos = service.obtener_movimientos(nif, 5)  # últimos 5

        return render_template(
            'tarjetas/detalle.html',
            tarjeta=tarjeta,
            gasto=gasto,
            movimientos=movimientos
        )

    except Exception as e:
        flash(f'Error al cargar la tarjeta: {str(e)}', 'danger')
        return redirect(url_for('tarjetas.listar_tarjetas'))


@tarjetas_bp.route('/tarjetas/<nif>/eliminar', methods=['POST'])
def eliminar_tarjeta(nif):
    """
    Elimina una tarjeta y sus movimientos asociados
    Solo acepta POST para evitar eliminaciones accidentales por URL
    """
    try:
        service.eliminar_tarjeta(nif)
        flash(f'Tarjeta eliminada correctamente', 'success')

    except Exception as e:
        flash(f'Error al eliminar la tarjeta: {str(e)}', 'danger')

    return redirect(url_for('tarjetas.listar_tarjetas'))


@tarjetas_bp.route('/tarjetas/<nif>/modificar-pin', methods=['POST'])
def modificar_pin(nif):
    """
    Actualiza el PIN de una tarjeta concreta
    """
    try:
        nuevo_pin = request.form.get('pin')
        service.modificar_pin(nif, nuevo_pin)
        flash('PIN modificado correctamente', 'success')

    except ValueError as e:
        flash(str(e), 'danger')

    return redirect(url_for('tarjetas.detalle_tarjeta', nif=nif))


@movimientos_bp.route('/tarjetas/<nif>/movimientos')
def listar_movimientos(nif):
    """
    Muestra todos los movimientos de una tarjeta
    """
    try:
        tarjeta = service.obtener_tarjeta(nif)

        if tarjeta is None:
            flash('No se encontró ninguna tarjeta con ese NIF', 'warning')
            return redirect(url_for('tarjetas.listar_tarjetas'))

        # Parámetro opcional ?n=10 para limitar movimientos mostrados
        n = request.args.get('n', default=None, type=int)
        movimientos = service.obtener_movimientos(nif, n)

        return render_template(
            'movimientos/lista.html',
            tarjeta=tarjeta,
            movimientos=movimientos
        )

    except Exception as e:
        flash(f'Error al cargar los movimientos: {str(e)}', 'danger')
        return redirect(url_for('tarjetas.listar_tarjetas'))


@movimientos_bp.route('/tarjetas/<nif>/pago', methods=['GET', 'POST'])
def realizar_pago(nif):
    """
    GET  → Muestra el formulario de pago
    POST → Procesa el pago y lo guarda como movimiento
    """
    try:
        tarjeta = service.obtener_tarjeta(nif)

        if tarjeta is None:
            flash('No se encontró ninguna tarjeta con ese NIF', 'warning')
            return redirect(url_for('tarjetas.listar_tarjetas'))

        if request.method == 'GET':
            gasto = service.calcular_gasto_total(nif)
            limite_restante = tarjeta.limit - gasto
            return render_template(
                'movimientos/pago.html',
                tarjeta=tarjeta,
                limite_restante=limite_restante
            )

        if request.method == 'POST':
            cantidad = request.form.get('cantidad')
            concepto = request.form.get('concepto')

            service.realizar_pago(nif, cantidad, concepto)
            flash(f'Pago de {cantidad}€ realizado correctamente', 'success')
            return redirect(url_for('tarjetas.detalle_tarjeta', nif=nif))

    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('movimientos.realizar_pago', nif=nif))

    except Exception as e:
        flash(f'Error al realizar el pago: {str(e)}', 'danger')
        return redirect(url_for('tarjetas.detalle_tarjeta', nif=nif))