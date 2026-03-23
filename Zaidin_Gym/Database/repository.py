from datetime import date
from sqlalchemy.orm import Session

from Class.actividad import Actividad
from Class.especialidad import Especialidad
from Class.monitor import Monitor
from Class.socio import Socio
from Class.socio_premium import SocioPremium
from Database.models import (UsuarioModel, SocioModel, SocioPremiumModel,
                              MonitorModel, ActividadModel, VotoModel,
                              SocioActividadModel, MonitorEspecialidadModel)


# ==============================================================
#  ACTIVIDADES
# ==============================================================

def crear_actividad(session: Session, actividad: Actividad) -> ActividadModel:
    modelo = ActividadModel(
        nombre=actividad.nombre,
        duracion=actividad.duracion,
        calorias=actividad.calorias,
        categoria=actividad.categoria.value,
        es_premium=actividad.es_premium
    )
    session.add(modelo)
    session.commit()
    session.refresh(modelo)
    return modelo


def obtener_actividades(session: Session) -> list[Actividad]:
    modelos = session.query(ActividadModel).all()
    return [_modelo_a_actividad(session, m) for m in modelos]


def obtener_actividad_por_nombre(session: Session, nombre: str) -> Actividad | None:
    modelo = session.query(ActividadModel).filter(
        ActividadModel.nombre.ilike(nombre)
    ).first()
    return _modelo_a_actividad(session, modelo) if modelo else None


def eliminar_actividad(session: Session, nombre: str) -> bool:
    modelo = session.query(ActividadModel).filter(
        ActividadModel.nombre.ilike(nombre)
    ).first()
    if not modelo:
        return False
    session.delete(modelo)
    session.commit()
    return True


def votar_actividad(session: Session, nombre: str, voto: int) -> bool:
    modelo = session.query(ActividadModel).filter(
        ActividadModel.nombre.ilike(nombre)
    ).first()
    if not modelo or not (0 <= voto <= 10):
        return False
    session.add(VotoModel(actividad_id=modelo.id, voto=voto))
    session.commit()
    return True


def actividad_tiene_socios(session: Session, nombre: str) -> list[str]:
    """Devuelve lista de nombres de socios que tienen la actividad"""
    modelo = session.query(ActividadModel).filter(
        ActividadModel.nombre.ilike(nombre)
    ).first()
    if not modelo:
        return []
    socios_nombres = []
    for sa in modelo.socios:
        socio_model = session.get(SocioModel, sa.socio_id)
        if socio_model:
            socios_nombres.append(socio_model.nombre)
    return socios_nombres


# ==============================================================
#  USUARIOS (SOCIOS Y MONITORES)
# ==============================================================

def crear_socio(session: Session, socio: Socio) -> SocioModel:
    modelo = SocioModel(
        nombre=socio.nombre,
        dni=socio.dni,
        direccion=socio.direccion,
        provincia=socio.provincia,
        codigo_postal=socio.codigo_postal,
        telefono=socio.telefono,
        fecha_nacimiento=socio.fecha_nacimiento,
        fecha_registro=socio.fecha_registro,
        fecha_ultimo_acceso=socio.fecha_ultimo_acceso,
        esta_activo=socio.esta_activo,
        cuota=socio.cuota
    )
    session.add(modelo)
    session.flush()

    for actividad in socio.lista_actividades:
        act_model = session.query(ActividadModel).filter(
            ActividadModel.nombre.ilike(actividad.nombre)
        ).first()
        if act_model:
            session.add(SocioActividadModel(socio_id=modelo.id, actividad_id=act_model.id))

    session.commit()
    session.refresh(modelo)
    return modelo


def crear_socio_premium(session: Session, socio: SocioPremium) -> SocioPremiumModel:
    modelo = SocioPremiumModel(
        nombre=socio.nombre,
        dni=socio.dni,
        direccion=socio.direccion,
        provincia=socio.provincia,
        codigo_postal=socio.codigo_postal,
        telefono=socio.telefono,
        fecha_nacimiento=socio.fecha_nacimiento,
        fecha_registro=socio.fecha_registro,
        fecha_ultimo_acceso=socio.fecha_ultimo_acceso,
        esta_activo=socio.esta_activo,
        cuota=socio.cuota,
        es_premium=True
    )
    session.add(modelo)
    session.flush()

    for actividad in socio.lista_actividades:
        act_model = session.query(ActividadModel).filter(
            ActividadModel.nombre.ilike(actividad.nombre)
        ).first()
        if act_model:
            session.add(SocioActividadModel(socio_id=modelo.id, actividad_id=act_model.id))

    session.commit()
    session.refresh(modelo)
    return modelo


