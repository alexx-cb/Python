from datetime import date
from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from Database.database import Base


class UsuarioModel(Base):
    """Tabla base para todos los usuarios (herencia con discriminador)"""
    __tablename__ = "usuarios"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    tipo        = Column(String(20), nullable=False)  # "socio", "socio_premium", "monitor"
    nombre      = Column(String(100), nullable=False)
    dni         = Column(String(9), unique=True, nullable=False)
    direccion   = Column(String(200), nullable=False)
    provincia   = Column(String(100), nullable=False)
    codigo_postal = Column(String(5), nullable=False)
    telefono    = Column(String(9), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)

    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "usuario"
    }


class SocioModel(UsuarioModel):
    """Tabla para socios (extiende usuarios)"""
    __tablename__ = "socios"

    id               = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    fecha_registro   = Column(Date, nullable=False, default=date.today)
    fecha_ultimo_acceso = Column(Date, nullable=False)
    esta_activo      = Column(Boolean, nullable=False, default=True)
    cuota            = Column(Float, nullable=False, default=0.0)

    actividades = relationship("SocioActividadModel", back_populates="socio", cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": "socio"
    }


class SocioPremiumModel(SocioModel):
    """Tabla para socios premium (extiende socios)"""
    __tablename__ = "socios_premium"

    id         = Column(Integer, ForeignKey("socios.id"), primary_key=True)
    es_premium = Column(Boolean, nullable=False, default=True)

    __mapper_args__ = {
        "polymorphic_identity": "socio_premium"
    }


class MonitorModel(UsuarioModel):
    """Tabla para monitores (extiende usuarios)"""
    __tablename__ = "monitores"

    id                = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    sueldo            = Column(Float, nullable=False)
    votos_positivos   = Column(Integer, nullable=False, default=0)
    votos_negativos   = Column(Integer, nullable=False, default=0)

    especialidades = relationship("MonitorEspecialidadModel", back_populates="monitor", cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": "monitor"
    }


class ActividadModel(Base):
    """Tabla para actividades"""
    __tablename__ = "actividades"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    nombre     = Column(String(100), nullable=False)
    duracion   = Column(Integer, nullable=False)
    calorias   = Column(Integer, nullable=False)
    categoria  = Column(String(50), nullable=False)
    es_premium = Column(Boolean, nullable=False, default=False)

    votos   = relationship("VotoModel", back_populates="actividad", cascade="all, delete-orphan")
    socios  = relationship("SocioActividadModel", back_populates="actividad")


class VotoModel(Base):
    """Tabla para votos de actividades"""
    __tablename__ = "votos"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    actividad_id = Column(Integer, ForeignKey("actividades.id"), nullable=False)
    voto        = Column(Integer, nullable=False)

    actividad = relationship("ActividadModel", back_populates="votos")


class SocioActividadModel(Base):
    """Tabla intermedia socio <-> actividad"""
    __tablename__ = "socio_actividades"

    socio_id     = Column(Integer, ForeignKey("socios.id"), primary_key=True)
    actividad_id = Column(Integer, ForeignKey("actividades.id"), primary_key=True)

    socio    = relationship("SocioModel", back_populates="actividades")
    actividad = relationship("ActividadModel", back_populates="socios")


class MonitorEspecialidadModel(Base):
    """Tabla intermedia monitor <-> especialidad"""
    __tablename__ = "monitor_especialidades"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    monitor_id  = Column(Integer, ForeignKey("monitores.id"), nullable=False)
    especialidad = Column(String(50), nullable=False)

    monitor = relationship("MonitorModel", back_populates="especialidades")