def crear_monitor(session: Session, monitor: Monitor) -> MonitorModel:
    modelo = MonitorModel(
        nombre=monitor.nombre,
        dni=monitor.dni,
        direccion=monitor.direccion,
        provincia=monitor.provincia,
        codigo_postal=monitor.codigo_postal,
        telefono=monitor.telefono,
        fecha_nacimiento=monitor.fecha_nacimiento,
        sueldo=monitor.sueldo,
        votos_positivos=monitor.votos_positivos,
        votos_negativos=monitor.votos_negativos,
    )
    session.add(modelo)
    session.flush()

    for esp in monitor.especialidad:
        session.add(MonitorEspecialidadModel(monitor_id=modelo.id, especialidad=esp.value))

    session.commit()
    session.refresh(modelo)
    return modelo


def obtener_usuarios(session: Session) -> list[Socio | SocioPremium | Monitor]:
    modelos = session.query(UsuarioModel).all()
    return [_modelo_a_usuario(session, m) for m in modelos if m is not None]


def obtener_usuario_por_dni(session: Session, dni: str) -> Socio | SocioPremium | Monitor | None:
    modelo = session.query(UsuarioModel).filter(UsuarioModel.dni == dni).first()
    return _modelo_a_usuario(session, modelo) if modelo else None


def obtener_usuario_por_nombre(session: Session, nombre: str) -> Socio | SocioPremium | Monitor | None:
    modelo = session.query(UsuarioModel).filter(
        UsuarioModel.nombre.ilike(f"%{nombre}%")
    ).first()
    return _modelo_a_usuario(session, modelo) if modelo else None


def eliminar_usuario(session: Session, dni: str) -> bool:
    modelo = session.query(UsuarioModel).filter(UsuarioModel.dni == dni).first()
    if not modelo:
        return False
    session.delete(modelo)
    session.commit()
    return True


def actualizar_fecha_ultimo_acceso(session: Session, dni: str, nueva_fecha: date) -> bool:
    modelo = session.query(SocioModel).filter(
        SocioModel.id == UsuarioModel.id,
        UsuarioModel.dni == dni
    ).first()
    if not modelo:
        return False
    modelo.fecha_ultimo_acceso = nueva_fecha
    session.commit()
    return True


def actualizar_esta_activo(session: Session, dni: str, activo: bool) -> bool:
    modelo = session.query(SocioModel).filter(
        SocioModel.id == UsuarioModel.id,
        UsuarioModel.dni == dni
    ).first()
    if not modelo:
        return False
    modelo.esta_activo = activo
    session.commit()
    return True


def actualizar_sueldo_monitor(session: Session, nombre: str, nuevo_sueldo: float) -> bool:
    modelo = session.query(MonitorModel).filter(
        MonitorModel.id == UsuarioModel.id,
        UsuarioModel.nombre.ilike(f"%{nombre}%")
    ).first()
    if not modelo:
        return False
    modelo.sueldo = nuevo_sueldo
    session.commit()
    return True


def actualizar_especialidades_monitor(session: Session, nombre: str, especialidades: list[Especialidad]) -> bool:
    modelo = session.query(MonitorModel).filter(
        MonitorModel.id == UsuarioModel.id,
        UsuarioModel.nombre.ilike(f"%{nombre}%")
    ).first()
    if not modelo:
        return False
    for esp in modelo.especialidades:
        session.delete(esp)
    session.flush()
    for esp in especialidades:
        session.add(MonitorEspecialidadModel(monitor_id=int(modelo.id), especialidad=esp.value))
    session.commit()
    return True


def votar_monitor(session: Session, nombre: str, like: bool) -> bool:
    modelo = session.query(MonitorModel).filter(
        MonitorModel.id == UsuarioModel.id,
        UsuarioModel.nombre.ilike(f"%{nombre}%")
    ).first()
    if not modelo:
        return False
    if like:
        modelo.votos_positivos += 1
    else:
        modelo.votos_negativos += 1
    session.commit()
    return True


def añadir_actividad_socio(session: Session, dni: str, nombre_actividad: str) -> bool:
    socio_model = session.query(SocioModel).filter(
        SocioModel.id == UsuarioModel.id,
        UsuarioModel.dni == dni
    ).first()
    act_model = session.query(ActividadModel).filter(
        ActividadModel.nombre.ilike(nombre_actividad)
    ).first()
    if not socio_model or not act_model:
        return False
    existe = session.query(SocioActividadModel).filter_by(
        socio_id=socio_model.id, actividad_id=act_model.id
    ).first()
    if existe:
        return False
    session.add(SocioActividadModel(socio_id=int(socio_model.id), actividad_id=int(act_model.id)))
    session.commit()
    return True


def eliminar_actividad_socio(session: Session, dni: str, nombre_actividad: str) -> bool:
    socio_model = session.query(SocioModel).filter(
        SocioModel.id == UsuarioModel.id,
        UsuarioModel.dni == dni
    ).first()
    act_model = session.query(ActividadModel).filter(
        ActividadModel.nombre.ilike(nombre_actividad)
    ).first()
    if not socio_model or not act_model:
        return False
    relacion = session.query(SocioActividadModel).filter_by(
        socio_id=socio_model.id, actividad_id=act_model.id
    ).first()
    if not relacion:
        return False
    session.delete(relacion)
    session.commit()
    return True


def convertir_socio_a_premium(session: Session, dni: str) -> bool:
    """Convierte un SocioModel en SocioPremiumModel"""
    socio_model = session.query(SocioModel).join(UsuarioModel).filter(
        UsuarioModel.dni == dni,
        UsuarioModel.tipo == "socio"
    ).first()
    if not socio_model:
        return False

    # Cambiar el discriminador y crear registro en socios_premium
    socio_model.tipo = "socio_premium"
    premium_model = SocioPremiumModel(id=socio_model.id, es_premium=True)
    session.add(premium_model)
    session.commit()
    return True


def inactivar_socios_antiguos(session: Session, dias: int = 30) -> list[str]:
    """Inactiva socios que no acceden desde hace 'dias' días. Devuelve nombres inactivados."""
    from datetime import timedelta
    limite = date.today() - timedelta(days=dias)
    modelos = session.query(SocioModel).filter(
        SocioModel.fecha_ultimo_acceso < limite,
        SocioModel.esta_activo == True
    ).all()
    nombres = []
    for m in modelos:
        m.esta_activo = False
        nombres.append(m.nombre)
    session.commit()
    return nombres


# ==============================================================
#  CONVERSORES: modelo BD -> objeto Python
# ==============================================================

def _modelo_a_actividad(session: Session, modelo: ActividadModel) -> Actividad:
    actividad = Actividad(
        nombre=modelo.nombre,
        duracion=modelo.duracion,
        calorias=modelo.calorias,
        categoria=Especialidad(modelo.categoria),
        es_premium=modelo.es_premium
    )
    for voto_model in modelo.votos:
        actividad.votar(voto_model.voto)
    return actividad


def _modelo_a_usuario(session: Session, modelo: UsuarioModel) -> Socio | SocioPremium | Monitor | None:
    if modelo is None:
        return None

    if modelo.tipo == "monitor":
        m = session.get(MonitorModel, modelo.id)
        especialidades = [Especialidad(e.especialidad) for e in m.especialidades]
        return Monitor(
            nombre=m.nombre, dni=m.dni, direccion=m.direccion,
            provincia=m.provincia, codigo_postal=m.codigo_postal,
            telefono=m.telefono, fecha_nacimiento=m.fecha_nacimiento,
            especialidad=especialidades, sueldo=m.sueldo,
            votos_positivos=m.votos_positivos, votos_negativos=m.votos_negativos
        )

    elif modelo.tipo == "socio_premium":
        sp = session.get(SocioPremiumModel, modelo.id)
        actividades = [_modelo_a_actividad(session, sa.actividad) for sa in sp.actividades]
        return SocioPremium(
            nombre=sp.nombre, dni=sp.dni, direccion=sp.direccion,
            provincia=sp.provincia, codigo_postal=sp.codigo_postal,
            telefono=sp.telefono, fecha_nacimiento=sp.fecha_nacimiento,
            fecha_registro=sp.fecha_registro, fecha_ultimo_acceso=sp.fecha_ultimo_acceso,
            esta_activo=sp.esta_activo, lista_actividades=actividades, es_premium=True
        )

    elif modelo.tipo == "socio":
        s = session.get(SocioModel, modelo.id)
        actividades = [_modelo_a_actividad(session, sa.actividad) for sa in s.actividades]
        return Socio(
            nombre=s.nombre, dni=s.dni, direccion=s.direccion,
            provincia=s.provincia, codigo_postal=s.codigo_postal,
            telefono=s.telefono, fecha_nacimiento=s.fecha_nacimiento,
            fecha_registro=s.fecha_registro, fecha_ultimo_acceso=s.fecha_ultimo_acceso,
            esta_activo=s.esta_activo, lista_actividades=actividades
        )

    return None